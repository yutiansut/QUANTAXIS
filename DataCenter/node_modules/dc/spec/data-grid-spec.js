/* global appendChartID, loadDateFixture */
describe('dc.dataGrid', function () {
    var id, chart, data;
    var dateFixture;
    var dimension;
    var countryDimension;

    beforeEach(function () {
        dateFixture = loadDateFixture();
        data = crossfilter(dateFixture);
        dimension = data.dimension(function (d) {
            return d3.time.day.utc(d.dd);
        });
        countryDimension = data.dimension(function (d) {
            return d.countrycode;
        });

        id = 'data-grid';
        appendChartID(id);
        chart = dc.dataGrid('#' + id)
            .dimension(dimension)
            .group(function (d) {
                return 'Data Grid';
            })
            .transitionDuration(0)
            .size(3)
            .sortBy(function (d) {return d.id;})
            .order(d3.descending)
            .html(function (d) {
                return '<div id=\'id_' + d.id + '\' class=\'' + d.countrycode + ' ' + d.region + '\'>' + d.state + ':' + d.value + '</div>';
            });
        chart.render();
    });

    describe('creation', function () {
        it('generates something', function () {
            expect(chart).not.toBeNull();
        });
        it('registers', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });
        it('sets size', function () {
            expect(chart.size()).toEqual(3);
        });
        it('sets sortBy', function () {
            expect(chart.sortBy()).not.toBeNull();
        });
        it('sets order', function () {
            expect(chart.order()).toBe(d3.descending);
        });
        it('sets the group label', function () {
            expect(chart.selectAll('.dc-grid-group h1.dc-grid-label')[0][0].innerHTML).toEqual('Data Grid');
        });
        it('creates id div', function () {
            expect(chart.selectAll('.dc-grid-item div#id_9')[0].length).toEqual(1);
            expect(chart.selectAll('.dc-grid-item div#id_8')[0].length).toEqual(1);
            expect(chart.selectAll('.dc-grid-item div#id_3')[0].length).toEqual(1);
        });
        it('creates div content', function () {
            expect(chart.selectAll('.dc-grid-item div')[0][0].innerHTML).toEqual('Mississippi:44');
            expect(chart.selectAll('.dc-grid-item div')[0][1].innerHTML).toEqual('Mississippi:33');
            expect(chart.selectAll('.dc-grid-item div')[0][2].innerHTML).toEqual('Delaware:33');
        });
    });

    describe('slicing entries', function () {
        beforeEach(function () {
            chart.beginSlice(1);
            chart.redraw();
        });

        it('slice beginning', function () {
            expect(chart.selectAll('.dc-grid-item')[0].length).toEqual(2);
        });

        it('slice beginning and end', function () {
            chart.endSlice(2);
            chart.redraw();

            expect(chart.selectAll('.dc-grid-item')[0].length).toEqual(1);
        });
    });

    describe('external filter', function () {
        beforeEach(function () {
            countryDimension.filter('CA');
            chart.redraw();
        });
        it('renders only filtered data set', function () {
            expect(chart.selectAll('.dc-grid-item div')[0].length).toEqual(2);
        });
        it('renders the correctly filtered records', function () {
            expect(chart.selectAll('.dc-grid-item div')[0][0].innerHTML).toEqual('Ontario:22');
            expect(chart.selectAll('.dc-grid-item div')[0][1].innerHTML).toEqual('Ontario:55');
        });
    });

    describe('renderlet', function () {
        var derlet;
        beforeEach(function () {
            derlet = jasmine.createSpy('renderlet', function (chart) {
                chart.selectAll('.dc-grid-label').text('changed');
            });
            derlet.and.callThrough();
            chart.on('renderlet', derlet);
        });
        it('custom renderlet should be invoked with render', function () {
            chart.render();
            expect(chart.selectAll('.dc-grid-label').text()).toEqual('changed');
            expect(derlet).toHaveBeenCalled();
        });
        it('custom renderlet should be invoked with redraw', function () {
            chart.redraw();
            expect(chart.selectAll('.dc-grid-label').text()).toEqual('changed');
            expect(derlet).toHaveBeenCalled();
        });
    });

    afterEach(function () {
        dimension.filterAll();
        countryDimension.filterAll();
    });
});

