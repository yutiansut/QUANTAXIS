/* global appendChartID, makeDate */
describe('dc.filter-dates', function () {
    // do date filters work correctly?
    // adapted from a fiddle demonstrating the problem by Matt Traynham
    // see it fail with 1.7.1: http://jsfiddle.net/gordonwoodhull/Q2H9C/4/
    // see it win with 2.0: http://jsfiddle.net/gordonwoodhull/Q2H9C/3/
    // (Thanks!!)

    var dateDim1, dateDim2, group1, group2,
        row1, row2;
    var width = 400;
    var height = 200;
    var margins = {top: 15, right: 10, bottom: 20, left: 40};
    beforeEach(function () {
        // Months are 0 indexed...
        var start = makeDate(2013, 10, 1);
        var end = makeDate(2013, 11, 1);
        var stringLength = 2;

        // Generate Random Data [Date, VowelString, Random Number, Random Measure]
        var data = [];
        for (var i = 0; i < 2000; i++) {
            data[i] = [
                randomDate(start, end),
                randomVowelString(stringLength),
                Math.floor(Math.random() * 20),
                Math.floor(Math.random() * 30000)
            ];
        }

        var ndx = crossfilter(data);
        dateDim1 = ndx.dimension(function (d) { return d[0]; });
        dateDim2 = ndx.dimension(function (d) { return d[0]; });

        group1 = dateDim1.group().reduceSum(function (d) { return d[3]; });
        group2 = dateDim2.group().reduceSum(function (d) { return d[3]; });

        appendChartID(row1);
        appendChartID(row2);

        row1 = dc.rowChart('row1')
            .width(width)
            .height(height)
            .margins(margins)
            .dimension(dateDim1)
            .group(group1)
            .gap(1)
            .render();

        row2 = dc.rowChart('row2')
            .width(width)
            .height(height)
            .margins(margins)
            .dimension(dateDim2)
            .group(group2)
            .gap(1)
            .render();
    });

    it('filtering on 11/8 should keep only that row', function () {
        row1.filter(makeDate(2013, 10, 8));
        expect(group1.all()[6].value).not.toEqual(0);
        expect(group2.all()[6].value).toEqual(0);
        expect(group2.all()[7]).toEqual(group1.all()[7]);
        expect(group2.all()[8].value).toEqual(0);
    });

    it('filtering on 11/17 should keep only that row', function () {
        row1.filter(makeDate(2013, 10, 17));
        expect(group1.all()[15].value).not.toEqual(0);
        expect(group2.all()[15].value).toEqual(0);
        expect(group2.all()[16]).toEqual(group1.all()[16]);
        expect(group2.all()[17].value).toEqual(0);
    });

    // Create a Random Date
    function randomDate (start, end) {
        var d = new Date(start.getTime() + Math.random() * (end.getTime() - start.getTime()));
        d.setUTCHours(0,0,0,0);
        return d;
    }

    // Create a Random String of vowels
    var vowels = ['a','e','i','o','u','y'];
    function randomVowelString (length) {
        var val = '';
        for (var i = 0; i < length; i++) {
            val = val + vowels[Math.floor(Math.random() * (vowels.length - 1))];
        }
        return val;
    }
});
