/* global appendChartID, coordsFromTranslate, loadDateFixture */
describe('dc.legend', function () {
    var id, chart, dateDimension, dateValueSumGroup, dateIdSumGroup;

    beforeEach(function () {
        var data = crossfilter(loadDateFixture());
        dateDimension = data.dimension(function (d) { return d3.time.day.utc(d.dd); });
        dateValueSumGroup = dateDimension.group().reduceSum(function (d) { return d.value; });
        dateIdSumGroup = dateDimension.group().reduceSum(function (d) { return d.id; });

        id = 'legend-chart';
        appendChartID(id);
        chart = dc.lineChart('#' + id);

        chart
            .dimension(dateDimension)
            .group(dateIdSumGroup, 'Id Sum')
            .stack(dateValueSumGroup, 'Value Sum')
            .stack(dateValueSumGroup, 'Fixed', function () {})
            .x(d3.time.scale.utc().domain([new Date(2012, 4, 20), new Date(2012, 7, 15)]))
            .legend(dc.legend().x(400).y(10).itemHeight(13).gap(5));
    });

    describe('rendering the legend', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should generate a legend', function () {
            expect(chart.select('g.dc-legend').empty()).toBeFalsy();
        });

        it('should place the legend using the provided x and y values', function () {
            expect(chart.select('g.dc-legend').attr('transform')).toMatchTranslate(400,10);
        });

        it('should generate a legend item for each stacked line', function () {
            expect(chart.select('g.dc-legend').selectAll('g.dc-legend-item').size()).toBe(3);
        });

        describe('without .horizontal(true)', function () {
            it('should place legend items vertically', function () {
                expect(coordsFromTranslate(legendItem(0).attr('transform')).y).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(1).attr('transform')).y).toBeWithinDelta(18, 2);
                expect(coordsFromTranslate(legendItem(2).attr('transform')).y).toBeWithinDelta(36, 4);
            });
        });

        describe('with .horizontal(true)', function () {
            beforeEach(function () {
                chart.legend(dc.legend().horizontal(true));
                chart.render();
            });

            it('should place legend items horizontally', function () {
                expect(coordsFromTranslate(legendItem(0).attr('transform')).x).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(1).attr('transform')).x).toBeWithinDelta(65, 5);
                expect(coordsFromTranslate(legendItem(2).attr('transform')).x).toBeWithinDelta(155, 15);
            });
        });

        describe('with .horizontal(true) and defined legendWidth and itemWidth', function () {
            beforeEach(function () {
                chart.legend(dc.legend().horizontal(true).legendWidth(60).itemWidth(30));
                chart.render();
            });

            it('should place legend items in two columns. third item is new row', function () {
                expect(coordsFromTranslate(legendItem(0).attr('transform')).x).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(1).attr('transform')).x).toBeWithinDelta(30, 5);
                expect(coordsFromTranslate(legendItem(2).attr('transform')).x).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(0).attr('transform')).y).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(1).attr('transform')).y).toBeWithinDelta(0, 1);
                expect(coordsFromTranslate(legendItem(2).attr('transform')).y).toBeWithinDelta(13, 5);
            });
        });

        describe('with .autoItemWidth not called', function () {
            beforeEach(function () {
                chart.legend(dc.legend());
            });

            it('_autoItemWidth should be false', function () {
                expect(chart.legend().autoItemWidth()).toBe(false);
            });
        });

        describe('with .autoItemWidth(false)', function () {
            beforeEach(function () {
                chart.legend(dc.legend().autoItemWidth(false));
            });

            it('_autoItemWidth should be false', function () {
                expect(chart.legend().autoItemWidth()).toBe(false);
            });
        });

        describe('with .autoItemWidth(true)', function () {
            beforeEach(function () {
                chart.legend(dc.legend().autoItemWidth(true));
            });
            it('_autoItemWidth should be true', function () {
                expect(chart.legend().autoItemWidth()).toBe(true);
            });
        });

        describe('with .horizontal(true) and .autoItemWidth(true)', function () {

            var
                autoWidthOffset1, fixedWidthOffset1,
                autoWidthOffset2, fixedWidthOffset2;

            beforeEach(function () {
                chart.legend(dc.legend().horizontal(true).itemWidth(30).autoItemWidth(false));
                chart.render();
                fixedWidthOffset1 = coordsFromTranslate(legendItem(1).attr('transform')).x;
                fixedWidthOffset2 = coordsFromTranslate(legendItem(2).attr('transform')).x;
                chart.legend(dc.legend().horizontal(true).itemWidth(30).autoItemWidth(true));
                chart.render();
                autoWidthOffset1  = coordsFromTranslate(legendItem(1).attr('transform')).x;
                autoWidthOffset2  = coordsFromTranslate(legendItem(2).attr('transform')).x;
            });

            it('autoWidth x offset should be greater than fixedWidth x offset for some legend items', function () {
                expect(autoWidthOffset1).toBeGreaterThan(fixedWidthOffset1);
                expect(autoWidthOffset2).toBeGreaterThan(fixedWidthOffset2);
            });
        });

        it('should generate legend item boxes', function () {
            expect(legendIcon(0).attr('width')).toBeWithinDelta(13,2);
            expect(legendIcon(0).attr('height')).toBeWithinDelta(13, 2);
        });

        it('should color the legend item boxes using the chart line colors', function () {
            expect(legendIcon(0).attr('fill')).toBe('#1f77b4');
            expect(legendIcon(1).attr('fill')).toBe('#ff7f0e');
            expect(legendIcon(2).attr('fill')).toBe('#2ca02c');
        });

        it('should generate a legend label for each chart line', function () {
            expect(chart.selectAll('g.dc-legend g.dc-legend-item text').size()).toBe(3);
        });

        it('should position the legend labels', function () {
            expect(legendLabel(0).attr('x')).toBeWithinDelta(15, 2);
            expect(legendLabel(0).attr('y')).toBeWithinDelta(13, 2);
            expect(legendLabel(1).attr('x')).toBeWithinDelta(15, 2);
            expect(legendLabel(1).attr('y')).toBeWithinDelta(13, 2);
            expect(legendLabel(2).attr('x')).toBeWithinDelta(15, 2);
            expect(legendLabel(2).attr('y')).toBeWithinDelta(13, 2);
        });

        it('should label the legend items with the names of their associated stacks', function () {
            expect(legendLabel(0).text()).toBe('Id Sum');
            expect(legendLabel(1).text()).toBe('Value Sum');
            expect(legendLabel(2).text()).toBe('Fixed');
        });

        it('not allow hiding stacks be default', function () {
            legendItem(0).on('click').call(legendItem(0)[0][0], legendItem(0).datum());
            expect(chart.selectAll('path.line').size()).toBe(3);
        });

        describe('with .legendText()', function () {
            beforeEach(function () {
                chart.legend(dc.legend().legendText(function (d, i) {
                    var _i = i + 1;

                    return _i + '. ' + d.name;
                }));
                chart.render();
            });

            it('should label the legend items with the names of their associated stacks', function () {
                expect(legendLabel(0).text()).toBe('1. Id Sum');
                expect(legendLabel(1).text()).toBe('2. Value Sum');
                expect(legendLabel(2).text()).toBe('3. Fixed');
            });
        });
    });

    describe('legends with dashed lines', function () {
        beforeEach(function () {
            id = 'legend-chart-dashed';
            appendChartID(id);
            chart = dc.compositeChart('#' + id);

            var subChart1 = dc.lineChart(chart);
            subChart1
                .dimension(dateDimension)
                .group(dateIdSumGroup, 'Id Sum')
                .dashStyle([10,1]);

            var subChart2 = dc.lineChart(chart);
            subChart2
                .dimension(dateDimension)
                .group(dateValueSumGroup, 'Value Sum')
                .dashStyle([2,1]);

            chart
                .x(d3.scale.linear().domain([0,20]))
                .legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
                .compose([subChart1, subChart2])
                .render();
        });

        it('should style legend line correctly', function () {
            expect(legendLine(0).attr('stroke-dasharray')).toEqualIntList('10,1');
            expect(legendLine(1).attr('stroke-dasharray')).toEqualIntList('2,1');
        });
    });

    describe('legends with hidable stacks', function () {
        beforeEach(function () {
            chart.hidableStacks(true).render();
        });

        describe('clicking on a legend item', function () {
            beforeEach(function () {
                legendItem(0).on('click').call(legendItem(0)[0][0], legendItem(0).datum());
            });

            it('should fade out the legend item', function () {
                expect(legendItem(0).classed('fadeout')).toBeTruthy();
            });

            it('should hide its associated stack', function () {
                expect(chart.selectAll('path.line').size()).toEqual(2);
            });

            it('disable hover highlighting for that legend item', function () {
                legendItem(0).on('mouseover')(legendItem(0).datum());
                expect(d3.select(chart.selectAll('path.line')[0][1]).classed('fadeout')).toBeFalsy();
            });

            describe('clicking on a faded out legend item', function () {
                beforeEach(function () {
                    legendItem(0).on('click').call(legendItem(0)[0][0], legendItem(0).datum());
                });

                it('should unfade the legend item', function () {
                    expect(legendItem(0).classed('fadeout')).toBeFalsy();
                });

                it('should unfade its associated stack', function () {
                    expect(chart.selectAll('path.line').size()).toEqual(3);
                });
            });
        });
    });

    function legendItem (n) {
        return d3.select(chart.selectAll('g.dc-legend g.dc-legend-item')[0][n]);
    }
    function legendLabel (n) {
        return d3.select(chart.selectAll('g.dc-legend g.dc-legend-item text')[0][n]);
    }
    function legendIcon (n) {
        return d3.select(chart.selectAll('g.dc-legend g.dc-legend-item rect')[0][n]);
    }
    function legendLine (n) {
        return d3.select(chart.selectAll('g.dc-legend g.dc-legend-item line')[0][n]);
    }
});

