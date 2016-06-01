
var cps = require('../lib/cps.js');
var fib = require('./fib');
var assert = require("assert");

describe('cps', function() {
    describe('seq', function() {
        it('should return 3 for 1+2', function(cb) {
            var a, b;

            cps.seq([
                function(_, cb) {
                    setTimeout(function() {
                        cb(null, 1);
                    }, 0);
                },
                function(_, cb) {
                    a = _;
                    setTimeout(function() {
                        cb(null, 2);
                    }, 0);
                },
                function(_, cb) {
                    b = _;
                    cb(null, a + b);
                },
                function(_, cb) {
                    assert.equal(_, 3);
                    cb();
                }
            ], cb);
        });
    });

    describe('pwhile', function() {
        it('should return 2 for fib(2)', function(cb) {
            cps.seq([
                function(_, cb) {
                    fib(5, cb);
                },
                function(_, cb) {
                    assert.equal(_, 8);
                    cb();
                }
            ], cb);
        });

        it('should not fail for huge loops', function(cb) {
            this.timeout(0);
            var i;

            cps.seq([
                function(_, cb) {
                    i = 0;
                    cps.rescue({
                        'try': function(cb) {
                            cps.pwhile(
                                function(cb) {
                                    cb(null, i < 10000);
                                },
                                function(cb) {
                                    i++;
                                    cb();
                                },
                                cb
                            )
                        },
                        'catch': function(e, cb) {
                            console.log('ERROR: ', e);
                            throw e;
                        }
                    }, cb);
                },
                function(_, cb) {
                    console.log('i is: ', i);
                    cb();
                }
            ], cb);
        });
    });

    describe('pfor', function() {
        it('should return 45 for the sum of 0 through 9', function(cb) {
            var sum = 0;
            cps.seq([
                function(_, cb) {
                    cps.pfor(10, function(i, cb) {
                        setTimeout(function() {
                            sum += i;
                            cb();
                        }, 0);
                    }, cb);
                },
                function(_, cb) {
                    assert.equal(sum, 45);
                    cb();
                }
            ], cb);
        });
    });

    describe('peach', function() {
        it('should return 55 for the sum of 1 through 10', function(cb) {
            var sum = 0;

            cps.seq([
                function(_, cb) {
                    cps.peach(
                        [1,2,3,4,5,6,7,8,9,10],
                        function(el, cb) {
                            sum += el;
                            cb();
                        },
                        cb
                    );
                },
                function(_, cb) {
                    assert.equal(sum, 55);
                    cb();
                }
            ], cb);
        });
    });

    describe('pmap', function() {
        it('should return the list of squares of [1..10]', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.pmap(
                        [1,2,3,4,5,6,7,8,9,10],
                        function(el, cb) {
                            setTimeout(function() {
                                cb(null, el*el);
                            }, 0);
                        },
                        cb
                    );
                },
                function(_, cb) {
                    for (var i = 1; i <= 10; i++) {
                        assert.equal(_[i-1], i*i);
                    }
                    cb();
                }
            ], cb);
        });
    });

    describe('parallel', function() {
        it('should work for 3 parallel threads', function(cb) {
            this.timeout(0);

            var output = [];
            var start, end;

            cps.seq([
                function(_, cb) {
                    start = new Date();

                    cps.parallel([
                        function(cb) {
                            setTimeout(function() {
                                output.push(3);
                                cb(new Error('kaz'));
                            }, 3000);
                        },
                        function(cb) {
                            setTimeout(function() {
                                output.push(2);
                                cb(null, 'ok');
                            }, 2000);
                        },
                        function(cb) {
                            setTimeout(function() {
                                output.push(1);
                                cb(new Error('foobar'));
                            }, 1000);
                        }
                    ], cb);
                },
                function(_, cb) {
                    end = new Date();

                    assert(end-start < 3100, 'parallel is taking too long to run');

                    for (var i = 1; i <= 3; i++) {
                        assert.equal(output[i-1], i);
                    }

                    assert.equal(_[0].status, 'error');
                    assert.equal(_[0].error.message, 'kaz');

                    assert.equal(_[1].status, 'ok');
                    assert.equal(_[1].data, 'ok');

                    assert.equal(_[2].status, 'error');
                    assert.equal(_[2].error.message, 'foobar');

                    cb();
                }
            ], cb);
        });
    });

    describe('noFail', function() {
        it('should not fail on success', function(cb) {
            cps.noFail(function(cb) {
                cb(null, 1);
            }, cb);
        });

        it('should not fail on failure', function(cb) {
            cps.noFail(function(cb) {
                cb(new Error('foobar'));
            }, cb);
        });
    });

    describe('rescue', function() {
        it('should catch errors', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        },
                        'catch': function(err, cb) {
                            cb(null, 'ok');
                        }
                    }, cb);
                },
                function(_, cb) {
                    assert.equal(_, 'ok');
                    cb();
                }
            ], cb);
        });

        it('should be able to throw errors', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        }
                    }, cb);
                }
            ], function(err, res) {
                try {
                    assert.equal(err.message, 'foobar');
                    cb();
                } catch(e) {
                    cb(e);
                }
            });
        });

        it('should be able to rethrow errors', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        },
                        'catch': function(err, cb) {
                            throw new Error('kaz');
                        }
                    }, cb);
                }
            ], function(err, res) {
                try {
                    assert.equal(err.message, 'kaz');
                    cb();
                } catch(e) {
                    cb(e);
                }
            });
        });

        it('should execute finally clause on success', function(cb) {
            var finallyDone = false;

            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(null, 'ok');
                            }, 0);
                        },
                        'finally': function(cb) {
                            finallyDone = true;
                            cb();
                        }
                    }, cb);
                },
                function(_, cb) {
                    assert.equal(_, 'ok');
                    assert(finallyDone);
                    cb();
                }
            ], cb);
        });

        it('should execute finally clause on exception being caught', function(cb) {
            var finallyDone = false;

            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        },
                        'catch': function(err, cb) {
                            cb(null, 'exception caught');
                        },
                        'finally': function(cb) {
                            finallyDone = true;
                            cb();
                        }
                    }, cb);
                },
                function(_, cb) {
                    assert.equal(_, 'exception caught');
                    assert(finallyDone);
                    cb();
                }
            ], cb);
        });

        it('should execute finally clause on exception', function(cb) {
            var finallyDone = false;

            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        },
                        'finally': function(cb) {
                            finallyDone = true;
                            cb();
                        }
                    }, cb);
                }
            ], function(err, res) {
                try{
                    assert.equal(err.message, 'foobar');
                    assert(finallyDone);
                    cb();
                } catch(e) {
                    cb(e);
                }
            });
        });

        it('should throw exception in finally clause on success', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(null, 'ok');
                            }, 0);
                        },
                        'finally': function(cb) {
                            throw new Error('error in finally');
                            cb();
                        }
                    }, cb);
                }
            ], function(err, res) {
                try{
                    assert.equal(err.message, 'error in finally');
                    cb();
                } catch(e) {
                    cb(e);
                }
            });
        });

        it('should throw exception in finally clause on exception', function(cb) {
            cps.seq([
                function(_, cb) {
                    cps.rescue({
                        'try': function(cb) {
                            setTimeout(function() {
                                cb(new Error('foobar'));
                            }, 0);
                        },
                        'finally': function(cb) {
                            throw new Error('error in finally');
                            cb();
                        }
                    }, cb);
                }
            ], function(err, res) {
                try{
                    assert.equal(err.message, 'error in finally');
                    cb();
                } catch(e) {
                    cb(e);
                }
            });
        });
    });
});