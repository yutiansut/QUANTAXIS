/* global loadDateFixture */
describe('dc.colorMixin', function () {
    function colorTest (chart, domain, test) {
        chart.colorDomain(domain);
        return (test || domain).map(chart.getColor);
    }

    function identity (d) { return d; }

    describe('with ordinal domain' , function () {
        var chart, domain;

        beforeEach(function () {
            chart = dc.colorMixin({});
            chart.colorAccessor(identity);
            domain = ['a','b','c','d','e'];
        });

        it('default', function () {
            expect(colorTest(chart,domain)).toEqual(['#3182bd','#6baed6','#9ecae1','#c6dbef','#e6550d']);
        });

        it('custom', function () {
            chart.colors(d3.scale.category10());
            expect(colorTest(chart,domain)).toEqual(['#1f77b4','#ff7f0e','#2ca02c','#d62728','#9467bd']);
        });

        it('ordinal', function () {
            chart.ordinalColors(['red','green','blue']);
            expect(colorTest(chart,domain)).toEqual(['red','green','blue','red','green']);
        });

        it('linear', function () {
            // GIGO: mapping ordinal domain to linear scale is nonsensical
            // actually it gets scaled to NaN and then d3 corrects it
            chart.linearColors(['#FF0000','#00FF00']);
            expect(colorTest(chart,domain)).toEqual(['#000000', '#000000', '#000000', '#000000', '#000000']);
        });
    });
    describe('with numeric domain' , function () {
        var chart, domain, test;

        beforeEach(function () {
            chart = dc.colorChart({});
            chart.colorAccessor(identity);
            domain = [1,100];
            test = [0,1,50,100,101,1];
        });

        it('default', function () {
            expect(colorTest(chart,domain,test)).toEqual(['#9ecae1','#3182bd','#c6dbef','#6baed6','#e6550d','#3182bd']);
        });

        it('custom', function () {
            chart.colors(d3.scale.category10());
            expect(colorTest(chart,domain,test)).toEqual(['#2ca02c', '#1f77b4', '#d62728', '#ff7f0e', '#9467bd', '#1f77b4']);
        });

        it('ordinal', function () {
            chart.ordinalColors(['red','green','blue']);
            expect(colorTest(chart,domain,test)).toEqual(['blue', 'red', 'red', 'green', 'green', 'red']);
        });

        it('linear', function () {
            chart.linearColors(['#4575b4','#ffffbf']);
            expect(colorTest(chart,domain,test)).toEqual(['#4773b3', '#4575b4', '#4dc6c1', '#ffffbf', '#ffffc0', '#4575b4']);
        });
    });
    describe('calculateColorDomain' , function () {
        var chart;

        beforeEach(function () {
            var data = crossfilter(loadDateFixture());
            var valueDimension = data.dimension(function (d) {
                return d.value;
            });
            var valueGroup = valueDimension.group();
            chart = dc.colorChart(dc.baseChart({}))
                .colorAccessor(function (d) {return d.value;})
                .group(valueGroup);
        });

        it('check domain', function () {
            chart.calculateColorDomain();
            expect(chart.colorDomain()).toEqual([1,3]);
        });
    });
});

