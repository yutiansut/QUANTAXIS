
var Class = require('better-js-class');

var cps = require('cps');

var mysql = require('mysql');

var $U = require('underscore');

var getValue = function(o) {
    for (var k in o) {
        return o[k];
    }
};


module.exports = function() {
    var DB = Class({
        _init: function(cfg) {
            var transactionOverride = cfg['useTransaction'];
            delete cfg['useTransaction'];

            var cursorOverride = cfg['useCursor'];
            delete cfg['useCursor'];

            this._cfg = cfg;
            // console.log(this._cfg);
            this._pool = mysql.createPool(this._cfg);

            if (transactionOverride) {
                this._transactionCfg = this._buildCfg(cfg, transactionOverride);
                // console.log('transactionCfg:', this._transactionCfg);
                this._transactionPool = mysql.createPool(this._transactionCfg);
            }

            if (cursorOverride) {
                this._cursorCfg = this._buildCfg(cfg, cursorOverride);
                // console.log('cursorCfg:', this._cursorCfg);
                this._cursorPool = mysql.createPool(this._cursorCfg);
            }

            this._schema = {};
            this._prepared = false;
        },

        _buildCfg: function(cfg, override) {
            var res = {};

            for (var k in cfg) {
                res[k] = cfg[k];
            }

            $U.extend(res, override);
            return res;
        },

        connect: function(proc, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me._prepare(cb);
                },
                function(_, cb) {
                    me._connect(me._pool, proc, cb);
                }
            ], cb);
        },

        _prepare: function(cb) {
            if (this._prepared) {
                return cb();
            }

            // console.log('call prepare');
            var me = this;
            var conn;

            this._connect(me._pool, function(conn, cb) {
                cps.seq([
                    function(res, cb) {
                        conn.query('show tables', cb);
                    },
                    function(tables, cb) {
                        cps.peach(tables, function(table, cb) {
                            var tableName = getValue(table);
                            cps.seq([
                                function(_, cb) {
                                    conn.query('desc ' + tableName, cb);
                                },
                                function(columns, cb) {
                                    me._schema[tableName] = $U.map(columns, function(column) {
                                        return column['Field'];
                                    });
                                    me._prepared = true;
                                    cb();
                                }
                            ], cb);
                        }, cb);
                    }
                ], cb);
            }, cb);
        },

        _connect: function(pool, proc, cb) {
            var me = this;
            var conn;
            cps.seq([
                function(_, cb) {
                    pool.getConnection(cb);
                },
                function(res, cb) {
                    conn = res;
                    cps.rescue({
                        'try': function(cb) {
                            proc(conn, cb);
                        },
                        'finally': function(cb) {
                            // console.log('release connection');
                            conn.release();
                            cb();
                        }
                    }, cb);
                }
            ], cb);
        },

        transaction: function(conn, proc, cb) {
            var me = this;

            if (!me._transactionPool) {
                cb(new Error('transaction-not-setup-error'));
                return;
            }

            var txnConn;
            var commitRes;

            if (me._isTxnConnection(conn)) {
                proc(conn, cb);
            } else {
                cps.seq([
                    function(_, cb) {
                        me._prepare(cb);
                    },
                    /*
                    function(_, cb) {
                        me._getTxnConnection(cb);
                    },
                    */
                    function(_, cb) {
                        me._connect(me._transactionPool, function(conn, cb) {
                            me._enterTransaction(conn);
                            txnConn = conn;
                            cps.rescue({
                                'try': function(cb) {
                                    cps.seq([
                                        function(_, cb) {
                                            // console.log('start transaction');
                                            txnConn.query('START TRANSACTION', cb);
                                        },
                                        function(_, cb) {
                                            cps.rescue({
                                                'try': function(cb) {
                                                    cps.seq([
                                                        function(_, cb) {
                                                            proc(txnConn, cb);
                                                        },
                                                        function(res, cb) {
                                                            commitRes = res;
                                                            // console.log('committing');
                                                            txnConn.query('COMMIT', cb);
                                                        },
                                                        function(_, cb) {
                                                            // console.log('committed');
                                                            cb(null, commitRes);
                                                        }
                                                    ], cb);
                                                },
                                                'catch': function(err, cb) {
                                                    cps.seq([
                                                        function(_, cb) {
                                                            // console.log('rolling back ...');
                                                            txnConn.query('ROLLBACK', cb);
                                                        },
                                                        function(_, cb) {
                                                            // console.log('rolled back');
                                                            throw(err);
                                                        }
                                                    ], cb);
                                                }
                                            }, cb);
                                        }
                                    ], cb);
                                },
                                'finally': function(cb) {
                                    // console.log('txn connection release');
                                    // txnConn.release();
                                    me._leaveTransaction(txnConn);
                                    cb();
                                }
                            }, cb);
                        }, cb);
                    }
                ], cb);
            }
        },

        cursor: function(q, proc, _cb) {
            var me = this;

            if (!me._cursorPool) {
                _cb(new Error('cursor-not-setup-error'));
                return;
            }

            var returned = false;

            var cb = function(err, res) {
                if (!returned) {
                    returned = true;
                    _cb(err, res);
                } else {
                }
            }

            var breakCB =  cb;
            this._cursorPool.getConnection(function(err, conn) {
                var query = conn.query(q);
                query
                    .on('error', function(err) {
                        // console.log('cursor error');
                        conn.release();
                        cb(new Error(err));
                    })
                    .on('result', function(res) {
                        // console.log('cursor result');
                        conn.pause();

                        var cb = function(err, res) {
                            if (err) {
                                conn.release();
                                breakCB(err);
                            } else {
                                conn.resume();
                            }
                        };

                        cps.seq([
                            function(_, cb) {
                                // console.log('call row processor');
                                proc(res, cb);
                            }
                        ], cb);
                    })
                    .on('end', function() {
                        // console.log('cursor end');
                        conn.release();
                        cb();
                    })
                ;
            });
        },

        _isTxnConnection: function(conn) {
            return conn != null && conn.__transaction__;
        },

        _enterTransaction: function(conn) {
            conn.__transaction__ = true;
        },

        _leaveTransaction: function(conn) {
            conn.__transaction__ = false;
        },

        end: function() {
            this._pool.end();
            if (this._transactionPool) {
                this._transactionPool.end();
            }
            if (this._cursorPool) {
                this._cursorPool.end();
            }
        },

        getConnection: function(cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me._prepare(cb);
                },
                function(_, cb) {
                    me._pool.getConnection(cb);
                }
            ], cb);
        }
    });

    $U.extend(DB, {
        format: function(str, bindings) {
            var l = str.split('?')

            if (l.length - 1 != bindings.length) {
                throw new Error('sql string format error');
            }

            var res = [];

            for (var i = 0; i < bindings.length; i++) {
                res.push(l[i]);
                res.push(mysql.escape(bindings[i]));
            }

            res.push(l[l.length - 1]);

            return res.join(' ');
        }
    });

    return DB;
}();
