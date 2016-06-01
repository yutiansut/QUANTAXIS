function parseTranslate (actual) {
    var parts = /translate\((-?[\d\.]*)(?:[, ](.*))?\)/.exec(actual);
    if (!parts) {
        return null;
    }
    if (parts[2] === undefined) {
        parts[2] = 0;
    }
    expect(parts.length).toEqual(3);
    return parts;
}

function parseTranslateRotate (actual) {
    var parts = /translate\((-?[\d\.]*)(?:[, ](.*))?\)[, ]rotate\((-?[\d\.]*)\)/.exec(actual);
    if (!parts) {
        return null;
    }
    if (parts[2] === undefined) {
        parts[2] = 0;
    }
    expect(parts.length).toEqual(4);
    return parts;
}

function parsePath (path) {
    // an svg path is a string of any number of letters
    // each followed by zero or more numbers separated by spaces or commas
    var instrexp = /([a-z])[^a-z]*/gi,
        argexp = /(-?\d+(?:\.\d*)?)[, ]*/gi;
    var match, result = [], die = 99;
    while ((match = instrexp.exec(path))) {
        var instr = match[0];
        var cmd = {op: match[1], args: []};
        argexp.lastIndex = 0;
        while ((match = argexp.exec(instr))) {
            cmd.args.push(match[1]);
        }
        result.push(cmd);
        if (!--die) {
            throw 'give up';
        }
    }
    return result;
}

// there doesn't seem to be any way to access jasmine custom matchers
function compareWithinDelta (actual, expected, delta) {
    if (delta === undefined) {
        delta = 1e-6;
    }

    var result = {};

    result.pass = actual >= (+expected - delta) && actual <= (+expected + delta);

    var pre = 'Expected ' + actual + ' to ',
        post = 'be within [' + (+expected - delta) + '/' + (+expected + delta) + ']';

    if (result.pass) {
        result.message = pre + 'not ' + post;
    } else {
        result.message = pre + post;
    }

    return result;
}

// note: to make these reusable as boolean predicates, they only returns the first
// failure instead of using expect

function compareSubPath (got, wanted, i, j, delta) {
    for (var k = 0; k !== wanted.length; ++k) {
        var commandNum = 'path command #' + i + k;
        if (got[i + k].op.toUpperCase() !== wanted[j + k].op.toUpperCase()) {
            return {
                pass: false,
                message: commandNum + ' actual \'' + got[i + k].op.toUpperCase() +
                '\' != expected \'' + wanted[j + k].op.toUpperCase() + '\''
            };
        }
        if (got[i + k].args.length !== wanted[j + k].args.length) {
            return {
                pass: false,
                message: commandNum + ' number of arguments ' +
                got[i + k].args.length + ' != expected ' + wanted[j + k].args.length
            };
        }
        for (var h = 0; h < got[i + k].args.length; ++h) {
            var result = compareWithinDelta(got[i + k].args[h], wanted[j + k].args[h], delta);
            if (!result.pass) {
                result.message = commandNum + ', element ' + h + ': ' + result.message;
                return result;
            }
        }
    }
    return {pass: true};
}

function comparePaths (actual, expected, delta) {
    delta = delta || 1; // default delta of 1px
    var got = parsePath(actual),
        wanted = parsePath(expected);
    if (got.length !== wanted.length) {
        return {
            pass: false,
            message: 'actual number of path cmds ' + actual.length +
            ' did not match expected number ' + expected.length
        };
    }
    return compareSubPath(got, wanted, 0, 0, delta);
}

function findSubPath (actual, expected, delta) {
    delta = delta || 1; // default delta of 1px
    var got = parsePath(actual),
        wanted = parsePath(expected),
        end = got.length - wanted.length;
    for (var i = 0; i < end; ++i) {
        var result = compareSubPath(got, wanted, i, 0, delta);
        if (result.pass) {
            return result;
        }
    }
    return {
        pass: false,
        message: 'did not find expected subpath \'' + expected + '\' in actual path \'' + actual + '\''
    };
}

// actually number list, but presumably you'd want closeness if you need that
function compareIntList (actual, expected) {
    var aparts = actual.split(/, */),
        eparts = expected.split(/, */);
    if (aparts.length !== eparts.length) {
        return {
            pass: false,
            message: 'actual number of list items ' + aparts.length +
                ' did not match expected number ' + eparts.length
        };
    }
    for (var i = 0; i < eparts.length; ++i) {
        if (+aparts[i] !== +eparts[i]) {
            return {
                pass: false,
                message: 'list item[' + i + '] value ' + aparts[i] + ' did not equal expected value ' + eparts[i]
            };
        }
    }
    return {pass: true};
}

beforeEach(function () {
    jasmine.addMatchers({
        toBeWithinDelta: function (_) {
            return {
                compare: compareWithinDelta
            };
        },
        // note: all of these custom matchers ignore the possibility of .not.toMatch
        // (can't imagine how that would be useful here)
        toMatchTranslate: function () {
            return {
                compare: function (actual, x, y, prec) {
                    var parts = parseTranslate(actual);
                    if (!parts) {
                        return {pass: false, message: '\'' + actual + '\' did not match translate(x[,y]) regexp'};
                    }
                    expect(+parts[1]).toBeCloseTo(x, prec);
                    expect(+parts[2]).toBeCloseTo(y, prec);
                    return {pass: true};
                }
            };
        },
        toMatchTransRot: function () {
            return {
                compare: function (actual, x, y, r, prec) {
                    var parts = parseTranslateRotate(actual);
                    if (!parts) {
                        return {pass: false, message: '\'' + actual + '\' did not match translate(x[,y]),rotate(r) regexp'};
                    }
                    expect(+parts[1]).toBeCloseTo(x, prec);
                    expect(+parts[2]).toBeCloseTo(y, prec);
                    expect(+parts[3]).toBeCloseTo(r, prec);
                    return {pass: true};
                }
            };
        },
        toMatchUrl: function () {
            return {
                compare: function (actual, url) {
                    var regexp = new RegExp('url\\("?' + url + '"?\\)');
                    expect(actual).toMatch(regexp);
                    return {pass: true};
                }
            };
        },
        toMatchPath: function () {
            return {
                compare: comparePaths
            };
        },
        toContainPath: function () {
            return {
                compare: findSubPath
            };
        },
        toEqualIntList: function () {
            return {
                compare: compareIntList
            };
        }
    });
});
