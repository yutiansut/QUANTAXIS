var grunt = require("grunt");
var phantomjs = require('grunt-lib-phantomjs').init(grunt);
var difflib = require("jsdifflib");

module.exports = {
    testStockExample: function (asyncDone, showDiff) {
        var passed = false;
        process.env.TZ = "UTC";

        phantomjs.on('rendered', function(pageStr) {
            require("fs").readFile(__dirname + '/rendered-stock-fixture.html', function (err, data) {
                var fixtureStr = data.toString();

                if (err) {
                    grunt.log.error("Failed to open stock example.");
                } else {
                    var diffs = diffPages(fixtureStr, pageStr);
                    if (diffs.length > 0) {
                        grunt.log.error("Failed comparison to stock example.");
                        grunt.log.error("If these changes are intentional, please run `grunt update-stock-example` to overwrite the fixture.");
                        if (showDiff) {
                            grunt.log.writeln("\n" + diffs + "\n");
                        } else {
                            grunt.log.error("Run `grunt test-stock-example:diff` to see differences.");
                        }
                    } else {
                        grunt.log.writeln("Passed comparison to stock example.");
                        passed = true;
                    }
                }
                phantomjs.halt();
            });
        });

        phantomjs.spawn('web/index.html', {
            options: {
                inject: __dirname + "/inject-serializer.js"
            },
            done: function () {
                if (!passed) {
                    grunt.fatal("Failed regression test.");
                }
                asyncDone();
            }
        });
    },

    updateStockExample: function (asyncDone) {
        var ok = false;
        process.env.TZ = "UTC";

        phantomjs.on('rendered', function(pageStr) {
            require("fs").writeFile(__dirname + '/rendered-stock-fixture.html', pageStr, function (err) {
                if (!err) {
                    grunt.log.writeln("Overwrote stock example.");
                    ok = true;
                }
                phantomjs.halt();
            });
        });

        phantomjs.spawn('web/index.html', {
            options: {
                inject: __dirname + "/inject-serializer.js"
            },
            done: function () {
                if (!ok) {
                    grunt.fatal("Failed to overwrite stock example.");
                }
                asyncDone();
            }
        });
    }
};

function diffPages(first, second) {
    first = filterExceptions(first);
    second = filterExceptions(second);

    var firstLines = difflib.stringAsLines(first);
    var secondLines = difflib.stringAsLines(second);
    var seq = new difflib.SequenceMatcher(firstLines, secondLines);
    var ops = seq.get_opcodes();
    var diffs = [];

    for (var i = 0; i < ops.length; i++) {
        var op = ops[i];
        var firstDiff = firstLines.slice(op[1], op[2]).join("\n");
        var secondDiff = secondLines.slice(op[3], op[4]).join("\n");

        if (op[0] === 'replace') {
            if (!onlyDiffersByDelta(firstDiff, secondDiff, 0.01)) {
                diffs.push("Replacement:");
                diffs.push(firstDiff.red);
                diffs.push(secondDiff.green);
            }
        } else if (op[0] === 'insert') {
            diffs.push("Insertion:");
            diffs.push(secondDiff.green);
        } else if (op[0] === 'delete') {
            diffs.push("Deletion:");
            diffs.push(firstDiff.red);
        }
    }

    return diffs.join("\n\n");
}

// TODO: remove use of clientHeight in legend and remove this function
function filterExceptions(fixtureStr) {
    fixtureStr = fixtureStr.replace(/<text x="15" y="[0-9.]+">Monthly Index Move<\/text>/, "EXCEPTION");
    fixtureStr = fixtureStr.replace(/<text x="15" y="[0-9.]+">Monthly Index Average<\/text>/, "EXCEPTION");
    return fixtureStr;
}

function onlyDiffersByDelta(firstLine, secondLine, delta) {
    var findNums = /(?:[0-9]*\.[0-9]+|[0-9]+)/g;

    var firstNums = firstLine.match(findNums);
    var secondNums = secondLine.match(findNums);

    var firstWithoutNums = firstLine.replace(findNums, "NUMBER");
    var secondWithoutNums = secondLine.replace(findNums, "NUMBER");

    if (firstWithoutNums !== secondWithoutNums) {
        return false;
    }

    if (secondNums.length !== firstNums.length) {
        return false;
    }

    for (var i = 0; i < firstNums.length; i++) {
        if (Math.abs(+firstNums[i] - +secondNums[i]) > delta) {
            return false;
        }
    }

    return true;
}
