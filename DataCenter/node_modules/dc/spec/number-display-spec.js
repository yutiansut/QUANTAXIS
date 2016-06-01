/* global appendChartID, loadDateFixture */
describe('dc.numberDisplay', function () {
    var data, meanGroup;
    var countryDimension;
    function average (d) {
        return d.n ? d.tot / d.n : 0;
    }

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        var groupAll = data.groupAll();
        meanGroup = groupAll.reduce(
            function (p, v) {
                ++p.n;
                p.tot += +v.value;
                return p;
            },
            function (p, v) {
                --p.n;
                p.tot -= +v.value;
                return p;
            },
            function () { return {n: 0,tot: 0}; }
        );
        countryDimension = data.dimension(function (d) {
            return d.countrycode;
        });
        countryDimension.filter('CA');
    });

    function buildChart (id) {
        var chart = dc.numberDisplay(id)
                .transitionDuration(0)
                .group(meanGroup)
                .formatNumber(d3.format('.3s'))
                .valueAccessor(average);
        chart.render();
        d3.timer.flush();
        return chart;
    }

    describe('Empty Div', function () {
        var chart;
        beforeEach(function () {
            var id = 'empty-div';
            appendChartID(id);
            chart = buildChart('#' + id);
        });
        it('should generate something', function () {
            expect(chart).not.toBeNull();
        });
        it('should be registered', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });
        it('should return a value', function () {
            expect(chart.value()).toEqual(38.5);
        });
        it('should have text value in child', function () {
            expect(chart.select('span.number-display').text()).toEqual('38.5');
        });
        describe('redraw', function () {
            beforeEach(function () {
                countryDimension.filterAll();
                chart.redraw();
                d3.timer.flush();
            });
            it('should update value', function () {
                expect(chart.select('span.number-display').text()).toEqual('41.8');
            });
        });
        describe('html with one, some and none', function () {
            beforeEach(function () {
                chart.html({one: '%number number',none: 'no number',some: '%number numbers'});
                chart.redraw();
                d3.timer.flush();
            });
            it('should use some for some', function () {
                expect(chart.select('span.number-display').text()).toEqual('38.5 numbers');
            });
        });
        describe('html with one, some and none', function () {
            beforeEach(function () {
                chart.html({one: '%number number',none: 'no number',some: '%number numbers'});
                chart.valueAccessor(function (d) {return 1;});
                chart.redraw();
                d3.timer.flush();
            });
            it('should use one for one', function () {
                expect(chart.select('span.number-display').text()).toEqual('1.00 number');
            });
        });
        describe('html with one, some and none', function () {
            beforeEach(function () {
                chart.html({one: '%number number',none: 'no number',some: '%number numbers'});
                chart.valueAccessor(function (d) {return 0;});
                chart.redraw();
                d3.timer.flush();
            });
            it('should use zero for zero', function () {
                expect(chart.select('span.number-display').text()).toEqual('no number');
            });
        });
        describe('html with just one', function () {
            beforeEach(function () {
                chart.html({one: '%number number'});
                chart.redraw();
                d3.timer.flush();
            });
            it('should use one for showing some', function () {
                expect(chart.select('span.number-display').text()).toEqual('38.5 number');
            });
        });
        describe('html with just some', function () {
            beforeEach(function () {
                chart.html({some: '%number numbers'});
                chart.redraw();
                d3.timer.flush();
            });
            it('should use some for showing one', function () {
                expect(chart.select('span.number-display').text()).toEqual('38.5 numbers');
            });
        });
        describe('html with just none', function () {
            beforeEach(function () {
                chart.html({});
                chart.redraw();
                d3.timer.flush();
            });
            it('should just show the number in case of some and one', function () {
                expect(chart.select('span.number-display').text()).toEqual('38.5');
            });
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });
    describe('Div with embedded span', function () {
        var chart;
        beforeEach(function () {
            var id = 'full-div';
            var div = appendChartID(id);
            div.append('p').html('There are <span class="number-display">_</span> Total Widgets.');
            chart = buildChart('#' + id);
        });
        it('should have text value in child', function () {
            expect(chart.root().text()).toEqual('There are 38.5 Total Widgets.');
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });
    describe('Inline nonspan element' , function () {
        beforeEach(function () {
            var div = d3.select('body').append('div').attr('id','number-display-test-section');
            div.append('p').html('There are <em id="nonspan"></em> Total Widgets.');
            buildChart('#nonspan');
        });
        it('should have text value in child', function () {
            expect(d3.select('body').select('#number-display-test-section').html())
                .toMatch(new RegExp('<p>There are <em (?:id="nonspan" class="dc-chart"|class="dc-chart" id="nonspan")>' +
                    '<span class="number-display">38.5</span></em> Total Widgets.</p>'));
        });
        afterEach(function () {
            countryDimension.filterAll();
            d3.select('#number-display-test-section').remove();
        });
    });
});
