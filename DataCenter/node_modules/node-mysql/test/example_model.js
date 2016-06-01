
var cps = require('cps');
var Class = require('better-js-class');
var $U = require('underscore');

var db = require('../lib/node-mysql.js');
var DB = db.DB;


var cb = function() {
    var handleError = function(e) {
        if (e.stack) {
            console.log(e.stack);
        } else {
            console.log(e);
        }
    };

    var start = new Date();
    return function(err, res) {
        try {
            var end = new Date();
            console.log('time spent: ', end-start);
            if (err) {
                handleError(err);
            } else {
                console.log(res);
            }
        } catch(e) {
            handleError(e);
        } finally {
            // dw.end();
        }
    };
}();

var dw = new db.DB({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'data_warehouse_dev'
});

var Model = function() {
    var cls = {
    };

    var Row = Class(db.Row, {
        _init: function(data) {
            this.parent._init.call(this, data, {
                table: Table
            });
        }
    });

    var TableClass = Class(db.Table, {
    });

    var Table = new TableClass({
        'name': 'subscription_initiation',
        'idFieldName': 'id',
        'rowClass': Row,
        'db': dw
    });

    $U.extend(cls, {
        Row: Row,
        Table: Table
    });

    return cls;
}();


var findAndUpdateTest = function(cb) {
    dw.connect(function(conn, cb) {
        var o;
        cps.seq([
            function(_, cb) {
                var q = Model.Table.baseQuery('order by date_created desc limit 1');
                console.log(q);
                Model.Table.find(conn, q, cb);
            },
            function(res, cb) {
                o = res[0];
                var dto = {
                    'first_shipment_id': 300,
                    'junk': function() {}
                };
                o.update(conn, dto, cb);
            },
            function(res, cb) {
                console.log(res);
                cb();
            }
        ], cb);
    }, cb);
};


var getSampleDto = function() {
    return {
        id: 46585,
        user_id: '1',
        subscription_id: '1',
        order_id: '1',
        product_id: '1',
        init_date: new Date(),
        subscription_status: 'inactive',
        date_created: new Date(),
        last_updated: new Date(),
        version: 100
    }
};

var createTest = function(cb) {
    dw.connect(function(conn, cb) {
        cps.seq([
            function(_, cb) {
                Model.Table.clone(conn, getSampleDto(), cb);
            },
            function(res, cb) {
                console.log(res);
                cb();
            }
        ], cb);
    }, cb);
};

var txnTest = function(cb) {
    var add2Rows = function(conn, b, cb) {
        dw.transaction(conn, function(conn, cb) {
            cps.seq([
                function(_, cb) {
                    Model.Table.create(conn, getSampleDto(), cb);
                },
                function(_, cb) {
                    dw.transaction(conn, function(conn, cb) {
                        Model.Table.create(conn, getSampleDto(), cb);
                    }, cb);
                },
                function(_, cb) {
                    if (b) {
                        cb(null, "Commit");
                    } else {
                        throw new Error("Roll back");
                    }
                }
            ], cb);
        }, cb);

    };

    dw.connect(function(conn, cb) {
        // dw.transaction(conn, function(conn, cb) {
            cps.seq([
                function(_, cb) {
                    add2Rows(conn, true, cb);
                },
                function(_, cb) {
                    add2Rows(conn, true, cb);
                }
            ], cb);
        // }, cb);
    }, cb);
};

var lockTest = function(cb) {
    var id = 74;

    var exclusiveUpdate = function(conn, delay, value, cb) {
        dw.transaction(conn, function(conn, cb) {
            cps.seq([
                function(_, cb) {
                    console.log('start to lock: ' + value);
                    Model.Table.lockById(conn, id, cb);
                },
                function(res, cb) {
                    console.log('locked to update to: ' + value);
                    setTimeout(function() {
                        cb(null, res);
                    }, delay);
                },
                function(row, cb) {
                    if (value == 'foo1') {
                        row.update(conn, {'product_id': 50}, cb);
                    } else {
                        row.update(conn, {'subscription_status': value}, cb);
                    }
                },
                function(res, cb) {
                    console.log('updated with value: ' + value);
                    console.log(res);
                    cb();
                }
            ], cb)
        }, cb);
    };

    var conn;

    dw.connect(function(conn, cb) {
        cps.seq([
            function(_, cb) {
                cps.parallel([
                    function(cb) {
                        exclusiveUpdate(conn, 2000, 'foo1', cb);
                    },
                    function(cb) {
                        exclusiveUpdate(conn, 0, 'bar1', cb);
                    }
                ], cb);
            },
            function(res, cb) {
                console.log(res);
                cb();
            }
        ], cb);
    }, cb);
};


createTest(cb);
