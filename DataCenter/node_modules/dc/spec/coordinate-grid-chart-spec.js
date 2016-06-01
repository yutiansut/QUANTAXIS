/* global appendChartID, loadDateFixture, makeDate, cleanDateRange */
describe('dc.coordinateGridChart', function () {
    var chart, id;
    var data, dimension, group;

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        dimension = data.dimension(function (d) { return d3.time.day.utc(d.dd); });
        group = dimension.group();

        id = 'coordinate-grid-chart';
        appendChartID(id);

        chart = dc.lineChart('#' + id)
            .width(500)
            .height(150)
            .dimension(dimension)
            .group(group)
            .transitionDuration(0)
            .brushOn(false)
            .margins({top: 20, bottom: 0, right: 10, left: 0})
            .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]));
    });

    describe('rendering', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create the svg', function () {
            expect(chart.svg().empty()).toBeFalsy();
        });

        it('should create a root g', function () {
            expect(chart.g().empty()).toBeFalsy();
        });

        it('should register the chart', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });

        it('should set a dimension on the chart', function () {
            expect(chart.dimension()).toBe(dimension);
        });

        it('should set a group on the chart', function () {
            expect(chart.group()).toBe(group);
        });

        it('should set a width on the chart', function () {
            expect(chart.width()).toBe(500);
        });

        it('should set a height on the chart', function () {
            expect(chart.height()).toBe(150);
        });

        it('should use the height for the svg', function () {
            expect(chart.select('svg').attr('height')).toBe('150');
        });

        it('should have zero transition duration', function () {
            expect(chart.transitionDuration()).toBe(0);
        });

        it('should set the margins of the chart', function () {
            expect(chart.margins()).not.toBeNull();
        });

        it('should set an x domain', function () {
            expect(chart.x()).toBeDefined();
        });

        it('should set a y domain', function () {
            expect(chart.y()).toBeDefined();
        });

        it('should set the x domain to endpoint dates', function () {
            expect(chart.x().domain()).toEqual([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]);
        });

        it('should create the brush', function () {
            expect(chart.select('g.brush')).not.toBeNull();
        });

        it('should not set round by default', function () {
            expect(chart.round()).not.toBeDefined();
        });

        it('should auto-calculate x range round based on width', function () {
            expect(chart.x().range()[0]).toBe(0);
            expect(chart.x().range()[1]).toBe(490);
        });

        it('should auto-calculate y range round based on height', function () {
            expect(chart.y().range()[0]).toBe(130);
            expect(chart.y().range()[1]).toBe(0);
        });

        it('should auto-calculate y domain based on height', function () {
            expect(chart.y().domain()[0]).toBe(0);
            expect(chart.y().domain()[1]).toBe(3);
        });

        it('should be able to change round', function () {
            chart.round(d3.time.day.utc.round);
            expect(chart.round()).not.toBeNull();
        });

        it('should have a default value for x', function () {
            expect(chart.keyAccessor()).not.toBeNull();
        });

        it('should have a default value for y', function () {
            expect(chart.valueAccessor()).not.toBeNull();
        });

        describe('renderlets', function () {
            beforeEach(function () {
                chart.on('renderlet', function (chart) {
                    chart.selectAll('path').attr('fill', 'red');
                });
            });

            it('should not run immediately', function () {
                expect(chart.selectAll('path').attr('fill')).not.toBe('red');
            });

            it('should run when render is invoked', function () {
                chart.render();
                expect(chart.selectAll('path').attr('fill')).toBe('red');
            });

            it('should run when redraw is invoked', function () {
                chart.redraw();
                expect(chart.selectAll('path').attr('fill')).toBe('red');
            });
        });

        describe('clip paths', function () {
            it('should only create one def', function () {
                expect(chart.selectAll('defs').size()).toBe(1);
            });

            it('should only create one clip path', function () {
                // selecting on ID due to webkit bug #83438
                expect(chart.selectAll('defs #coordinate-grid-chart-clip').size()).toBe(1);
            });

            it('should only create one clip rect', function () {
                expect(chart.selectAll('defs #coordinate-grid-chart-clip rect').size()).toBe(1);
            });

            it('should create a clip rect based on the graph size', function () {
                var rect = chart.select('defs #coordinate-grid-chart-clip rect');
                expect(rect.attr('width')).toBe('490');
                expect(rect.attr('height')).toBe('130');
            });

            it('should translate the clip rect to 0,0', function () {
                var rect = chart.select('defs #coordinate-grid-chart-clip rect');
                expect(rect.attr('transform')).toMatchTranslate(0,0);
            });

            it('should add clip path refs to the chart body', function () {
                chart.selectAll('g.chart-body').each(function () {
                    expect(d3.select(this).attr('clip-path')).toMatchUrl('#coordinate-grid-chart-clip');
                });
            });

            describe('setting clipPadding(20)', function () {

                beforeEach(function () {
                    chart.clipPadding(20);
                    chart.render();
                });

                it('should update the clip rect based on the graph size and clipPadding', function () {
                    var rect = chart.select('defs #coordinate-grid-chart-clip rect');
                    expect(rect.attr('width')).toBe('530');
                    expect(rect.attr('height')).toBe('170');
                });

                it('should translate the clip rect to -20,-20', function () {
                    var rect = chart.select('defs #coordinate-grid-chart-clip rect');
                    expect(rect.attr('transform')).toMatchTranslate(-20,-20);
                });

            });

            describe('with a complex selector', function () {
                beforeEach(function () {
                    appendChartID('coordinate-grid').append('div').attr('class', 'chart');
                    chart = dc.lineChart('#coordinate-grid .chart')
                        .width(500)
                        .height(150)
                        .dimension(dimension)
                        .group(group)
                        .transitionDuration(0)
                        .brushOn(false)
                        .margins({top: 20, bottom: 0, right: 10, left: 0})
                        .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]));
                    chart.render();
                });
                it('should generate a valid clippath id', function () {
                    var rect = chart.select('defs #coordinate-grid--chart-clip rect');
                    expect(rect.empty()).toBeFalsy();
                });
            });

            describe('with a selector containing brackets', function () {
                beforeEach(function () {
                    appendChartID('coordinate-grid').append('div').attr('class', 'chart').attr('foo', 'bar');
                    chart = dc.lineChart('#coordinate-grid .chart[foo=bar]')
                        .width(500)
                        .height(150)
                        .dimension(dimension)
                        .group(group)
                        .transitionDuration(0)
                        .brushOn(false)
                        .margins({top: 20, bottom: 0, right: 10, left: 0})
                        .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]));
                    chart.render();
                });
                it('should generate a valid clippath id', function () {
                    var rect = chart.select('defs #coordinate-grid--chart-foo-bar--clip rect');
                    expect(rect.empty()).toBeFalsy();
                });
            });

            describe('redrawing at a different size', function () {
                beforeEach(function () {
                    chart.width(300).height(400).redraw();
                });
                it('should change the clippath to the new size', function () {
                    var rect = chart.select('defs #coordinate-grid-chart-clip rect');
                    expect(rect.attr('width')).toBe('290');
                    expect(rect.attr('height')).toBe('380');
                });
            });
        });

        describe('when an x function is not provided', function () {
            it('should trigger a descriptive exception', function () {
                try {
                    dc.coordinateGridChart({}).group({}).dimension({}).render();
                    expect('exception').toBe('thrown');
                } catch (e) {
                    expect(e instanceof dc.errors.InvalidStateException).toBeTruthy();
                    expect(e.message).toMatch(/Mandatory attribute chart.x is missing on chart\[#.+\]/);
                }
            });
        });

        describe('x-axis', function () {
            it('should place an x axis at the bottom', function () {
                expect(chart.select('g.x').attr('transform')).toMatchTranslate(0,150);
            });

            it('should update x axis position when the chart height is changed', function () {
                chart.elasticX(true).height(400).redraw();
                expect(chart.select('g.x').attr('transform')).toMatchTranslate(0,400);
            });

            describe('labels', function () {
                beforeEach(function () {
                    expect(chart.effectiveHeight()).toBe(130);
                    chart.xAxisLabel('X Label').render();
                });

                it('should set the x-axis label', function () {
                    expect(chart.selectAll('text.x-axis-label').text()).toBe('X Label');
                });

                it('should adjust the chart height accordingly due to label padding', function () {
                    expect(chart.effectiveHeight()).toBe(118);
                });

                describe('with custom padding', function () {
                    beforeEach(function () {
                        chart.xAxisLabel('Custom X Label', 50).render();
                    });

                    it('should adjust the chart height with respect to the custom padding', function () {
                        expect(chart.effectiveHeight()).toBe(80);
                    });
                });

                describe('reset axis label', function () {
                    beforeEach(function () {
                        chart.elasticX(true).xAxisLabel('New X Label').redraw();
                    });
                    it('should change the x-axis label', function () {
                        expect(chart.selectAll('text.x-axis-label').text()).toBe('New X Label');
                    });
                });
            });
        });

        describe('y-axes', function () {
            describe('grid lines', function () {
                beforeEach(function () {
                    chart
                        .renderHorizontalGridLines(true)
                        .renderVerticalGridLines(true)
                        .render();
                });

                describe('horizontal grid lines', function () {
                    it('should draw lines associated with the data shown on the right y-axis', function () {
                        var nthGridLine = function (n) { return d3.select(chart.selectAll('.grid-line.horizontal line')[0][n]); };

                        expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(7);
                        expect(nthGridLine(0).attr('y2')).toBe('130');
                        expect(nthGridLine(0).attr('y1')).toBe('130');
                        expect(nthGridLine(1).attr('y1')).toBe('108');
                        expect(nthGridLine(2).attr('y1')).toBe('87');
                    });

                    it('should position the lines horizontally on the graph', function () {
                        var firstGridLine = chart.select('.grid-line.horizontal line');
                        expect(firstGridLine.attr('x1')).toBe('1');
                        expect(firstGridLine.attr('x2')).toBe('490');
                        expect(firstGridLine.attr('y1')).toBe(firstGridLine.attr('y2'));
                    });

                    describe('with custom tick values', function () {
                        beforeEach(function () {
                            chart.yAxis().tickValues([0, 1, 2]);
                            chart.render();
                        });

                        it('should draws lines associated with the data using the custom ticks', function () {
                            var nthGridLine = function (n) { return d3.select(chart.selectAll('.grid-line.horizontal line')[0][n]); };

                            expect(chart.selectAll('.grid-line.horizontal line').size()).toBe(3);
                            expect(nthGridLine(0).attr('y2')).toBe('130');
                            expect(nthGridLine(0).attr('y1')).toBe('130');
                            expect(nthGridLine(1).attr('y1')).toBe('87');
                            expect(nthGridLine(2).attr('y1')).toBe('43');
                        });
                    });
                });

                describe('vertical grid lines', function () {
                    it('should draw lines associated with the data shown on the x-axis', function () {
                        var nthGridLine = function (n) { return d3.select(chart.selectAll('.grid-line.vertical line')[0][n]); };

                        expect(chart.selectAll('.grid-line.vertical line').size()).toBe(13);
                        expect(nthGridLine(0).attr('x2')).toBe('0');
                        expect(nthGridLine(0).attr('x1')).toBe('0');
                        expect(nthGridLine(1).attr('x1')).toBeWithinDelta(39, 1);
                        expect(nthGridLine(2).attr('x1')).toBeWithinDelta(79, 1);
                    });

                    it('should position the lines vertically on the graph', function () {
                        var firstGridLine = chart.select('.grid-line.vertical line');
                        expect(firstGridLine.attr('y1')).toBe('130');
                        expect(firstGridLine.attr('y2')).toBe('0');
                        expect(firstGridLine.attr('x1')).toBe(firstGridLine.attr('x2'));
                    });

                    describe('with custom tick values', function () {
                        beforeEach(function () {
                            chart.xAxis().tickValues([makeDate(2012, 4, 21), makeDate(2012, 5, 20), makeDate(2012, 6, 1)]);
                            chart.render();
                        });

                        it('should draw lines associated with the data using the custom ticks', function () {
                            var nthGridLine = function (n) { return d3.select(chart.selectAll('.grid-line.vertical line')[0][n]); };

                            expect(chart.selectAll('.grid-line.vertical line').size()).toBe(3);
                            expect(nthGridLine(0).attr('x2')).toBeWithinDelta(6, 1);
                            expect(nthGridLine(0).attr('x1')).toBeWithinDelta(6, 1);
                            expect(nthGridLine(1).attr('x1')).toBeWithinDelta(175, 1);
                            expect(nthGridLine(2).attr('x1')).toBeWithinDelta(237, 1);
                        });
                    });

                    describe('with an ordinal x axis', function () {
                        beforeEach(function () {
                            chart.x(d3.scale.ordinal())
                                .xUnits(dc.units.ordinal)
                                .render();
                        });
                        it('should render without errors', function () {
                            expect(chart.selectAll('.grid-line.vertical line').size()).toBe(6);
                        });
                    });
                });
            });

            describe('a left y-axis', function () {
                beforeEach(function () {
                    chart.render();
                });

                it('should render a y-axis', function () {
                    expect(chart.selectAll('.axis.y').size()).toBe(1);
                });

                it('should orient the y-axis text to the left by default', function () {
                    expect(chart.yAxis().orient()).toBe('left');
                });

                it('should place the y axis to the left', function () {
                    expect(chart.select('g.y').attr('transform')).toMatchTranslate(0,20);
                });

                describe('y-axis labels', function () {
                    beforeEach(function () {
                        expect(chart.effectiveWidth()).toBe(490);
                        chart.yAxisLabel('The Y Axis Label').render();
                    });

                    it('should display provided label text', function () {
                        expect(chart.selectAll('text.y-axis-label.y-label').text()).toBe('The Y Axis Label');
                    });

                    it('should change the effective width of the chart due to padding', function () {
                        expect(chart.effectiveWidth()).toBe(478);
                    });

                    it('should position the label to the left of the chart', function () {
                        expect(chart.selectAll('text.y-axis-label.y-label').attr('transform')).toMatchTransRot(12,85,-90);
                    });

                    describe('with custom padding', function () {
                        beforeEach(function () {
                            chart.yAxisLabel('Custom Y Label', 50).render();
                        });

                        it('should adjust the chart height with respect to the custom padding', function () {
                            expect(chart.effectiveWidth()).toBe(440);
                        });
                    });
                });
            });

            describe('a right y-axis', function () {
                beforeEach(function () {
                    chart.useRightYAxis(true).render();
                });

                it('should render a y-axis', function () {
                    expect(chart.selectAll('.axis.y').size()).toBe(1);
                });

                it('should orient the y-axis text to the right', function () {
                    expect(chart.yAxis().orient()).toBe('right');
                });

                it('should position the axis to the right of the chart', function () {
                    expect(chart.select('.axis.y').attr('transform')).toMatchTranslate(490,20);
                });

                describe('y-axis labels', function () {
                    beforeEach(function () {
                        expect(chart.effectiveWidth()).toBe(490);
                        chart.yAxisLabel('Right Y Axis Label').render();
                    });

                    it('should display provided label text', function () {
                        expect(chart.selectAll('text.y-axis-label.y-label').text()).toBe('Right Y Axis Label');
                    });

                    it('should change the effective width of the chart due to padding', function () {
                        expect(chart.effectiveWidth()).toBe(478);
                    });

                    it('should position the label to the right of the chart', function () {
                        expect(chart.selectAll('text.y-axis-label.y-label').attr('transform')).toMatchTransRot(488,85,90);
                    });

                    describe('with custom padding', function () {
                        beforeEach(function () {
                            chart.yAxisLabel('Custom Y Label', 50).render();
                        });

                        it('should adjust the chart height with respect to the custom padding', function () {
                            expect(chart.effectiveWidth()).toBe(440);
                        });
                    });
                });
            });
        });
    });

    describe('elastic axis', function () {
        describe('with data', function () {
            beforeEach(function () {
                data.dimension(function (d) {
                    return d.countrycode;
                }).filter('CA');

                chart.elasticX(true).elasticY(true).render();
            });

            it('should shrink the y axis', function () {
                expect(chart.y().domain()[1]).toBe(1);
            });

            it('should shrink the x domain', function () {
                expect(chart.x().domain()).toEqual([makeDate(2012, 4, 25), makeDate(2012, 7, 10)]);
            });
        });

        describe('with no data', function () {
            beforeEach(function () {
                data.dimension(function (d) {
                    return d.countrycode;
                }).filter('INVALID CODE');

                chart.elasticX(true).elasticY(true).render();
            });

            it('should set y-axis to be empty', function () {
                expect(chart.y().domain()[0]).toBe(0);
                expect(chart.y().domain()[1]).toBe(0);
            });

        });
    });

    describe('rescaling', function () {
        var originalUnitCount;
        beforeEach(function () {
            chart.render();
            originalUnitCount = chart.xUnitCount();
            chart.x().domain([makeDate(2012, 4, 20), makeDate(2012, 6, 15)]);
            chart.rescale();
        });

        it('should reset x unit count to reflect updated x domain', function () {
            expect(chart.xUnitCount()).not.toEqual(originalUnitCount);
        });
    });

    describe('range chart setup', function () {
        var rangeChart;

        beforeEach(function () {
            rangeChart = buildRangeChart();
            chart.rangeChart(rangeChart);
            chart.render();
            rangeChart.render();
        });

        it('should set our chart as range chart\'s focus chart', function () {
            expect(chart.rangeChart().focusChart()).toEqual(chart);
        });
    });

    describe('restricting zoom out', function () {
        beforeEach(function () {
            chart.zoomScale([-1,10]);
            chart.zoomOutRestrict(true);
        });

        it('should set the start of zoom scale extent to 1', function () {
            expect(chart.zoomScale()[0]).toEqual(1);
        });

        it('sohuld leave the end of zoom scale extent unchanged', function () {
            expect(chart.zoomScale()[1]).toEqual(10);
        });
    });

    describe('disabling zoom out restriction', function () {
        beforeEach(function () {
            chart.zoomScale([-1,10]);
            chart.zoomOutRestrict(false);
        });

        it('should set the start of zoom scale extent to 0', function () {
            expect(chart.zoomScale()[0]).toEqual(0);
        });
    });

    describe('setting x', function () {
        var newDomain = [1,10];
        beforeEach(function () {
            chart.x(d3.scale.linear().domain(newDomain));
        });

        it('should reset the original x domain', function () {
            expect(chart.xOriginalDomain()).toEqual(newDomain);
        });
    });

    describe('x unit count', function () {
        it('reflects number of units in chart domain', function () {
            var domain = chart.x().domain();
            expect(chart.xUnitCount()).toEqual(dc.units.integers(domain[0], domain[1], domain));
        });

        describe('with fixed units', function () {
            beforeEach(function () {
                chart.xUnits(function (start, end, xDomain) { return 10; });
            });

            it('should return the fixed unit count', function () {
                expect(chart.xUnitCount()).toEqual(10);
            });
        });
    });

    describe('ordinality flag', function () {
        describe('when x units are not ordinal', function () {
            it('should be false', function () {
                expect(chart.isOrdinal()).toBeFalsy();
            });
        });

        describe('when x units are ordinal', function () {
            beforeEach(function () {
                chart.xUnits(dc.units.ordinal);
            });

            it('should be true', function () {
                expect(chart.isOrdinal()).toBeTruthy();
            });
        });
    });

    describe('applying a filter', function () {
        var filter = [makeDate(2012, 5, 20), makeDate(2012, 6, 15)];
        beforeEach(function () {
            chart.brushOn(true);
            chart.render();
            chart.filter(filter);
        });

        it('should update the brush extent', function () {
            expect(chart.brush().extent()).toEqual(filter);
        });
    });

    describe('removing the filter', function () {
        beforeEach(function () {
            chart.brushOn(true);
            chart.render();
            chart.brush().extent([makeDate(2012, 5, 20), makeDate(2012, 6, 15)]);
            chart.filter(null);
        });

        it('should clear the brush extent', function () {
            expect(chart.brush().empty()).toBeTruthy();
        });
    });

    describe('rendering for the first time with mouse zoom disabled when it wasn\'t previously enabled', function () {
        beforeEach(function () {
            chart.mouseZoomable(false);
            spyOn(chart, '_disableMouseZoom');
            chart.render();
        });

        it('should not explicitly disable mouse zooming', function () {
            expect(chart._disableMouseZoom).not.toHaveBeenCalled();
        });
    });

    describe('rendering with mouse zoom disabled after it was previously enabled', function () {
        beforeEach(function () {
            chart.mouseZoomable(true);
            chart.render();
            chart.mouseZoomable(false);
            spyOn(chart, '_disableMouseZoom');
            chart.render();
        });

        it('should explicitly disable mouse zooming', function () {
            expect(chart._disableMouseZoom).toHaveBeenCalled();
        });
    });

    describe('with mouse zoom disabled', function () {
        beforeEach(function () {
            chart.mouseZoomable(false);
            chart.render();
        });

        it('should not respond to double-click by refocusing', function () {
            doubleClick(chart);
            expect(chart.refocused()).toBeFalsy();
        });
    });

    describe('zooming', function () {
        var rangeChart, zoomCallback, context;

        context = function () { return {chart: chart, zoomCallback: zoomCallback}; };

        beforeEach(function () {
            zoomCallback = jasmine.createSpy();
            chart.on('zoomed', zoomCallback);
            chart.mouseZoomable(true);
            rangeChart = buildRangeChart();
            chart.rangeChart(rangeChart);
            chart.render();
            rangeChart.render();

            spyOn(dc, 'redrawAll');
            spyOn(chart, 'redraw');
            spyOn(rangeChart, 'redraw');
        });

        describe('when chart is zoomed via mouse interaction', function () {
            beforeEach(function () {
                doubleClick(chart);
            });

            itActsLikeItZoomed(context);
        });

        describe('when chart is zoomed programatically via focus method', function () {
            beforeEach(function () {
                chart.focus([makeDate(2012, 5, 1), makeDate(2012, 5, 15)]);
            });

            itActsLikeItZoomed(context);
        });

        function itActsLikeItZoomed (context) {
            describe('(shared things that happen on zooming)', function () {
                var chart, zoomCallback;
                beforeEach(function () {
                    chart = context().chart;
                    zoomCallback = context().zoomCallback;
                });

                it('should be flagged as refocused', function () {
                    expect(chart.refocused()).toBeTruthy();
                });

                it('should update chart filter to match new x domain', function () {
                    var filter = cleanDateRange(chart.filter());
                    expect(filter).toEqual(chart.x().domain());
                });

                it('should be rescaled', function () {
                    var domain = chart.x().domain();
                    expect(chart.xUnitCount()).toEqual(dc.units.integers(domain[0], domain[1], domain));
                });

                it('should redraw itself', function () {
                    expect(chart.redraw).toHaveBeenCalled();
                });

                it('should update its range chart\'s filter', function () {
                    expect(chart.rangeChart().filter()).toEqual(chart.filter());
                });

                it('should trigger redraw on its range chart', function () {
                    expect(chart.rangeChart().redraw).toHaveBeenCalled();
                });

                it('should fire custom zoom listeners', function () {
                    expect(zoomCallback).toHaveBeenCalled();
                });

                it('should trigger redraw on other charts in group after a brief pause', function () {
                    jasmine.clock().tick(100);
                    expect(dc.redrawAll).toHaveBeenCalledWith(chart.chartGroup());
                });
            });
        }
    });

    describe('when chart is zoomed in, then zoomed back out to original domain', function () {
        beforeEach(function () {
            chart.render();
            doubleClick(chart);
            chart.focus(chart.xOriginalDomain());
        });

        it('should not be flagged as refocused', function () {
            expect(chart.refocused()).toBeFalsy();
        });
    });

    describe('brushing', function () {
        beforeEach(function () {
            chart.brushOn(true);
        });

        describe('with mouse zoom enabled', function () {
            beforeEach(function () {
                spyOn(chart, '_disableMouseZoom');
                spyOn(chart, '_enableMouseZoom');
                chart.mouseZoomable(true);
                chart.render();
                chart.brush().extent([makeDate(2012, 6, 1), makeDate(2012, 6, 15)]);
                chart.brush().event(chart.root());
            });

            it('should disable mouse zooming on brush start, and re-enables it afterwards', function () {
                chart.brush().extent([makeDate(2012, 6, 1), makeDate(2012, 6, 15)]);
                chart.brush().event(chart.root());
                expect(chart._disableMouseZoom).toHaveBeenCalled();
                expect(chart._enableMouseZoom).toHaveBeenCalled();
            });
        });

        describe('with mouse zoom disabled', function () {
            beforeEach(function () {
                spyOn(chart, '_enableMouseZoom');
                chart.mouseZoomable(false);
                chart.render();
                chart.brush().extent([makeDate(2012, 6, 1), makeDate(2012, 6, 15)]);
                chart.brush().event(chart.root());
            });

            it('should not enable mouse zooming', function () {
                expect(chart._enableMouseZoom).not.toHaveBeenCalled();
            });
        });

        describe('with equal dates', function () {
            beforeEach(function () {
                spyOn(chart, 'filter');
                chart.brush().clear();
                chart.render();
                chart.brush().event(chart.root());
            });

            it('should clear the chart filter', function () {
                expect(chart.filter()).toEqual(undefined);
            });
        });
    });

    describe('with a range chart', function () {
        var rangeChart;
        var selectedRange = [makeDate(2012, 6, 1), makeDate(2012, 6, 15)];

        beforeEach(function () {
            rangeChart = buildRangeChart();
            chart.rangeChart(rangeChart);
            chart.render();
            rangeChart.render();
        });

        it('should zoom the focus chart when range chart is brushed', function () {
            spyOn(chart, 'focus').and.callThrough();
            rangeChart.brush().extent(selectedRange);
            rangeChart.brush().event(rangeChart.g());
            jasmine.clock().tick(100);
            // expect(chart.focus).toHaveBeenCalledWith(selectedRange);
            var focus = cleanDateRange(chart.focus.calls.argsFor(0)[0]);
            expect(focus).toEqual(selectedRange);
        });

        it('should zoom the focus chart back out when range chart is un-brushed', function () {
            rangeChart.brush().extent(selectedRange);
            rangeChart.brush().event(rangeChart.g());
            jasmine.clock().tick(100);

            expect(chart.x().domain()).toEqual(selectedRange);
            rangeChart.filter(null);
            jasmine.clock().tick(100);
            expect(rangeChart.x().domain()).toEqual(rangeChart.xOriginalDomain());
        });

        it('should update the range chart brush to match zoomed domain of focus chart', function () {
            spyOn(rangeChart, 'replaceFilter');
            chart.focus(selectedRange);
            // expect(rangeChart.replaceFilter).toHaveBeenCalledWith(selectedRange);
            var replaceFilter = cleanDateRange(rangeChart.replaceFilter.calls.argsFor(0)[0]);
            expect(replaceFilter).toEqual(selectedRange);
        });
    });

    describe('with zoom restriction enabled', function () {
        beforeEach(function () {
            chart.zoomOutRestrict(true);
            chart.render();
            chart.focus([makeDate(2012, 8, 20), makeDate(2012, 8, 25)]);
        });

        it('should not be able to zoom out past its original x domain', function () {
            chart.focus([makeDate(2012, 2, 20), makeDate(2012, 9, 15)]);
            expect(chart.x().domain()).toEqual(chart.xOriginalDomain());
        });

        describe('with a range chart', function () {
            beforeEach(function () {
                var rangeChart = buildRangeChart();
                chart.rangeChart(rangeChart);
                chart.render();
                rangeChart.render();
                chart.focus([makeDate(2012, 8, 20), makeDate(2012, 8, 25)]);
            });

            it('should not be able to zoom out past its range chart origin x domain', function () {
                chart.focus([makeDate(2012, 2, 20), makeDate(2012, 9, 15)]);
                expect(chart.x().domain()).toEqual(chart.rangeChart().xOriginalDomain());
            });
        });
    });

    describe('with zoom restriction disabled', function () {
        beforeEach(function () {
            chart.zoomOutRestrict(false);
            chart.render();
            chart.focus([makeDate(2012, 8, 20), makeDate(2012, 8, 25)]);
        });

        it('should be able to zoom out past its original x domain', function () {
            chart.focus([makeDate(2012, 2, 20), makeDate(2012, 9, 15)]);
            chart.render();
            expect(chart.x().domain()).toEqual([makeDate(2012, 2, 20), makeDate(2012, 9, 15)]);
        });
    });

    describe('focus', function () {
        beforeEach(function () {
            chart.render();
        });

        describe('when called with a range argument', function () {
            var focusDomain = [makeDate(2012,5,20), makeDate(2012,5,30)];

            beforeEach(function () {
                chart.focus(focusDomain);
            });

            it('should update the x domain to match specified domain', function () {
                expect(chart.x().domain()).toEqual(focusDomain);
            });
        });

        describe('when called with no arguments', function () {
            beforeEach(function () {
                chart.focus([makeDate(2012,5,1), makeDate(2012,5,2)]);
                chart.focus();
            });

            it('should revert the x domain to the original domain', function () {
                expect(chart.x().domain()).toEqual(chart.xOriginalDomain());
            });
        });
    });

    function buildRangeChart () {
        var rangeId = 'range-chart';
        appendChartID(rangeId);
        return dc.lineChart('#' + rangeId)
            .dimension(dimension)
            .group(dimension.group().reduceSum(function (d) { return d.id; }))
            .x(d3.time.scale.utc().domain([makeDate(2012, 5, 20), makeDate(2012, 6, 15)]));
    }

    function doubleClick (chart) {
        var centerX = chart.root().node().clientLeft + (chart.width() / 2);
        var centerY = chart.root().node().clientTop + (chart.height() / 2);
        var event = document.createEvent('MouseEvents');
        event.initMouseEvent('dblclick', true, true, window, centerX, centerY, centerX, centerY, 0, false, false, false, false, 0, null);
        chart.root().node().dispatchEvent(event);
    }
});
