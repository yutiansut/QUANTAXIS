/* global appendChartID, loadColorFixture, loadColorFixture2 */
describe('dc.heatmap', function () {
    var id, data, dimension, group, chart, chartHeight, chartWidth;

    beforeEach(function () {
        data = crossfilter(loadColorFixture());
        dimension = data.dimension(function (d) { return [+d.colData, +d.rowData]; });
        group = dimension.group().reduceSum(function (d) { return +d.colorData; });

        chartHeight = 210;
        chartWidth = 210;

        id = 'heatmap-chart';
        appendChartID(id);
        chart = dc.heatMap('#' + id);

        chart
            .dimension(dimension)
            .group(group)
            .keyAccessor(function (d) { return d.key[0]; })
            .valueAccessor(function (d) { return d.key[1]; })
            .colorAccessor(function (d) { return d.value; })
            .colors(['#000001', '#000002', '#000003', '#000004'])
            .title(function (d) {return d.key + ': ' + d.value; })
            .height(chartHeight)
            .width(chartWidth)
            .transitionDuration(0)
            .margins({top: 5, right: 5, bottom: 5, left: 5})
            .calculateColorDomain();

    });

    describe('rendering the heatmap', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create svg', function () {
            expect(chart.svg()).not.toBeNull();
        });

        it('should transform the graph position using the graph margins', function () {
            expect(chart.select('g.heatmap').attr('transform')).toMatchTranslate(5,5);
        });

        it('should position the heatboxes in a matrix', function () {
            var heatBoxes = chart.selectAll('rect.heat-box');

            expect(+heatBoxes[0][0].getAttribute('x')).toEqual(0);
            expect(+heatBoxes[0][0].getAttribute('y')).toEqual(100);

            expect(+heatBoxes[0][1].getAttribute('x')).toEqual(0);
            expect(+heatBoxes[0][1].getAttribute('y')).toEqual(0);

            expect(+heatBoxes[0][2].getAttribute('x')).toEqual(100);
            expect(+heatBoxes[0][2].getAttribute('y')).toEqual(100);

            expect(+heatBoxes[0][3].getAttribute('x')).toEqual(100);
            expect(+heatBoxes[0][3].getAttribute('y')).toEqual(0);
        });

        it('should color heatboxes using the provided color option', function () {
            var heatBoxes = chart.selectAll('rect.heat-box');

            expect(heatBoxes[0][0].getAttribute('fill')).toEqual('#000001');
            expect(heatBoxes[0][1].getAttribute('fill')).toEqual('#000002');
            expect(heatBoxes[0][2].getAttribute('fill')).toEqual('#000003');
            expect(heatBoxes[0][3].getAttribute('fill')).toEqual('#000004');
        });

        it('should size heatboxes based on the size of the matrix', function () {
            chart.selectAll('rect.heat-box').each(function () {
                expect(+this.getAttribute('height')).toEqual(100);
                expect(+this.getAttribute('width')).toEqual(100);
            });
        });

        it('should position the y-axis labels with their associated rows', function () {
            var yaxisTexts = chart.selectAll('.rows.axis text');
            expect(+yaxisTexts[0][0].getAttribute('y')).toEqual(150);
            expect(+yaxisTexts[0][0].getAttribute('x')).toEqual(0);
            expect(+yaxisTexts[0][1].getAttribute('y')).toEqual(50);
            expect(+yaxisTexts[0][1].getAttribute('x')).toEqual(0);
        });

        it('should have labels on the y-axis corresponding to the row values', function () {
            var yaxisTexts = chart.selectAll('.rows.axis text');
            expect(yaxisTexts[0][0].textContent).toEqual('1');
            expect(yaxisTexts[0][1].textContent).toEqual('2');
        });

        it('should position the x-axis labels with their associated columns', function () {
            var xaxisTexts = chart.selectAll('.cols.axis text');
            expect(+xaxisTexts[0][0].getAttribute('y')).toEqual(200);
            expect(+xaxisTexts[0][0].getAttribute('x')).toEqual(50);
            expect(+xaxisTexts[0][1].getAttribute('y')).toEqual(200);
            expect(+xaxisTexts[0][1].getAttribute('x')).toEqual(150);
        });

        it('should have labels on the x-axis corresponding to the row values', function () {
            var xaxisTexts = chart.selectAll('.cols.axis text');
            expect(xaxisTexts[0][0].textContent).toEqual('1');
            expect(xaxisTexts[0][1].textContent).toEqual('2');
        });

        describe('with custom labels', function () {
            beforeEach(function () {
                chart.colsLabel(function (x) { return 'col ' + x;})
                    .rowsLabel(function (x) { return 'row ' + x;})
                    .redraw();
            });
            it('should display the custom labels on the x axis', function () {
                var xaxisTexts = chart.selectAll('.cols.axis text');
                expect(xaxisTexts[0][0].textContent).toEqual('col 1');
                expect(xaxisTexts[0][1].textContent).toEqual('col 2');
            });
            it('should display the custom labels on the y axis', function () {
                var yaxisTexts = chart.selectAll('.rows.axis text');
                expect(yaxisTexts[0][0].textContent).toEqual('row 1');
                expect(yaxisTexts[0][1].textContent).toEqual('row 2');
            });
        });

        describe('box radius', function () {
            it('should default the x', function () {
                chart.select('rect.heat-box').each(function () {
                    expect(this.getAttribute('rx')).toBe('6.75');
                });
            });

            it('should default the y', function () {
                chart.select('rect.heat-box').each(function () {
                    expect(this.getAttribute('ry')).toBe('6.75');
                });
            });

            it('should set the radius to an overridden x', function () {
                chart.xBorderRadius(7);
                chart.render();

                chart.select('rect.heat-box').each(function () {
                    expect(this.getAttribute('rx')).toBe('7');
                });
            });

            it('should set the radius to an overridden y', function () {
                chart.yBorderRadius(7);
                chart.render();

                chart.select('rect.heat-box').each(function () {
                    expect(this.getAttribute('ry')).toBe('7');
                });
            });
        });

    });

    describe('change crossfilter', function () {
        var data2, dimension2, group2, originalDomain, newDomain;

        var reduceDimensionValues = function (dimension) {
            return dimension.top(Infinity).reduce(function (p, d) {
                p.cols.add(d.colData);
                p.rows.add(d.rowData);
                return p;
            }, {cols: d3.set(), rows: d3.set()});
        };

        beforeEach(function () {
            data2 = crossfilter(loadColorFixture2());
            dimension2 = data2.dimension(function (d) { return [+d.colData, +d.rowData]; });
            group2 = dimension2.group().reduceSum(function (d) { return +d.colorData; });
            originalDomain = reduceDimensionValues(dimension);
            newDomain = reduceDimensionValues(dimension2);

            chart.dimension(dimension2).group(group2);
            chart.render();
            chart.dimension(dimension).group(group);
            chart.redraw();
        });

        it('should have the correct number of columns', function () {
            chart.selectAll('.box-group').each(function (d) {
                expect(originalDomain.cols.has(d.key[0])).toBeTruthy();
            });

            chart.selectAll('.cols.axis text').each(function (d) {
                expect(originalDomain.cols.has(d)).toBeTruthy();
            });
        });

        it('should have the correct number of rows', function () {
            chart.selectAll('.box-group').each(function (d) {
                expect(originalDomain.rows.has(d.key[1])).toBeTruthy();
            });

            chart.selectAll('.rows.axis text').each(function (d) {
                expect(originalDomain.rows.has(d)).toBeTruthy();
            });
        });
    });

    describe('indirect filtering', function () {
        var dimension2, group2;
        beforeEach(function () {
            dimension2 = data.dimension(function (d) { return +d.colorData; });
            group2 = dimension2.group().reduceSum(function (d) { return +d.colorData; });

            chart.dimension(dimension).group(group);
            chart.render();
            dimension2.filter('3');
            chart.redraw();
        });

        it('should update the title of the boxes', function () {
            var titles = chart.selectAll('.box-group title');
            var expected = ['1,1: 0', '1,2: 0', '2,1: 6', '2,2: 0'];
            titles.each(function (d) {
                expect(this.textContent).toBe(expected.shift());
            });
        });
    });

    describe('filtering', function () {
        var filterX, filterY;
        var otherDimension;

        beforeEach(function () {
            filterX = Math.ceil(Math.random() * 2);
            filterY = Math.ceil(Math.random() * 2);
            otherDimension = data.dimension(function (d) { return +d.colData; });
            chart.render();
        });

        function clickCellOnChart (chart, x, y) {
            var oneCell = chart.selectAll('.box-group').filter(function (d) {
                return d.key[0] === x && d.key[1] === y;
            });
            oneCell.select('rect').on('click')(oneCell.datum());
            return oneCell;
        }

        it('cells should have the appropriate class', function () {
            clickCellOnChart(chart, filterX, filterY);
            chart.selectAll('.box-group').each(function (d) {
                var cell = d3.select(this);
                if (d.key[0] === filterX && d.key[1] === filterY) {
                    expect(cell.classed('selected')).toBeTruthy();
                    expect(chart.hasFilter(d.key)).toBeTruthy();
                } else {
                    expect(cell.classed('deselected')).toBeTruthy();
                    expect(chart.hasFilter(d.key)).toBeFalsy();
                }
            });
        });

        it('should keep all data points for that cell', function () {
            var otherGroup = otherDimension.group().reduceSum(function (d) { return +d.colorData; });
            var otherChart = dc.baseChart({}).dimension(otherDimension).group(otherGroup);

            otherChart.render();
            var clickedCell = clickCellOnChart(chart, filterX, filterY);
            expect(otherChart.data()[filterX - 1].value).toEqual(clickedCell.datum().value);
        });

        it('should be able to clear filters by filtering with null', function () {
            clickCellOnChart(chart, filterX, filterY);
            expect(otherDimension.top(Infinity).length).toBe(2);
            chart.filter(null);
            expect(otherDimension.top(Infinity).length).toBe(8);
        });
    });

    describe('click events', function () {
        beforeEach(function () {
            chart.render();
        });
        it('should toggle a filter for the clicked box', function () {
            chart.selectAll('.box-group').each(function (d) {
                var cell = d3.select(this).select('rect');
                cell.on('click')(d);
                expect(chart.hasFilter(d.key)).toBeTruthy();
                cell.on('click')(d);
                expect(chart.hasFilter(d.key)).toBeFalsy();
            });
        });
        describe('on axis labels', function () {
            function assertOnlyThisAxisIsFiltered (chart, axis, value) {
                chart.selectAll('.box-group').each(function (d) {
                    if (d.key[axis] === value) {
                        expect(chart.hasFilter(d.key)).toBeTruthy();
                    } else {
                        expect(chart.hasFilter(d.key)).toBeFalsy();
                    }
                });
            }

            describe('with nothing previously filtered', function () {
                it('should filter all cells on that axis', function () {
                    chart.selectAll('.cols.axis text').each(function (d) {
                        var axisLabel = d3.select(this);
                        axisLabel.on('click')(d);
                        assertOnlyThisAxisIsFiltered(chart, 0, d);
                        axisLabel.on('click')(d);
                    });
                    chart.selectAll('.rows.axis text').each(function (d) {
                        var axisLabel = d3.select(this);
                        axisLabel.on('click')(d);
                        assertOnlyThisAxisIsFiltered(chart, 1, d);
                        axisLabel.on('click')(d);
                    });
                });
            });
            describe('with one cell on that axis already filtered', function () {
                it('should filter all cells on that axis (and the original cell should remain filtered)', function () {
                    var boxes = chart.selectAll('.box-group');
                    var box = d3.select(boxes[0][Math.floor(Math.random() * boxes.length)]);

                    box.select('rect').on('click')(box.datum());

                    expect(chart.hasFilter(box.datum().key)).toBeTruthy();

                    var xVal = box.datum().key[0];

                    var columns = chart.selectAll('.cols.axis text');
                    var column = columns.filter(function (columnData) {
                        return columnData === xVal;
                    });

                    column.on('click')(column.datum());

                    assertOnlyThisAxisIsFiltered(chart, 0, xVal);

                    column.on('click')(column.datum());
                });
            });
            describe('with all cells on that axis already filtered', function () {
                it('should remove all filters on that axis', function () {
                    var xVal = 1;
                    chart.selectAll('.box-group').each(function (d) {
                        var box = d3.select(this);
                        if (d.key[0] === xVal) {
                            box.select('rect').on('click')(box.datum());
                        }
                    });

                    assertOnlyThisAxisIsFiltered(chart, 0, xVal);

                    var columns = chart.selectAll('.cols.axis text');
                    var column = columns.filter(function (columnData) {
                        return columnData === xVal;
                    });

                    column.on('click')(column.datum());

                    chart.select('.box-group').each(function (d) {
                        expect(chart.hasFilter(d.key)).toBeFalsy();
                    });
                });
            });
        });
    });
});
