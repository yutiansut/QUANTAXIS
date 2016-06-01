/* global appendChartID, loadDateFixture */
describe('dc.dataTable', function () {
    var id, chart, data;
    var dateFixture;
    var dimension;
    var countryDimension;
    var valueGroup;

    beforeEach(function () {
        dateFixture = loadDateFixture();
        data = crossfilter(dateFixture);
        dimension = data.dimension(function (d) {
            return d3.time.day.utc(d.dd);
        });
        countryDimension = data.dimension(function (d) {
            return d.countrycode;
        });
        valueGroup = function () {
                return 'Data Table';
            };

        id = 'data-table';
        appendChartID(id);
        chart = dc.dataTable('#' + id)
            .dimension(dimension)
            .group(valueGroup)
            .transitionDuration(0)
            .size(3)
            .sortBy(function (d) {return d.id;})
            .order(d3.descending)
            .columns(
                [function (d) {
                    return d.id;
                }, function (d) {
                    return d.status;
                }]
            );
    });

    describe('simple table', function () {
        beforeEach(function () {
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
            it('group should be set', function () {
                expect(chart.group()).toEqual(valueGroup);
            });
            it('group tr should not be undefined', function () {
                expect(typeof(chart.selectAll('tr.dc-table-group')[0][0])).not.toBe('undefined');
            });
            it('sets column span set on group tr', function () {
                expect(chart.selectAll('tr.dc-table-group td')[0][0].getAttribute('colspan')).toEqual('2');
            });
            it('creates id column', function () {
                expect(chart.selectAll('td._0')[0][0].innerHTML).toEqual('9');
                expect(chart.selectAll('td._0')[0][1].innerHTML).toEqual('8');
                expect(chart.selectAll('td._0')[0][2].innerHTML).toEqual('3');
            });
            it('creates status column', function () {
                expect(chart.selectAll('td._1')[0][0].innerHTML).toEqual('T');
                expect(chart.selectAll('td._1')[0][1].innerHTML).toEqual('F');
                expect(chart.selectAll('td._1')[0][2].innerHTML).toEqual('T');
            });
        });

        describe('slicing entries', function () {
            beforeEach(function () {
                chart.beginSlice(1);
                chart.redraw();
            });

            it('slice beginning', function () {
                expect(chart.selectAll('tr.dc-table-row')[0].length).toEqual(2);
            });

            it('slice beginning and end', function () {
                chart.endSlice(2);
                chart.redraw();

                expect(chart.selectAll('tr.dc-table-row')[0].length).toEqual(1);
            });
        });

        describe('external filter', function () {
            beforeEach(function () {
                countryDimension.filter('CA');
                chart.redraw();
            });
            it('renders only filtered data set', function () {
                expect(chart.selectAll('td._0')[0].length).toEqual(2);
            });
            it('renders the correctly filtered records', function () {
                expect(chart.selectAll('td._0')[0][0].innerHTML).toEqual('7');
                expect(chart.selectAll('td._0')[0][1].innerHTML).toEqual('5');
            });
        });

        describe('ascending order', function () {
            beforeEach(function () {
                chart.order(d3.ascending);
                chart.redraw();
            });
            it('uses dimension.bottom() instead of top()', function () {
                expect(chart.selectAll('td._0')[0][0].innerHTML).toEqual('1');
            });
        });
    });

    describe('renderlet', function () {
        var derlet;
        beforeEach(function () {
            derlet = jasmine.createSpy('renderlet', function (chart) {
                chart.selectAll('td.dc-table-label').text('changed');
            });
            derlet.and.callThrough();
            chart.on('renderlet', derlet);
        });
        it('custom renderlet should be invoked with render', function () {
            chart.render();
            expect(chart.selectAll('td.dc-table-label').text()).toEqual('changed');
            expect(derlet).toHaveBeenCalled();
        });
        it('custom renderlet should be invoked with redraw', function () {
            chart.redraw();
            expect(chart.selectAll('td.dc-table-label').text()).toEqual('changed');
            expect(derlet).toHaveBeenCalled();
        });
    });

    describe('specifying chart columns with label', function () {
        beforeEach(function () {
            chart.columns(['state']);
            chart.render();
        });
        it('should render value and capitalized header', function () {
            var cols = chart.selectAll('td.dc-table-column')[0].map(function (d) {return d.textContent;});
            var expected = ['Mississippi', 'Mississippi', 'Delaware'];
            expect(cols.length).toEqual(expected.length);
            expected.forEach(function (d) {
                expect(cols).toContain(d);
            });
            var colheader = chart.selectAll('th.dc-table-head')[0].map(function (d) {return d.textContent;});
            expect(colheader.length).toEqual(1);
            expect(colheader[0]).toEqual('State');

        });
    });
    describe('specifying chart columns with function', function () {
        beforeEach(function () {
            chart.columns([function (d) {return '' + d.id + 'test';}]);
            chart.render();
        });
        it('should render function result and no header', function () {
            var cols = chart.selectAll('td.dc-table-column')[0].map(function (d) {return d.textContent;});
            var expected = ['9test', '8test', '3test'];
            expect(cols.length).toEqual(expected.length);
            expected.forEach(function (d) {
                expect(cols).toContain(d);
            });
            var colheader = chart.selectAll('th.dc-table-head')[0].map(function (d) {return d.textContent;});
            expect(colheader.length).toEqual(0);
        });
    });
    describe('specifying chart columns with object', function () {
        beforeEach(function () {
            chart.columns([{
                label: 'Test ID',
                format: function (d) {
                    return 'test' + d.id;
                }
            }]);
            chart.render();
        });
        it('should produce correct table header with single column', function () {
            var thead = chart.selectAll('thead');
            expect(thead.length).toBe(1);
            var tr = thead.selectAll('tr');
            expect(tr.length).toBe(1);
            var colheader = tr.selectAll('th.dc-table-head')[0].map(function (d) {return d.textContent;});
            expect(colheader.length).toEqual(1);
            expect(colheader[0]).toEqual('Test ID');
        });

        it('should render correct values in rows', function () {
            var cols = chart.selectAll('td.dc-table-column')[0].map(function (d) {return d.textContent;});
            var expected = ['test9', 'test8', 'test3'];
            expect(cols.length).toEqual(expected.length);
            expected.forEach(function (d, i) {
                expect(cols[i]).toEqual(d);
            });
        });
    });

    describe('with existing table header', function () {
        beforeEach(function () {
            // add some garbage for table to replace
            d3.select('#data-table')
                .selectAll('thead').data([0]).enter().append('thead')
                .selectAll('tr').data([1,2]).enter().append('tr')
                .selectAll('th').data([1,2,3]).enter().append('th');
            chart.columns([{
                label: 'Test ID',
                format: function (d) {
                    return 'test' + d.id;
                }
            }]);
            chart.render();
        });
        it('should produce correct table header with single column', function () {
            var thead = chart.selectAll('thead');
            expect(thead.length).toBe(1);
            var tr = thead.selectAll('tr');
            expect(tr.length).toBe(1);
            var colheader = tr.selectAll('th.dc-table-head')[0].map(function (d) {return d.textContent;});
            expect(colheader.length).toEqual(1);
            expect(colheader[0]).toEqual('Test ID');
        });
    });

    describe('specifying showGroups as false', function () {
        beforeEach(function () {
            chart.showGroups(false);
            chart.render();
        });
        it('group tr should be undefined', function () {
            expect(typeof(chart.selectAll('tr.dc-table-group')[0][0])).toBe('undefined');
        });
    });

    afterEach(function () {
        dimension.filterAll();
        countryDimension.filterAll();
    });
});

