/* global appendChartID, comparePaths, loadDateFixture, makeDate */
describe('dc.scatterPlot', function () {
    var id, chart;
    var data, group, dimension;

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        dimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });
        group = dimension.group();

        id = 'scatter-plot';
        appendChartID(id);

        chart = dc.scatterPlot('#' + id);
        chart.dimension(dimension)
            .group(group)
            .width(500).height(180)
            .x(d3.scale.linear().domain([0, 70]))
            .excludedColor('#ccc')
            .excludedOpacity(0.25)
            .transitionDuration(0);
    });

    describe('rendering the scatter plot', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create an svg', function () {
            expect(chart.svg().empty()).toBeFalsy();
        });

        it('should create the correct number of symbols', function () {
            expect(chart.group().all().length).toBe(chart.selectAll('path.symbol').size());
        });

        it('should correctly place the symbols', function () {
            expect(nthSymbol(4).attr('transform')).toMatchTranslate(264,131);
            expect(nthSymbol(5).attr('transform')).toMatchTranslate(264,75);
            expect(nthSymbol(8).attr('transform')).toMatchTranslate(396,131);
        });

        it('should generate a default color fill for symbols', function () {
            expect(nthSymbol(4).attr('fill')).toBe('#1f77b4');
            expect(nthSymbol(5).attr('fill')).toBe('#1f77b4');
            expect(nthSymbol(8).attr('fill')).toBe('#1f77b4');
        });

        describe('with a custom color', function () {
            beforeEach(function () {
                chart.colors('red').render();
            });

            it('should color the symbols to the provided color', function () {
                expect(nthSymbol(4).attr('fill')).toBe('red');
                expect(nthSymbol(5).attr('fill')).toBe('red');
                expect(nthSymbol(8).attr('fill')).toBe('red');
            });
        });

        function nthSymbol (i) {
            return d3.select(chart.selectAll('path.symbol')[0][i]);
        }

        describe('filtering the chart', function () {
            var otherDimension;

            beforeEach(function () {
                otherDimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });

                chart.filterAll();
                chart.filter([[22, -3], [44, 2]]);
            });

            it('should filter dimensions based on the same data', function () {
                expect(otherDimension.top(Infinity).length).toBe(3);
            });

            describe('when filtering with null', function () {
                beforeEach(function () {
                    chart.filter(null);
                });

                it('should remove all filtering from the dimensions based on the same data', function () {
                    expect(otherDimension.top(Infinity).length).toBe(10);
                });

            });
        });

        describe('filtering another dimension', function () {
            var otherDimension;

            beforeEach(function () {
                otherDimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });
                var ff = dc.filters.RangedTwoDimensionalFilter([[22, -3], [44, 2]]).isFiltered;
                otherDimension.filterFunction(ff);
                chart.redraw();
            });

            it('should show the included points', function () {
                var shownPoints = symbolsOfRadius(chart.symbolSize());
                expect(shownPoints.length).toBe(2);
                expect(shownPoints[0].key).toEqual([22, -2]);
                expect(shownPoints[1].key).toEqual([33, 1]);
            });
            it('should hide the excluded points', function () {
                var hiddenPoints = symbolsOfRadius(chart.hiddenSize());
                expect(hiddenPoints.length).toBe(7);
            });
        });

        describe('brushing', function () {
            var otherDimension;

            beforeEach(function () {
                otherDimension = data.dimension(function (d) { return [+d.value, +d.nvalue]; });

                chart.brush().extent([[22, -3], [44, 2]]);
                chart.brush().on('brush')();
                chart.redraw();
            });

            it('should filter dimensions based on the same data', function () {
                jasmine.clock().tick(100);
                expect(otherDimension.top(Infinity).length).toBe(3);
            });

            it('should set the height of the brush to the height implied by the extent', function () {
                expect(chart.select('g.brush rect.extent').attr('height')).toBe('46');
            });

            it('should not add handles to the brush', function () {
                expect(chart.select('.resize path').empty()).toBeTruthy();
            });

            describe('excluded points', function () {
                var selectedPoints;

                beforeEach(function () {
                    jasmine.clock().tick(100);
                });

                var isOpaque = function () {
                    return +d3.select(this).attr('opacity') === 1;
                }, isTranslucent = function () {
                    return +d3.select(this).attr('opacity') === 0.25;
                }, isBlue = function () {
                    return d3.select(this).attr('fill') === '#1f77b4';
                }, isGrey = function () {
                    return d3.select(this).attr('fill') === '#ccc';
                };

                it('should not shrink the included points', function () {
                    selectedPoints = symbolsOfRadius(chart.symbolSize());
                    expect(selectedPoints.length).toBe(2);
                    expect(selectedPoints[0].key).toEqual([22, -2]);
                    expect(selectedPoints[1].key).toEqual([33, 1]);
                });

                it('should shrink the excluded points', function () {
                    selectedPoints = symbolsOfRadius(chart.excludedSize());
                    expect(selectedPoints.length).toBe(7);
                    expect(selectedPoints[0].key).toEqual([22, 10]);
                    expect(selectedPoints[1].key).toEqual([44, -3]);
                });

                it('should keep the included points opaque', function () {
                    selectedPoints = symbolsMatching(isOpaque);
                    expect(selectedPoints.length).toBe(2);
                    expect(selectedPoints[0].key).toEqual([22, -2]);
                    expect(selectedPoints[1].key).toEqual([33, 1]);
                });

                it('should make the excluded points translucent', function () {
                    selectedPoints = symbolsMatching(isTranslucent);
                    expect(selectedPoints.length).toBe(7);
                    expect(selectedPoints[0].key).toEqual([22, 10]);
                    expect(selectedPoints[1].key).toEqual([44, -3]);
                });

                it('should keep the included points blue', function () {
                    selectedPoints = symbolsMatching(isBlue);
                    expect(selectedPoints.length).toBe(2);
                    expect(selectedPoints[0].key).toEqual([22, -2]);
                    expect(selectedPoints[1].key).toEqual([33, 1]);
                });

                it('should make the excluded points grey', function () {
                    selectedPoints = symbolsMatching(isGrey);
                    expect(selectedPoints.length).toBe(7);
                    expect(selectedPoints[0].key).toEqual([22, 10]);
                    expect(selectedPoints[1].key).toEqual([44, -3]);
                });

                it('should restore sizes, colors, and opacity when the brush is empty', function () {
                    chart.brush().extent([[22, 2], [22, -3]]);
                    chart.brush().on('brush')();
                    jasmine.clock().tick(100);

                    selectedPoints = symbolsOfRadius(chart.symbolSize());
                    expect(selectedPoints.length).toBe(9);

                    selectedPoints = symbolsMatching(isBlue);
                    expect(selectedPoints.length).toBe(9);

                    selectedPoints = symbolsMatching(isOpaque);
                    expect(selectedPoints.length).toBe(9);

                    chart.redraw();

                    selectedPoints = symbolsOfRadius(chart.symbolSize());
                    expect(selectedPoints.length).toBe(9);

                    selectedPoints = symbolsMatching(isBlue);
                    expect(selectedPoints.length).toBe(9);

                    selectedPoints = symbolsMatching(isOpaque);
                    expect(selectedPoints.length).toBe(9);
                });
            });
        });
    });

    function matchSymbolSize (r) {
        return function () {
            var symbol = d3.select(this);
            var size = Math.pow(r, 2);
            var path = d3.svg.symbol().size(size)();
            var result = comparePaths(symbol.attr('d'), path);
            return result.pass;
        };
    }

    function symbolsMatching (pred) {
        function getData (symbols) {
            return symbols[0].map(function (symbol) {
                return d3.select(symbol).datum();
            });
        }
        return getData(chart.selectAll('path.symbol').filter(pred));
    }

    function symbolsOfRadius (r) {
        return symbolsMatching(matchSymbolSize(r));
    }

    describe('legends', function () {
        var compositeChart, id;
        var subChart1, subChart2;
        var firstItem;

        beforeEach(function () {
            id = 'scatter-plot-composite';
            appendChartID(id);

            compositeChart = dc.compositeChart('#' + id);
            compositeChart
                .dimension(dimension)
                .x(d3.time.scale.utc().domain([makeDate(2012, 0, 1), makeDate(2012, 11, 31)]))
                .transitionDuration(0)
                .legend(dc.legend())
                .compose([
                    subChart1 = dc.scatterPlot(compositeChart).colors('red').group(group, 'Scatter 1'),
                    subChart2 = dc.scatterPlot(compositeChart).colors('blue').group(group, 'Scatter 2')
                ]).render();

            firstItem = compositeChart.select('g.dc-legend g.dc-legend-item');
        });

        it('should provide a composite chart with corresponding legend data', function () {
            expect(compositeChart.legendables()).toEqual([
                {chart: subChart1, name: 'Scatter 1', color: 'red'},
                {chart: subChart2, name: 'Scatter 2', color: 'blue'}
            ]);
        });

        describe('hovering', function () {
            beforeEach(function () {
                firstItem.on('mouseover')(firstItem.datum());
            });

            describe('when a legend item is hovered over', function () {
                it('should highlight corresponding plot', function () {
                    nthChart(0).expectPlotSymbolsToHaveSize(chart.highlightedSize());

                });

                it('should fade out non-corresponding lines and areas', function () {
                    nthChart(1).expectPlotSymbolsToHaveClass('fadeout');
                });
            });

            describe('when a legend item is hovered out', function () {
                beforeEach(function () {
                    firstItem.on('mouseout')(firstItem.datum());
                });

                it('should remove highlighting from corresponding lines and areas', function () {
                    nthChart(0).expectPlotSymbolsToHaveSize(chart.symbolSize());
                });

                it('should fade in non-corresponding lines and areas', function () {
                    nthChart(1).expectPlotSymbolsNotToHaveClass('fadeout');
                });
            });
        });

        function nthChart (n) {
            var subChart = d3.select(compositeChart.selectAll('g.sub')[0][n]);

            subChart.expectPlotSymbolsToHaveClass = function (className) {
                subChart.selectAll('path.symbol').each(function () {
                    expect(d3.select(this).classed(className)).toBeTruthy();
                });
            };

            subChart.expectPlotSymbolsToHaveSize = function (size) {
                var highlightedSize = Math.pow(size, 2);
                var highlightedPath = d3.svg.symbol().size(highlightedSize)();
                subChart.selectAll('path.symbol').each(function () {
                    expect(d3.select(this).attr('d')).toMatchPath(highlightedPath);
                });
            };

            subChart.expectPlotSymbolsNotToHaveClass = function (className) {
                subChart.selectAll('path.symbol').each(function () {
                    expect(d3.select(this).classed(className)).toBeFalsy();
                });
            };

            return subChart;
        }
    });
});

