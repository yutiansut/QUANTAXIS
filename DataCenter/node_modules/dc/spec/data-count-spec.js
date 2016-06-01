/* global appendChartID, loadDateFixture */
describe('dc.dataCount', function () {
    var data, countryDimension, groupAll;
    var chart;
    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        groupAll = data.groupAll();
        countryDimension = data.dimension(function (d) {
            return d.countrycode;
        });
        countryDimension.filter('CA');
    });
    function buildChart (id) {
        var chart = dc.dataCount('#' + id)
            .transitionDuration(0)
            .dimension(data)
            .group(groupAll);
        chart.render();
        d3.timer.flush();
        return chart;
    }
    describe('creation', function () {
        beforeEach(function () {
            var id = 'data-count';
            var div = appendChartID(id);
            div.append('span').attr('class', 'filter-count');
            div.append('span').attr('class', 'total-count');
            chart = buildChart(id);
        });
        it('should generate something', function () {
            expect(chart).not.toBeNull();
        });
        it('should be registered', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });
        it('should fill in the total count', function () {
            expect(chart.select('span.total-count').text()).toEqual('10');
        });
        it('should fill in the filter count', function () {
            expect(chart.select('span.filter-count').text()).toEqual('2');
        });
        describe('redraw', function () {
            beforeEach(function () {
                countryDimension.filterAll();
                chart.redraw();
                return chart;
            });
            it('should fill in the updated total count', function () {
                expect(chart.select('span.total-count').text()).toEqual('10');
            });
            it('should fill in the updated filter count', function () {
                expect(chart.select('span.filter-count').text()).toEqual('10');
            });
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });

    describe('creation with html attribute', function () {
        beforeEach(function () {
            var id = 'data-count';
            var div = appendChartID(id);
            div.append('span').attr('class', 'filter-count');
            div.append('span').attr('class', 'total-count');
            chart = buildChart(id);
            chart.html({some: '%filter-count selected from %total-count',all: 'All Records Selected'});
            chart.redraw();
        });
        it('should generate something', function () {
            expect(chart).not.toBeNull();
        });
        it('should be registered', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });
        it('should fill the element replacing %filter-count and %total-count', function () {
            expect(chart.root().text()).toEqual('2 selected from 10');
        });
        describe('when all selected', function () {
            beforeEach(function () {
                countryDimension.filterAll();
                chart.redraw();
                return chart;
            });
            it('should use html.all', function () {
                expect(chart.root().text()).toEqual('All Records Selected');
            });
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });

    describe('creation with just html.some attribute', function () {
        beforeEach(function () {
            var id = 'data-count';
            var div = appendChartID(id);
            div.append('span').attr('class', 'filter-count');
            div.append('span').attr('class', 'total-count');
            chart = buildChart(id);
            chart.html({some: '%filter-count selected from %total-count'});
            chart.redraw();
        });
        it('should fill the element replacing %filter-count and %total-count', function () {
            expect(chart.root().text()).toEqual('2 selected from 10');
        });
        describe('when all selected', function () {
            beforeEach(function () {
                countryDimension.filterAll();
                chart.redraw();
                return chart;
            });
            it('should use html.some for all', function () {
                expect(chart.root().text()).toEqual('10 selected from 10');
            });
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });

    describe('creation with just html.all attribute', function () {
        beforeEach(function () {
            var id = 'data-count';
            var div = appendChartID(id);
            div.append('span').attr('class', 'filter-count');
            div.append('span').attr('class', 'total-count');
            chart = buildChart(id);
            chart.html({all: 'All Records Selected'});
            chart.redraw();
        });
        it('should fill in the total count', function () {
            expect(chart.select('span.total-count').text()).toEqual('10');
        });
        it('should fill in the filter count', function () {
            expect(chart.select('span.filter-count').text()).toEqual('2');
        });
        describe('when all selected', function () {
            beforeEach(function () {
                countryDimension.filterAll();
                chart.redraw();
                return chart;
            });
            it('should use html.all for all', function () {
                expect(chart.root().text()).toEqual('All Records Selected');
            });
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });

    describe('creation with formatNumber attribute', function () {
        beforeEach(function () {
            var id = 'data-count';
            var div = appendChartID(id);
            div.append('span').attr('class', 'filter-count');
            div.append('span').attr('class', 'total-count');
            chart = buildChart(id);
            chart.formatNumber(d3.format('04.1g'));
            chart.redraw();
        });
        it('should generate something', function () {
            expect(chart).not.toBeNull();
        });
        it('should be registered', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });
        it('should fill in the formatted total count', function () {
            expect(chart.select('span.total-count').text()).toEqual('1e+1');
        });
        it('should fill in the formatted filter count', function () {
            expect(chart.select('span.filter-count').text()).toEqual('0002');
        });
        afterEach(function () {
            countryDimension.filterAll();
        });
    });

});
