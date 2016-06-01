// reporter for saucelabs
jasmine.getEnv().addReporter(new jasmine.JSReporter2());

(function () {
    var oldJSReport = window.jasmine.getJSReport;
    window.jasmine.getJSReport = function () {
        var results = oldJSReport();
        if (results) {
            return {
                durationSec: results.durationSec,
                suites: removePassingTests(results.suites),
                passed: results.passed
            };
        } else {
            return null;
        }
    };

    function removePassingTests (suites) {
        return suites.filter(specFailed)
            .map(mapSuite);
    }

    function mapSuite (suite) {
        var result = {};
        for (var s in suite) {
            result[s] = suite[s];
        }
        result.specs = suite.specs.filter(specFailed);
        result.suites = removePassingTests(suite.suites);
        return result;
    }

    function specFailed (item) {
        return !item.passed;
    }
})();
