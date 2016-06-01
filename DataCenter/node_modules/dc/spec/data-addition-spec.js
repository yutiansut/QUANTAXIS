/* global appendChartID, loadDateFixture, loadDateFixture2, makeDate */
describe('Dynamic data addition in crossfilter', function () {
    var width = 200;
    var height = 200;
    var radius = 100;
    var baseData, moreData;

    beforeEach(function () {
        baseData = crossfilter(loadDateFixture());
        moreData = loadDateFixture2();
    });

    function occurrences (str, value) {
        return (str.split(value)).length - 1;
    }

    describe('pie chart slice addition', function () {
        var valueDimension, valueGroup;
        var chart;
        function buildPieChart (id) {
            var div = appendChartID(id);
            div.append('a').attr('class', 'reset').style('display', 'none');
            div.append('span').attr('class', 'filter').style('display', 'none');
            var chart = dc.pieChart('#' + id);
            chart.dimension(valueDimension).group(valueGroup)
                .width(width)
                .height(height)
                .radius(radius)
                .transitionDuration(0);
            chart.render();
            baseData.add(moreData);
            chart.expireCache();
            return chart;
        }
        beforeEach(function () {
            valueDimension = baseData.dimension(function (d) {
                return d.value;
            });
            valueGroup = valueDimension.group();
            chart = buildPieChart('pie-chart');
            chart.redraw();
        });
        it('slice g should be created with class', function () {
            expect(chart.selectAll('svg g g.pie-slice').data().length).toEqual(7);
        });
        it('slice path should be created', function () {
            expect(chart.selectAll('svg g g.pie-slice path').data().length).toEqual(7);
        });
        it('default function should be used to dynamically generate label', function () {
            expect(d3.select(chart.selectAll('text.pie-slice')[0][0]).text()).toEqual('11');
        });
        it('pie chart slices should be in numerical order', function () {
            expect(chart.selectAll('text.pie-slice').data().map(function (slice) { return slice.data.key; }))
                .toEqual(['11','22','33','44','55','66','76']);
        });
        it('default function should be used to dynamically generate title', function () {
            expect(d3.select(chart.selectAll('g.pie-slice title')[0][0]).text()).toEqual('11: 1');
        });
        afterEach(function () {
            valueDimension.filterAll();
        });
    });
    describe('line chart segment addition', function () {
        var timeDimension, timeGroup;
        var chart;
        function buildLineChart (id) {
            appendChartID(id);
            var chart = dc.lineChart('#' + id);
            chart.dimension(timeDimension).group(timeGroup)
                .width(width).height(height)
                .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]))
                .transitionDuration(0)
                .xUnits(d3.time.days.utc)
                .brushOn(false)
                .renderArea(true)
                .renderTitle(true);
            chart.render();
            baseData.add(moreData);
            chart.expireCache();
            return chart;
        }
        beforeEach(function () {
            timeDimension = baseData.dimension(function (d) {
                return d.dd;
            });
            timeGroup = timeDimension.group();
            chart = buildLineChart('line-chart');
            chart.render();
        });
        it('number of dots should equal the size of the group', function () {
            expect(chart.selectAll('circle.dot')[0].length).toEqual(timeGroup.size());
        });
        it('number of line segments should equal the size of the group', function () {
            var path = chart.selectAll('path.line').attr('d');
            expect(occurrences(path, 'L') + 1).toEqual(timeGroup.size());
        });
        it('number of area segments should equal twice the size of the group', function () {
            var path = chart.selectAll('path.area').attr('d');
            expect(occurrences(path, 'L') + 1).toEqual(timeGroup.size() * 2);
        });

        describe('resetting line chart with fewer data points', function () {
            beforeEach(function () {
                var chart = buildLineChart('stackable-line-chart');
                chart.render();

                timeDimension.filterAll();
                baseData.remove();
                baseData.add(moreData);
                chart.render();
            });

            it('it should not contain stale data points', function () {
                expect(chart.data()[0].values.length).toEqual(2);
            });
        });

        afterEach(function () {
            timeDimension.filterAll();
        });
    });
});
