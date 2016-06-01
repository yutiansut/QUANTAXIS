/* global appendChartID, loadBoxPlotFixture */
describe('dc.boxPlot', function () {
    var id, chart;
    var data, dimension, group;

    beforeEach(function () {
        data = crossfilter(loadBoxPlotFixture());

        dimension = data.dimension(function (d) { return d.countrycode; });
        group = dimension.group().reduce(
            function (p, v) { p.push(+v.value); return p; },
            function (p, v) { p.splice(p.indexOf(+v.value), 1); return p; },
            function () { return []; }
        );

        id = 'boxplot';
        appendChartID(id);

        chart = dc.boxPlot('#' + id);
        chart
            .dimension(dimension)
            .group(group)
            .width(300)
            .height(144)
            .margins({top: 0, right: 0, bottom: 0, left: 0})
            .boxPadding(0)
            .transitionDuration(0)
            .y(d3.scale.linear().domain([0, 144]))
            .ordinalColors(['#01','#02']);
    });

    describe('rendering the box plot', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create a non-empty SVG node', function () {
            expect(chart.svg().empty()).toBeFalsy();
        });

        it('should create one outlier circle per outlier', function () {
            expect(chart.selectAll('circle.outlier').size()).toBe(2);
        });

        it('should create an offset box for each dimension in the group', function () {
            expect(box(0).attr('transform')).toMatchTranslate(50,0);
            expect(box(1).attr('transform')).toMatchTranslate(150,0);
        });

        it('should correctly place median line', function () {
            expect(box(1).selectAll('line.median').attr('y1')).toBe('100');
            expect(box(1).selectAll('line.median').attr('y2')).toBe('100');
        });

        it('should set the median value correctly', function () {
            expect(box(1).boxText(1).text()).toBe('44');
        });

        it('should place the left box line at the x origin', function () {
            expect(box(1).select('rect.box').attr('x')).toBe('0');
        });

        describe('the width of the box plot', function () {
            it('should default to being based on the rangeBand', function () {
                expect(box(1).select('rect.box').attr('width')).toBe('100');
            });

            it('should be settable to a number', function () {
                chart.boxWidth(150).render();
                expect(box(1).select('rect.box').attr('width')).toBe('150');
            });

            it('should be settable to a function', function () {
                chart.boxWidth(function (innerChartWidth, xUnits) {
                    return innerChartWidth / (xUnits + 2);
                }).render();
                expect(box(1).select('rect.box').attr('width')).toBe('75');
            });
        });

        describe('the tickFormat of the box plot', function () {
            it('should default to whole number', function () {
                expect(box(1).boxText(1).text()).toBe('44');
                expect(box(1).whiskerText(0).text()).toBe('22');
                expect(box(1).whiskerText(1).text()).toBe('66');
            });

            it('should be settable to a d3.format', function () {
                chart.tickFormat(d3.format('.2f')).render();
                expect(box(1).boxText(1).text()).toBe('44.00');
                expect(box(1).whiskerText(0).text()).toBe('22.00');
                expect(box(1).whiskerText(1).text()).toBe('66.00');
            });
        });

        it('should place interquartile range lines after the first and before the fourth quartile', function () {
            expect(box(1).select('rect.box').attr('y')).toBe('94.5');
            expect(box(1).select('rect.box').attr('height')).toBe('16.5');
        });

        it('should label the interquartile range lines using their calculated values', function () {
            expect(box(1).boxText(0).text()).toBe('33');
            expect(box(1).boxText(2).text()).toBe('50');
        });

        it('should place the whiskers at 1.5x the interquartile range', function () {
            expect(box(1).whiskerLine(0).attr('y1')).toBe('122');
            expect(box(1).whiskerLine(0).attr('y2')).toBe('122');
            expect(box(1).whiskerLine(1).attr('y1')).toBeWithinDelta(78);
            expect(box(1).whiskerLine(1).attr('y2')).toBeWithinDelta(78);
        });

        it('should label the whiskers using their calculated values', function () {
            expect(box(1).whiskerText(0).text()).toBe('22');
            expect(box(1).whiskerText(1).text()).toBe('66');
        });

        it('should assign a fill color to the boxes', function () {
            expect(box(0).select('rect.box').attr('fill')).toBe('#01');
            expect(box(1).select('rect.box').attr('fill')).toBe('#02');
        });

        describe('when a box has no data', function () {
            var firstBox;

            beforeEach(function () {
                firstBox = chart.select('g.box').node();
                var otherDimension = data.dimension(function (d) { return d.countrycode; });
                otherDimension.filter('US');
                chart.redraw();
            });

            it('should not attempt to render that box', function () {
                expect(chart.selectAll('g.box').size()).toBe(1);
            });

            it('should not animate the removed box into another box', function () {
                expect(chart.select('g.box').node()).not.toBe(firstBox);
            });

            describe('with elasticX enabled', function () {
                beforeEach(function () {
                    chart.elasticX(true).render();
                });

                it('should not represent the box in the chart domain', function () {
                    expect(chart.selectAll('.axis.x .tick').size()).toBe(1);
                });
            });

            describe('when elasticX is disabled', function () {
                beforeEach(function () {
                    chart.elasticX(false).render();
                });

                it('should represent the box in the chart domain', function () {
                    expect(chart.selectAll('.axis.x .tick').size()).toBe(2);
                });
            });
        });
    });

    describe('events', function () {
        beforeEach(function () {
            chart.render();
        });

        describe('filtering the box plot', function () {
            beforeEach(function () {
                chart.filter('CA').redraw();
            });

            it('should select the boxes corresponding to the filtered value', function () {
                box(0).each(function (d) {
                    expect(d3.select(this).classed('selected')).toBeTruthy();
                });
            });

            it('should deselect the boxes not corresponding to the filtered value', function () {
                box(1).each(function (d) {
                    expect(d3.select(this).classed('deselected')).toBeTruthy();
                });
            });
        });

        describe('clicking on a box', function () {
            beforeEach(function () {
                box(0).on('click').call(chart, box(0).datum());
            });

            it('should apply a filter to the chart', function () {
                expect(chart.hasFilter('CA')).toBeTruthy();
            });
        });
    });

    function box (n) {
        var nthBox = d3.select(chart.selectAll('g.box')[0][n]);
        nthBox.boxText = function (n) {
            return d3.select(this.selectAll('text.box')[0][n]);
        };
        nthBox.whiskerLine = function (n) {
            return d3.select(this.selectAll('line.whisker')[0][n]);
        };
        nthBox.whiskerText = function (n) {
            return d3.select(this.selectAll('text.whisker')[0][n]);
        };
        return nthBox;
    }
});

