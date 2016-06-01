/* global appendChartID, loadDateFixture, makeDate */
describe('dc.compositeChart', function () {
    var id, chart, data, dateDimension, dateValueSumGroup, dateValueNegativeSumGroup,
        dateIdSumGroup, dateGroup;

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        dateDimension = data.dimension(function (d) { return d3.time.day.utc(d.dd); });
        dateValueSumGroup = dateDimension.group().reduceSum(function (d) { return d.value; });
        dateValueNegativeSumGroup = dateDimension.group().reduceSum(function (d) { return -d.value; });
        dateIdSumGroup = dateDimension.group().reduceSum(function (d) { return d.id; });
        dateGroup = dateDimension.group();

        id = 'composite-chart';
        appendChartID(id);

        chart = dc.compositeChart('#' + id);
        chart
            .dimension(dateDimension)
            .group(dateIdSumGroup)
            .width(500)
            .height(150)
            .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]))
            .transitionDuration(0)
            .xUnits(d3.time.days.utc)
            .shareColors(true)
            .compose([
                dc.barChart(chart)
                    .centerBar(true)
                    .group(dateValueSumGroup, 'Date Value Group Bar')
                    .gap(1),
                dc.lineChart(chart)
                    .group(dateIdSumGroup, 'Date ID Group')
                    .stack(dateValueSumGroup, 'Date Value Group Line 1')
                    .stack(dateValueSumGroup, 'Date Value Group Line 2')
                    .hidableStacks(true),
                dc.lineChart(chart)
                    .group(dateGroup, 'Date Group')
            ]);
    });

    it('should registered the chart with DC', function () {
        expect(dc.hasChart(chart)).toBeTruthy();
    });

    it('should set a dimension on the chart', function () {
        expect(chart.dimension()).toBe(dateDimension);
    });

    it('should set a group on the chart', function () {
        expect(chart.group()).toBe(dateIdSumGroup);
    });

    it('should set a width on the chart', function () {
        expect(chart.width()).toBe(500);
    });

    it('should set a height on the chart', function () {
        expect(chart.height()).toBe(150);
    });

    it('should have zero transition duration', function () {
        expect(chart.transitionDuration()).toBe(0);
    });

    it('should set the margins of the chart', function () {
        expect(chart.margins()).not.toBeNull();
    });

    it('should set a domain', function () {
        expect(chart.x()).toBeDefined();
    });

    it('should set the x domain to endpoint dates', function () {
        expect(chart.x().domain()[0].getTime()).toBe(makeDate(2012, 4, 20).getTime());
        expect(chart.x().domain()[1].getTime()).toBe(makeDate(2012, 7, 15).getTime());
    });

    it('should set the x units', function () {
        expect(chart.xUnits()).toBe(d3.time.days.utc);
    });

    it('should create the x axis', function () {
        expect(chart.xAxis()).not.toBeNull();
    });

    it('should create the y axis', function () {
        expect(chart.yAxis()).not.toBeNull();
    });

    it('should create the brush', function () {
        expect(chart.select('g.brush')).not.toBeNull();
    });

    it('does not set round by default', function () {
        expect(chart.round()).not.toBeDefined();
    });

    it('can change round', function () {
        chart.round(d3.time.day.utc.round);
        expect(chart.round()).not.toBeNull();
    });

    it('has a default value for x', function () {
        expect(chart.keyAccessor()).not.toBeNull();
    });

    it('has a default value for y', function () {
        expect(chart.valueAccessor()).not.toBeNull();
    });

    describe('rendering the chart', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create a root SVG element', function () {
            expect(chart.svg().empty()).toBeFalsy();
        });

        it('should create a root SVG group element', function () {
            expect(chart.g().empty()).toBeFalsy();
        });

        it('should size the chart to the full height of the chart', function () {
            expect(chart.select('svg').attr('height')).toBe('150');
        });

        it('should set x range to width', function () {
            expect(chart.x().range()).toEqual([0, 420]);
        });

        it('should set y domain', function () {
            expect(chart.y()).toBeDefined();
        });

        it('should set y range to height by default', function () {
            expect(chart.y().range()).toEqual([110, 0]);
        });

        it('should automatically size the y domain based on height', function () {
            expect(chart.y().domain()).toEqual([0, 281]);
        });

        it('should place the x axis at the bottom', function () {
            expect(chart.select('svg g g.x').attr('transform')).toMatchTranslate(30,120);
        });

        it('should place the y axis to the left', function () {
            expect(chart.select('svg g g.y').attr('transform')).toMatchTranslate(30,10);
        });

        it('should create a separate g for each subchart', function () {
            expect(chart.selectAll('g.sub').size()).toBe(3);
        });

        it('should index each subchart g by css class', function () {
            expect(d3.select(chart.selectAll('g.sub')[0][0]).attr('class')).toBe('sub _0');
            expect(d3.select(chart.selectAll('g.sub')[0][1]).attr('class')).toBe('sub _1');
        });

        it('should generate sub line chart paths', function () {
            expect(chart.selectAll('g.sub path.line').size()).not.toBe(0);
            chart.selectAll('g.sub path.line').each(function (d, i) {
                switch (i) {
                case 0:
                    expect(d3.select(this).attr('d'))
                        .toMatchPath('M24.137931034482758,110L91.72413793103448,108L101.37931034482757,103L202.75862068965515,' +
                        '108L246.20689655172413,104L395.8620689655172,105');
                    break;
                case 1:
                    expect(d3.select(this).attr('d'))
                        .toMatchPath('M24.137931034482758,92L91.72413793103448,82L101.37931034482757,52L202.75862068965515,' +
                        '91L246.20689655172413,83L395.8620689655172,75');
                    break;
                }
            });
        });

        it('should generate sub bar charts', function () {
            expect(chart.selectAll('g.sub g._0 rect').size()).toBe(6);
        });

        it('should render sub bar chart', function () {
            expect(chart.selectAll('g.sub rect.bar').size()).not.toBe(0);
            chart.selectAll('g.sub rect.bar').each(function (d, i) {
                switch (i) {
                case 0:
                    expect(d3.select(this).attr('x')).toBeCloseTo('22.637931034482758', 3);
                    expect(d3.select(this).attr('y')).toBe('93');
                    expect(d3.select(this).attr('width')).toBe('3');
                    expect(d3.select(this).attr('height')).toBe('17');
                    break;
                case 5:
                    expect(d3.select(this).attr('x')).toBeCloseTo('394.3620689655172', 3);
                    expect(d3.select(this).attr('y')).toBe('80');
                    expect(d3.select(this).attr('width')).toBe('3');
                    expect(d3.select(this).attr('height')).toBe('30');
                    break;
                }
            });
        });

        describe('the chart clip paths', function () {
            it('should create only one defs', function () {
                expect(chart.selectAll('defs').size()).toBe(1);
            });

            it('should create only one clip path', function () {
                expect(chart.selectAll('defs #composite-chart-clip').size()).toBe(1);
            });

            it('should create only one clip rect', function () {
                expect(chart.selectAll('defs #composite-chart-clip rect').size()).toBe(1);
            });

            it('should have the correct size', function () {
                var rect = chart.select('defs #composite-chart-clip rect');
                expect(rect.attr('width')).toBe('420');
                expect(rect.attr('height')).toBe('110');
            });

            it('should have clip path refs', function () {
                expect(chart.selectAll('g.chart-body').size()).not.toBe(0);
                chart.selectAll('g.chart-body').each(function () {
                    expect(d3.select(this).attr('clip-path')).toMatchUrl('#composite-chart-clip');
                });
            });
        });

        describe('the chart brush', function () {

            it('should be positioned with the chart left margin', function () {
                expect(chart.select('g.brush').attr('transform')).toMatchTranslate(chart.margins().left,10);
            });

            it('should have a resize handle', function () {
                expect(chart.selectAll('g.brush .resize path').size()).not.toBe(0);
                chart.selectAll('g.brush .resize path').each(function (d, i) {
                    if (i === 0) {
                        expect(d3.select(this).attr('d'))
                            .toMatchPath('M0.5,36.666666666666664A6,6 0 0 1 6.5,42.666666666666664V67.33333333333333A6,' +
                            '6 0 0 1 0.5,73.33333333333333ZM2.5,44.666666666666664V65.33333333333333M4.5,' +
                            '44.666666666666664V65.33333333333333');
                    } else {
                        expect(d3.select(this).attr('d'))
                            .toMatchPath('M-0.5,36.666666666666664A6,6 0 0 0 -6.5,42.666666666666664V67.33333333333333A6,' +
                            '6 0 0 0 -0.5,73.33333333333333ZM-2.5,44.666666666666664V65.33333333333333M-4.5,' +
                            '44.666666666666664V65.33333333333333');
                    }
                });
            });

            it('should stretch the background', function () {
                expect(chart.select('g.brush rect.background').attr('width')).toBe('420');
            });

            it('should set the height of background to height of chart', function () {
                expect(chart.select('g.brush rect.background').attr('height')).toBe('110');
            });

            it('should set the extent height to chart height', function () {
                expect(chart.select('g.brush rect.extent').attr('height')).toBe('110');
            });

            describe('when filtering the chart', function () {
                beforeEach(function () {
                    chart.filter([makeDate(2012, 5, 1), makeDate(2012, 5, 30)]).redraw();
                });

                it('should set extent width to chart width based on filter set', function () {
                    expect(chart.select('g.brush rect.extent').attr('width')).toBe('140');
                });

                it('should fade filtered bars into the background', function () {
                    expect(chart.selectAll('g.sub rect.deselected').size()).toBe(4);
                });
            });

            describe('after filtering all', function () {
                beforeEach(function () {
                    chart.filterAll();
                    chart.redraw();
                });

                it('should bring all bars to the foreground', function () {
                    chart.selectAll('g rect.bar').each(function (d) {
                        expect(d3.select(this).attr('class')).toBe('bar');
                    });
                });
            });
        });

        describe('legends composed of subchart groups', function () {
            beforeEach(function () {
                chart.legend(dc.legend().x(200).y(10).itemHeight(13).gap(5)).render();
            });

            it('should generate a legend item for each subchart', function () {
                expect(chart.selectAll('g.dc-legend g.dc-legend-item').size()).toBe(5);
            });

            it('should generate legend labels for each sub-chart', function () {
                expect(chart.selectAll('g.dc-legend-item text').size()).toBe(5);
            });

            it('should be placed according to its own legend option, ignoring the sub-charts', function () {
                expect(chart.select('g.dc-legend').attr('transform')).toMatchTranslate(200,10);
            });

            it('should generate legend labels with their associated group text', function () {
                function legendText (n) {
                    return d3.select(chart.selectAll('g.dc-legend g.dc-legend-item text')[0][n]).text();
                }
                expect(legendText(0)).toBe('Date Value Group Bar');
                expect(legendText(1)).toBe('Date ID Group');
                expect(legendText(2)).toBe('Date Value Group Line 1');
                expect(legendText(3)).toBe('Date Value Group Line 2');
                expect(legendText(4)).toBe('Date Group');
            });

            it('should properly delegate highlighting to its children', function () {
                var firstItem = chart.select('g.dc-legend g.dc-legend-item');

                firstItem.on('mouseover')(firstItem.datum());
                expect(chart.selectAll('rect.highlight').size()).toBe(6);
                expect(chart.selectAll('path.fadeout').size()).toBe(4);
                firstItem.on('mouseout')(firstItem.datum());
                expect(chart.selectAll('rect.highlight').size()).toBe(0);
                expect(chart.selectAll('path.fadeout').size()).toBe(0);
            });

            it('should hide hidable child stacks', function () {
                var dateValueGroupLine2 = d3.select(chart.selectAll('g.dc-legend g.dc-legend-item')[0][3]);

                dateValueGroupLine2.on('click')(dateValueGroupLine2.datum());
                expect(dateValueGroupLine2.text()).toBe('Date Value Group Line 2');
                expect(d3.select(chart.selectAll('g.dc-legend g.dc-legend-item')[0][3]).classed('fadeout')).toBeTruthy();
                expect(chart.selectAll('path.line').size()).toEqual(3);
            });
        });
    });

    describe('no elastic', function () {
        beforeEach(function () {
            chart.y(d3.scale.linear().domain([-200, 200]));
            chart.render();
        });

        it('should respect manually applied domain', function () {
            expect(chart.y().domain()[0]).toBe(-200);
            expect(chart.y().domain()[1]).toBe(200);
        });
    });

    describe('elastic chart axes', function () {
        beforeEach(function () {
            data.dimension(function (d) {
                return d.countrycode;
            }).filter('CA');

            chart.elasticY(true).elasticX(true).render();
        });

        it('should adjust the y axis, combining all child charts maxs & mins', function () {
            expect(chart.y().domain()[1]).toBe(115);
        });

        it('should set the x domain', function () {
            expect(chart.x().domain()[0].getTime() >= 1337904000000).toBeTruthy();
            expect(chart.x().domain()[1].getTime() >= 1344556800000).toBeTruthy();
        });
    });

    describe('subchart renderlets', function () {
        beforeEach(function () {
            chart.children()[0].on('renderlet', function (chart) {
                chart.selectAll('rect.bar').attr('width', function (d) {
                    return 10;
                });
            });
            chart.render();
        });

        it('should trigger the sub-chart renderlet', function () {
            expect(d3.select(chart.selectAll('rect')[0][0]).attr('width')).toBe('10');
        });
    });

    describe('when two subcharts share the same group', function () {
        beforeEach(function () {
            var dimension = data.dimension(function (d) {
                return d.status;
            });
            var group = dimension.group().reduce(
                function (p, v) {
                    ++p.count;
                    p.value += +v.value;
                    return p;
                },
                function (p, v) {
                    --p.count;
                    p.value -= +v.value;
                    return p;
                },
                function () {
                    return {count: 0, value: 0};
                }
            );
            chart
                .brushOn(false)
                .dimension(dimension)
                .shareTitle(false)
                .x(d3.scale.ordinal())
                .xUnits(dc.units.ordinal)
                .compose([
                    dc.lineChart(chart)
                        .group(group, 'Series 1')
                        .valueAccessor(function (d) {
                            return d.value.count;
                        })
                        .title(function (d) {
                            var value = d.value.count;
                            if (isNaN(value)) {
                                value = 0;
                            }
                            return 'Count: ' + d3.format('d')(value);
                        }),
                    dc.lineChart(chart)
                        .group(group, 'Series 2')
                        .valueAccessor(function (d) {
                            return d.value.value;
                        })
                        .title(function (d) {
                            var value = d.value.value;
                            if (isNaN(value)) {
                                value = 0;
                            }
                            return 'Value: ' + d3.format('d')(value);

                        })
                ]).render();
        });

        it('should set a tooltip based on the shared group', function () {
            expect(chart.select('.sub._0 .dc-tooltip._0 .dot title').text()).toBe('Count: 5');
            expect(chart.select('.sub._1 .dc-tooltip._0 .dot title').text()).toBe('Value: 220');
        });
    });

    describe('subchart title rendering', function () {
        beforeEach(function () {
            chart.renderTitle(false);
            chart.render();
        });

        it('should respect boolean flag when title not set', function () {
            expect(chart.select('.sub._0 .dc-tooltip._0 .dot').empty()).toBeTruthy();
            expect(chart.select('.sub._1 .dc-tooltip._0 .dot').empty()).toBeTruthy();
        });
    });

    describe('the y-axes', function () {
        describe('when composing charts with both left and right y-axes', function () {
            var rightChart;

            beforeEach(function () {
                chart
                    .compose([
                        dc.barChart(chart)
                            .group(dateValueSumGroup, 'Date Value Group'),
                        rightChart = dc.lineChart(chart)
                            .group(dateIdSumGroup, 'Date ID Group')
                            .stack(dateValueSumGroup, 'Date Value Group')
                            .stack(dateValueSumGroup, 'Date Value Group')
                            .useRightYAxis(true)
                    ])
                    .render();
            });

            it('should render two y-axes', function () {
                expect(chart.selectAll('.axis').size()).toBe(3);
            });

            it('should render a right and a left label', function () {
                chart.yAxisLabel('Left Label').rightYAxisLabel('Right Label').render();

                expect(chart.selectAll('.y-axis-label').size()).toBe(2);
                expect(chart.selectAll('.y-axis-label.y-label').empty()).toBeFalsy();
                expect(chart.selectAll('.y-axis-label.yr-label').empty()).toBeFalsy();
            });

            it('should scale "right" charts according to the right y-axis' , function () {
                expect(rightChart.y()).toBe(chart.rightY());
            });

            it('should set the domain of the right axis', function () {
                expect(rightChart.yAxisMin()).toBe(0);
                expect(rightChart.yAxisMax()).toBe(281);
            });

            it('domain', function () {
                expect(chart.rightY().domain()).toEqual([0, 281]);
                expect(chart.y().domain()).toEqual([0, 132]);
            });

            it('should set "right" chart y-axes to the composite chart right y-axis', function () {
                expect(rightChart.yAxis()).toBe(chart.rightYAxis());
            });

            describe('horizontal gridlines', function () {
                beforeEach(function () {
                    chart.yAxis().ticks(3);
                    chart.rightYAxis().ticks(6);
                    chart.renderHorizontalGridLines(true).render();
                });

                it('should draw left horizontal gridlines by default', function () {
                    expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(3);
                });

                it('should allow right horizontal gridlines to be used', function () {
                    chart.useRightAxisGridLines(true).render();
                    expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(6);
                });
            });
        });

        describe('when composing charts with just a left axis', function () {
            beforeEach(function () {
                chart.yAxis().ticks(4);
                chart.compose([
                    dc.lineChart(chart).group(dateGroup)
                ]).renderHorizontalGridLines(true).render();
            });

            it('should only render a left y axis', function () {
                expect(chart.selectAll('.axis.y').empty()).toBeFalsy();
                expect(chart.selectAll('.axis.yr').empty()).toBeTruthy();
            });

            it('should only draw left horizontal gridlines', function () {
                expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(4);
            });
        });

        describe('when composing charts with just a right axis', function () {
            beforeEach(function () {
                chart.yAxis().ticks(7);
                chart.compose([
                    dc.lineChart(chart).group(dateGroup).useRightYAxis(true)
                ]).renderHorizontalGridLines(true).render();
            });

            it('should only render a right y axis', function () {
                expect(chart.selectAll('.axis.y').empty()).toBeTruthy();
                expect(chart.selectAll('.axis.yr').empty()).toBeFalsy();
            });

            it('should only draw the right horizontal gridlines', function () {
                expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(7);
            });
        });

        describe('when composing a left axis chart with negative values', function () {
            var leftChart, rightChart;
            beforeEach(function () {
                chart
                    .compose([
                        leftChart = dc.barChart(chart)
                            .group(dateValueNegativeSumGroup, 'Date Value Group'),
                        rightChart = dc.lineChart(chart)
                            .group(dateIdSumGroup, 'Date ID Group')
                            .useRightYAxis(true)
                    ])
                    .render();
            });

            it('the axis baselines shouldn\'t match', function () {
                expect(leftChart.y()(0)).not.toEqual(rightChart.y()(0));
            });

            describe('with alignYAxes', function () {
                beforeEach(function () {
                    chart.alignYAxes(true)
                        .elasticY(true)
                        .render();
                });
                it('the axis baselines should match', function () {
                    expect(leftChart.y()(0)).toEqual(rightChart.y()(0));
                });
            });
        });

        describe('when composing a right axis chart with negative values', function () {
            var leftChart, rightChart;
            beforeEach(function () {
                chart
                    .compose([
                        leftChart = dc.barChart(chart)
                            .group(dateIdSumGroup, 'Date Value Group'),
                        rightChart = dc.lineChart(chart)
                            .group(dateValueNegativeSumGroup, 'Date ID Group')
                            .useRightYAxis(true)
                    ])
                    .render();
            });

            it('the axis baselines shouldn\'t match', function () {
                expect(leftChart.y()(0)).not.toEqual(rightChart.y()(0));
            });

            describe('with alignYAxes', function () {
                beforeEach(function () {
                    chart.alignYAxes(true)
                        .elasticY(true)
                        .render();
                });
                it('the axis baselines should match', function () {
                    expect(leftChart.y()(0)).toEqual(rightChart.y()(0));
                });
            });
        });
    });

    describe('sub-charts with different filter types', function () {
        var scatterGroup, scatterDimension;
        var lineGroup, lineDimension;

        beforeEach(function () {
            data = crossfilter(loadDateFixture());

            scatterDimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });
            scatterGroup = scatterDimension.group();

            lineDimension = data.dimension(function (d) { return +d.value; });
            lineGroup = lineDimension.group();

            chart
                .dimension(scatterDimension)
                .group(scatterGroup)
                .x(d3.scale.linear().domain([0,70]))
                .brushOn(true)
                .compose([
                    dc.scatterPlot(chart),
                    dc.scatterPlot(chart),
                    dc.lineChart(chart).dimension(lineDimension).group(lineGroup)
                ]).render();
        });

        describe('brushing', function () {
            var otherDimension;

            beforeEach(function () {
                otherDimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });
                chart.brush().extent([22, 35]);
                chart.brush().on('brush')();
                chart.redraw();
            });

            it('should filter the child charts', function () {
                expect(otherDimension.top(Infinity).length).toBe(4);
            });

            describe('brush decreases in size', function () {
                beforeEach(function () {
                    chart.brush().extent([22, 33]);
                    chart.brush().on('brush')();
                    chart.redraw();
                });

                it('should filter down to fewer points', function () {
                    expect(otherDimension.top(Infinity).length).toBe(2);
                });

            });

            describe('brush disappears', function () {
                beforeEach(function () {
                    chart.brush().extent([22, 22]);
                    chart.brush().on('brush')();
                    chart.redraw();
                });

                it('should clear all filters', function () {
                    expect(otherDimension.top(Infinity).length).toBe(10);
                });
            });
        });
    });
});
