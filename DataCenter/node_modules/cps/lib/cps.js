
var Tail = require('./tail');

module.exports = function() {
    var procedure = function(fn) {
        return function() {
            var cb = arguments[arguments.length - 1];

            try {
                fn.apply(this, arguments);
            } catch(e) {
                handleError(e, cb);
            }
        };
    };

    var handleError = function(e, cb) {
        cb(e);
    };

    var callback = function(cb, fn) {
        var called = false;

        return function(err) {
            if (called) {
                if (err) {
                    console.log(err);
                    if (err.stack) {
                        console.log(err.stack);
                    }
                }
                throw new Error('Continuation is being called more than once!');
            }
            called = true;
            try {
                if (err) {
                    handleError(err, cb);
                } else {
                    fn.apply(this, arguments);
                }
            } catch(e) {
                handleError(e, cb);
            }
        };
    };

    var _seq = procedure(function(procs, i, res, cb) {
        if (i >= procs.length) {
            return cb(null, res);
        }
        var proc = procs[i];
        proc(res, callback(cb, function(err, res) {
            // return _seq(procs, i+1, res, cb);
            return Tail.run(function() {
                _seq(procs, i+1, res, cb);
            });
        }));
    });

    var seq = function(procs, cb) {
        return _seq(procs, 0, null, cb);
    };

    var rescue = procedure(function(procBundle, cb) {
        var tryProc = procBundle['try'];
        var catchProc = procBundle['catch'] || function(err, cb) {cb(err);};
        var finallyProc = procBundle['finally'] || function(cb) {cb();};

        var applyTry = procedure(function(cb) {
            tryProc(cb);
        });

        var applyCatch = procedure(function(err, cb) {
            catchProc(err, cb);
        });

        var applyFinallyOk = procedure(function(res0, cb) {
            finallyProc(callback(cb, function(err, res) {
                cb(null, res0);
            }));
        });

        var applyFinallyError = procedure(function(err0, cb) {
            finallyProc(callback(cb, function(err, res) {
                cb(err0);
            }));
        });

        applyTry(function(err, res) {
            if (err) {
                applyCatch(err, function(err, res) {
                    if (err) {
                        applyFinallyError(err, cb);
                    } else {
                        applyFinallyOk(res, cb);
                    }
                });
            } else {
                applyFinallyOk(res, cb);
            }
        });
    });

    var pwhile = procedure(function(procBool, procBody, cb) {
        seq([
            function(_, cb) {
                procBool(cb);
            },
            function(_, cb) {
                if (_) {
                    seq([
                        function(_, cb) {
                            procBody(cb);
                        },
                        function(_, cb) {
                            pwhile(procBool, procBody, cb);
                        }
                    ], cb);
                } else {
                    cb();
                }
            }
        ], cb);
    });

    var peach = procedure(function(arr, proc, cb) {
        var i = 0;

        pwhile(
            function(cb) {
                cb(null, i < arr.length);
            },
            function(cb) {
                seq([
                    function(_, cb) {
                        proc(arr[i], cb);
                    },
                    function(_, cb) {
                        i++;
                        cb();
                    }
                ], cb);
            },
            cb
        )
    });

    var pfor = procedure(function(n, proc, cb) {
        var i = 0;

        pwhile(
            function(cb) {
                cb(null, i < n);
            },
            function(cb) {
                seq([
                    function(_, cb) {
                        proc(i, cb);
                    },
                    function(_, cb) {
                        i++;
                        cb();
                    }
                ], cb);
            },
            cb
        );
    });

    var pmap = procedure(function(arr, proc, cb) {
        var l = [];

        seq([
            function(_, cb) {
                peach(arr, function(e, cb) {
                    seq([
                        function(_, cb) {
                            proc(e, cb);
                        },
                        function(_, cb) {
                            l.push(_);
                            cb();
                        }
                    ], cb);
                }, cb);
            },
            function(_, cb) {
                cb(null, l);
            }
        ], cb);
    });

    var _parallel2 = procedure(function(proc1, proc2, cb) {
        var state1 = 'start';
        var state2 = 'start';
        var res1;
        var res2;
        var err1;
        var err2;

        var applyProc1 = procedure(function(cb) {
            proc1(cb);
        });

        var applyProc2 = procedure(function(cb) {
            proc2(cb);
        });

        applyProc1(function(err, res) {Tail.run(function() {
            if (err) {
                state1 = 'error';
                err1 = err;
                switch(state2) {
                    case 'start':
                        break;
                    case 'done':
                        cb(null, [
                            {status: 'error', error: err1},
                            {status: 'ok', data: res2}
                        ]);
                        break;
                    case 'error':
                        cb(null, [
                            {status: 'error', error: err1},
                            {status: 'error', error: err2}
                        ]);
                        break;
                    default:
                }
            } else {
                state1 = 'done';
                res1 = res;
                switch(state2) {
                    case 'start':
                        break;
                    case 'done':
                        cb(null, [
                            {status: 'ok', data: res1},
                            {status: 'ok', data: res2}
                        ]);
                        break;
                    case 'error':
                        cb(null, [
                            {status: 'ok', data: res1},
                            {status: 'error', error: err2}
                        ]);
                        break;
                    default:
                }
            }
        })});

        applyProc2(function(err, res) {Tail.run(function() {
            if (err) {
                state2 = 'error';
                err2 = err;
                switch(state1) {
                    case 'start':
                        break;
                    case 'done':
                        cb(null, [
                            {status: 'ok', data: res1},
                            {status: 'error', error: err2}
                        ]);
                        break;
                    case 'error':
                        cb(null, [
                            {status: 'error', error: err1},
                            {status: 'error', error: err2}
                        ]);
                        break;
                    default:
                }
            } else {
                state2 = 'done';
                res2 = res;
                switch(state1) {
                    case 'start':
                        break;
                    case 'done':
                        cb(null, [
                            {status: 'ok', data: res1},
                            {status: 'ok', data: res2}
                        ]);
                        break;
                    case 'error':
                        cb(null, [
                            {status: 'error', error: err1},
                            {status: 'ok', data: res2}
                        ]);
                        break;
                    default:
                }
            }
        })});
    });

    var _parallel = procedure(function(procs, i, cb) {
        if (procs.length == 0) {
            return cb();
        }

        if (i == procs.length - 1) {
            return procs[i](function(err, res) {
                if (err) {
                    cb(null, [{status: 'error', error: err}]);
                } else {
                    cb(null, [{status: 'ok', data: res}]);
                }
            });
        }

        if (i < procs.length) {
            _parallel2(
                procs[i],
                function(cb) {
                    _parallel(procs, i+1, cb);
                },
                callback(cb, function(err, res) {
                    cb(null, [res[0]].concat(res[1].data));
                })
            );
        }
    });

    var parallel = procedure(function(procs, cb) {
        _parallel(procs, 0, cb);
    });

    var noFail = function() {
        var proc, handler, cb;

        proc = arguments[0];
        cb = arguments[arguments.length - 1];

        if (arguments.length == 2) {
            handler = function(err) {
                console.log('ERROR caught by cps.noFail: ', err);
                if (err.stack) {
                    console.log(err.stack);
                }
            };
        } else if (arguments.length == 3) {
            handler = arguments[1];
        } else {
            handleError(new Error('Incorrect number of arguments in calling cps.noFail.'), cb);
        }

        rescue({
            'try': function(cb) {
                proc(cb);
            },
            'catch': function(err, cb) {
                handler(err);
                cb();
            }
        }, cb);
    };

    var run = function(proc, cfg) {
        cfg = cfg || {};

        var cb = function(err, res) {
            try {
                if (err) {
                    if (cfg['error']) {
                        cfg['error'](err);
                    } else {
                        console.log('cps.run ERROR: ', err);
                        if (err.stack) {
                            console.log(err.stack);
                        }
                    }
                } else {
                    if (cfg['ok']) {
                        cfg['ok'](res);
                    } else {
                        console.log('cps.run OK: ', res);
                    }
                }
            } catch(e) {
                if (cfg['topLevelError']) {
                    cfg['topLevelError'](e);
                } else {
                    console.log('cps.run TOP_LEVEL_ERROR: ', e);
                }
            } finally {
                if (cfg['finally']) {
                    try {
                        cfg['finally']();
                    } catch(e) {
                        console.log('cps.run FINALLY_ERROR: ', e);
                    }
                }
            }
        };

        proc(cb);
    };

    return {
        seq: seq,
        peach: peach,
        pwhile: pwhile,
        pmap: pmap,
        pfor: pfor,
        rescue: rescue,
        parallel: parallel,
        noFail: noFail,
        run: run
    };
}();
