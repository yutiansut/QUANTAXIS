/* global appendChartID, loadDateFixture, makeDate */
describe('dc.lineChart', function () {
    var id, chart, data;
    var dimension, group;

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        dimension = data.dimension(function (d) { return d3.time.day.utc(d.dd); });
        group = dimension.group();

        id = 'line-chart';
        appendChartID(id);

        chart = dc.lineChart('#' + id);
        chart.dimension(dimension).group(group)
            .width(1100).height(200)
            .x(d3.time.scale.utc().domain([makeDate(2012, 1, 1), makeDate(2012, 11, 31)]))
            .transitionDuration(0);
    });

    describe('rendering', function () {
        beforeEach(function () {
            chart.render();
        });

        describe('with a specified dash style', function () {
            beforeEach(function () {
                chart.dashStyle([3, 1, 1, 1]).render();
            });

            it('should be dash-dot-dot-dot to match the specified style', function () {
                expect(chart.selectAll('path.line').attr('stroke-dasharray')).toEqualIntList('3,1,1,1');
            });
        });

        describe('render data markers', function () {
            beforeEach(function () {
                chart.dotRadius(5)
                    .brushOn(false)
                    .renderDataPoints({}).render();

            });

            it('should use default options', function () {
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    expect(dot.style('fill-opacity')).toBeWithinDelta(0.8);
                    expect(dot.style('stroke-opacity')).toBeWithinDelta(0.8);
                    expect(dot.attr('r')).toBe('2');
                });
            });

            it('should use supplied options', function () {
                chart.renderDataPoints({radius: 3, fillOpacity: 1, strokeOpacity: 1})
                    .render();
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    expect(dot.style('fill-opacity')).toBe('1');
                    expect(dot.style('stroke-opacity')).toBe('1');
                    expect(dot.attr('r')).toBe('3');
                });
            });

            it('should change the radius on mousemove', function () {
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    dot.on('mousemove').call(this);
                    expect(dot.attr('r')).toBe('5');
                });
            });

            it('should revert to original radius on mouseout', function () {
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    dot.on('mousemove').call(this);
                    dot.on('mouseout').call(this);
                    expect(dot.attr('r')).toBe('2');
                });
            });

            describe('hiding all data markers', function () {
                beforeEach(function () {
                    chart.renderDataPoints(false).render();
                });

                it('should not change the default opacity and radius', function () {
                    chart.selectAll('circle.dot').each(function () {
                        expect(d3.select(this).style('fill-opacity')).toBeWithinDelta(1e-6);
                        expect(d3.select(this).style('stroke-opacity')).toBeWithinDelta(1e-6);
                    });
                });

                it('should not change showing the data point on mousemove', function () {
                    chart.selectAll('circle.dot').each(function () {
                        var dot = d3.select(this);
                        dot.on('mousemove').call(this);
                        expect(dot.style('fill-opacity')).toBeWithinDelta(0.8);
                        expect(dot.style('stroke-opacity')).toBeWithinDelta(0.8);
                    });
                });

                it('should not change returning to extremely low opacity on hover out', function () {
                    chart.selectAll('circle.dot').each(function () {
                        var dot = d3.select(this);
                        dot.on('mousemove').call(this);
                        dot.on('mouseout').call(this);
                        expect(dot.style('fill-opacity')).toBeWithinDelta(1e-6);
                        expect(dot.style('stroke-opacity')).toBeWithinDelta(1e-6);
                    });
                });
            });
        });

        describe('title rendering', function () {
            beforeEach(function () {
                chart.renderTitle(false);
                chart.render();
            });

            it('should not render tooltips when boolean flag is false', function () {
                expect(chart.select('.sub._0 .dc-tooltip._0 .dot').empty()).toBeTruthy();
                expect(chart.select('.sub._1 .dc-tooltip._0 .dot').empty()).toBeTruthy();
            });
        });

        describe('data point highlights and refs off', function () {
            beforeEach(function () {
                chart.title(function (d) { return d.value; });
                chart.brushOn(false).xyTipsOn(false).render();
            });
            it('should not generate per data points', function () {
                expect(chart.selectAll('circle.dot').size()).toBe(0);
            });
            it('should not generate x and y refs', function () {
                expect(chart.selectAll('path.xRef').size()).toBe(0);
                expect(chart.selectAll('path.yRef').size()).toBe(0);
            });
        });

        describe('data point highlights', function () {
            beforeEach(function () {
                chart.title(function (d) { return d.value; });
                chart.brushOn(false).dotRadius(10).render();
            });
            it('should not generate a chart brush', function () {
                expect(chart.selectAll('g.brush').empty()).toBeTruthy();
            });

            it('should be generated per data point', function () {
                expect(chart.selectAll('circle.dot').size()).toBe(6);
            });

            it('should have configurable radius', function () {
                chart.selectAll('circle.dot').each(function () {
                    expect(d3.select(this).attr('r')).toBe('10');
                });
            });

            it('should be have extremely low opacity by default', function () {
                chart.selectAll('circle.dot').each(function () {
                    expect(d3.select(this).style('fill-opacity')).toBeWithinDelta(1e-6);
                    expect(d3.select(this).style('stroke-opacity')).toBeWithinDelta(1e-6);
                });
            });

            it('should become visible when hovered over', function () {
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    dot.on('mousemove').call(this);
                    expect(dot.style('fill-opacity')).toBeWithinDelta(0.8);
                    expect(dot.style('stroke-opacity')).toBeWithinDelta(0.8);
                });
            });

            it('should return to extremely low opacity on hover out', function () {
                chart.selectAll('circle.dot').each(function () {
                    var dot = d3.select(this);
                    dot.on('mousemove').call(this);
                    dot.on('mouseout').call(this);
                    expect(dot.style('fill-opacity')).toBeWithinDelta(1e-6);
                    expect(dot.style('stroke-opacity')).toBeWithinDelta(1e-6);
                });
            });

            it('should render titles on to each circle', function () {
                chart.selectAll('g._0 circle.dot').each(function (d) {
                    expect(+d3.select(this).select('title').text()).toBe(d.data.value);
                });
            });

            describe('ref lines', function () {
                it('should generate lines that are hidden by default', function () {
                    expect(chart.select('path.xRef').style('display')).toBe('none');
                    expect(chart.select('path.yRef').style('display')).toBe('none');
                });

                it('should have a stroke dash', function () {
                    expect(chart.selectAll('path.xRef').attr('stroke-dasharray')).toEqualIntList('5,5');
                    expect(chart.selectAll('path.yRef').attr('stroke-dasharray')).toEqualIntList('5,5');
                });

                describe('when dot is hovered over', function () {
                    describe('for vertical ref lines', function () {
                        var x;
                        beforeEach(function () {
                            var dot = chart.select('circle.dot');
                            dot.on('mousemove').call(dot[0][0]);
                            x = dot.attr('cx');
                        });

                        it('shows the ref line from the bottom of the graph', function () {
                            var path = 'M' + x + ' 160 L ' + x + ' 107';
                            expect(chart.select('path.xRef').attr('d')).toMatchPath(path);
                            expect(chart.select('path.xRef').attr('display')).not.toBe('none');
                        });
                    });

                    describe('for horizontal ref lines', function () {
                        describe('for a left y-axis chart', function () {
                            var x;
                            beforeEach(function () {
                                var dot = chart.select('circle.dot');
                                dot.on('mousemove').call(dot[0][0]);
                                x = dot.attr('cx');
                            });

                            it('shows the ref line on the left', function () {
                                var path = 'M0 107 L ' + x + ' 107';
                                expect(chart.select('path.yRef').attr('d')).toMatchPath(path);
                                expect(chart.select('path.yRef').attr('display')).not.toBe('none');
                            });
                        });

                        describe('for a right y-axis chart', function () {
                            var x;
                            beforeEach(function () {
                                chart.useRightYAxis(true).render();
                                var dot = chart.select('circle.dot');
                                dot.on('mousemove').call(dot[0][0]);
                                x = dot.attr('cx');
                            });

                            it('shows the ref line on the right', function () {
                                var path = 'M1020 107L' + x + ' 107';
                                expect(chart.select('path.yRef').attr('d')).toMatchPath(path); //"M1020 107L405 107");
                                expect(chart.select('path.yRef').attr('display')).not.toBe('none');
                            });
                        });
                    });
                });
            });
        });

        describe('undefined points', function () {
            beforeEach(function () {
                chart.defined(function (d) { return d.x.valueOf() !== makeDate(2012, 5, 10).getTime(); });
                chart.brushOn(false).render();
            });

            it('should not show line where not defined', function () {
                expect(chart.select('path.line').attr('d').indexOf('M', 1)).not.toBe(-1);
            });

            it('should not draw dots on undefined points', function () {
                expect(chart.selectAll('.dot').size()).toBe(5);
            });
        });

        describe('with chart area enabled', function () {
            beforeEach(function () {
                chart.renderArea(true).render();
            });

            it('should draw the chart line', function () {
                expect(chart.select('path.line').attr('d')).toMatchPath('M348,107 L390,107 L397,0 L461,107 L488,53 L583,53');
            });

            it('should draw the chart area', function () {
                expect(chart.select('path.area').attr('d')).toMatchPath('M348,107 L390,107 L397,0 L461,107 L488,53 L583,' +
                    '53 L583,160 L488,160 L461,160 L397,160 L390,160 L348,160Z');
            });
        });

        describe('with an ordinal x domain', function () {
            beforeEach(function () {
                var stateDimension = data.dimension(function (d) { return d.state; });
                var stateGroup = stateDimension.group();

                chart.dimension(stateDimension)
                    .group(stateGroup)
                    .xUnits(dc.units.ordinal)
                    .x(d3.scale.ordinal().domain(['California', 'Colorado', 'Delaware', 'Mississippi', 'Oklahoma', 'Ontario']))
                    .render();
            });

            it('should automatically disable the brush', function () {
                expect(chart.brushOn()).toBeFalsy();
            });

            it('should generate an ordinal path', function () {
                expect(chart.select('path.line').attr('d')).toMatchPath('M85,0L255,107L425,107L595,53L765,107L935,53');
            });
        });

        describe('with stacked data', function () {
            describe('with positive data', function () {
                beforeEach(function () {
                    var idGroup = dimension.group().reduceSum(function (d) { return d.id; });
                    var valueGroup = dimension.group().reduceSum(function (d) { return d.value; });

                    chart.dimension(dimension)
                        .brushOn(false)
                        .x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]))
                        .group(idGroup, 'stack 0')
                        .title('stack 0', function (d) { return 'stack 0: ' + d.value; })
                        .stack(valueGroup, 'stack 1')
                        .title('stack 1', function (d) { return 'stack 1: ' + d.value; })
                        .stack(valueGroup, 'stack 2')
                        .elasticY(true)
                        .render();
                });

                it('should render the correct number of lines', function () {
                    expect(chart.selectAll('path.line').size()).toBe(3);
                });

                it('should set the path for stack 0 line', function () {
                    expect(chart.select('g._0 path.line').attr('d')).toMatchPath('M58 159L222 157L246 150L492 158L597 151L961 153');
                });

                it('should set the path for stack 1 line', function () {
                    expect(chart.select('g._1 path.line').attr('d')).toMatchPath('M58 134L222 119L246 75L492 133L597 120L961 109');
                });

                it('should set the path for stack 2 line', function () {
                    expect(chart.select('g._2 path.line').attr('d')).toMatchPath('M58 109L222 81L246 0L492 108L597 89L961 65');
                });

                it('should have its own title accessor', function () {
                    expect(chart.title()({value: 1})).toBe('stack 0: 1');
                    expect(chart.title('stack 0')({value: 2})).toBe('stack 0: 2');
                    expect(chart.title('stack 1')({value: 3})).toBe('stack 1: 3');
                });

                it('should have titles rendered for extra stacks', function () {
                    chart.selectAll('g._1 circle.dot').each(function (d) {
                        expect(d3.select(this).select('title').text()).toBe('stack 1: ' + d.data.value);
                    });
                });

                it('should default to first stack title for untitled stacks', function () {
                    chart.selectAll('g._2 circle.dot').each(function (d) {
                        expect(d3.select(this).select('title').text()).toBe('stack 0: ' + d.data.value);
                    });
                });

                describe('with chart area enabled', function () {
                    beforeEach(function () {
                        chart.renderArea(true).render();
                    });

                    it('should render the correct number of areas', function () {
                        expect(chart.selectAll('path.area').size()).toBe(3);
                    });

                    it('should set the area for stack 0', function () {
                        expect(chart.select('g._0 path.area').attr('d')).toMatchPath('M58 159L222 157L246 150L492 158L597 ' +
                            '151L961 153L961 160L597 160L492 160L246 160L222 160L58 160Z');
                    });

                    it('should set the area for stack 1', function () {
                        expect(chart.select('g._1 path.area').attr('d')).toMatchPath('M58 134L222 119L246 75L492 133L597 ' +
                            '120L961 109L961 153L597 151L492 158L246 150L222 157L58 159Z');
                    });

                    it('should set the area for stack 2', function () {
                        expect(chart.select('g._2 path.area').attr('d')).toMatchPath('M58 109L222 81L246 0L492 108L597 89L961 ' +
                            '65L961 109L597 120L492 133L246 75L222 119L58 134Z');
                    });

                    it('should draw tooltip dots on top of paths and areas', function () {
                        var list = chart.selectAll('circle.dot, path.line, path.area');

                        var indexOfLastLine = list[0].indexOf(list.filter('path.line')[0][2]);
                        var indexOfLastArea = list[0].indexOf(list.filter('path.area')[0][2]);
                        var indexOfDot = list[0].indexOf(list.filter('circle.dot')[0][0]);

                        expect(indexOfDot).toBeGreaterThan(indexOfLastArea);
                        expect(indexOfDot).toBeGreaterThan(indexOfLastLine);
                    });

                    it('should draw tooltip ref lines on top of paths', function () {
                        var list = chart.selectAll('path.yRef, path.xRef, path.line, path.area');

                        var indexOfLastLine = list[0].indexOf(list.filter('path.line')[0][2]);
                        var indexOfLastArea = list[0].indexOf(list.filter('path.area')[0][2]);

                        var indexOfFirstYRef = list[0].indexOf(list.filter('path.yRef')[0][0]);
                        var indexOfFirstXRef = list[0].indexOf(list.filter('path.xRef')[0][0]);

                        expect(indexOfLastLine).toBeLessThan(indexOfFirstXRef);
                        expect(indexOfLastLine).toBeLessThan(indexOfFirstYRef);

                        expect(indexOfLastArea).toBeLessThan(indexOfFirstXRef);
                        expect(indexOfLastArea).toBeLessThan(indexOfFirstYRef);
                    });

                });

                describe('stack hiding', function () {
                    describe('first stack', function () {
                        beforeEach(function () {
                            chart.hideStack('stack 0').render();
                        });

                        it('should hide the stack', function () {
                            expect(chart.select('g._0 path.line').attr('d')).toMatchPath('M58 133L222 120L246 80L492 133L597 127L961 113');
                        });

                        it('should show the stack', function () {
                            chart.showStack('stack 0').render();
                            expect(chart.select('g._0 path.line').attr('d')).toMatchPath('M58 159L222 157L246 150L492 158L597 151L961 153');
                        });
                    });

                    describe('any other stack', function () {
                        beforeEach(function () {
                            chart.title('stack 2', function (d) { return 'stack 2: ' + d.value; });
                            chart.hideStack('stack 1').render();
                        });

                        it('should hide the stack', function () {
                            expect(chart.select('g._1 path.line').attr('d')).toMatchPath('M58 112L222 83L246 0L492 108L597 85L961 64');
                        });

                        it('should show the stack', function () {
                            chart.showStack('stack 1').render();
                            expect(chart.select('g._1 path.line').attr('d')).toMatchPath('M58 134L222 119L246 75L492 133L597 120L961 109');
                        });

                        it('should color chart dots the same as line paths', function () {
                            var lineColor = chart.select('g._1 path.line').attr('stroke');
                            var circleColor = chart.select('g._1 circle.dot').attr('fill');
                            expect(lineColor).toEqual(circleColor);
                        });

                        it('should still show the title for a visible stack', function () {
                            chart.selectAll('g._1 circle.dot').each(function (d) {
                                expect(d3.select(this).select('title').text()).toBe('stack 2: ' + d.data.value);
                            });
                        });
                    });

                    describe('hiding all the stacks', function () {
                        beforeEach(function () {
                            chart.hideStack('stack 0')
                                .hideStack('stack 1')
                                .hideStack('stack 2')
                                .render();
                        });

                        it('should show a blank graph', function () {
                            expect(chart.selectAll('path.line').size()).toBe(0);
                        });
                    });
                });
            });

            describe('with negative data', function () {
                beforeEach(function () {
                    var negativeGroup = dimension.group().reduceSum(function (d) { return d.nvalue; });

                    chart.group(negativeGroup).stack(negativeGroup).stack(negativeGroup);
                    chart.x(d3.time.scale.utc().domain([makeDate(2012, 4, 20), makeDate(2012, 7, 15)]));

                    chart.margins({top: 30, right: 50, bottom: 30, left: 30})
                        .renderArea(true)
                        .yAxisPadding(5)
                        .elasticY(true)
                        .yAxis().ticks(5);

                    chart.render();
                });

                it('should generate a line and area for each stack', function () {
                    expect(chart.selectAll('path.line').size()).toBe(3);
                    expect(chart.selectAll('path.area').size()).toBe(3);
                });

                it('should generate negative lines and area for stack 0', function () {
                    expect(chart.select('g._0 path.line').attr('d')).toMatchPath('M58 81L222 81L246 92L492 79L597 52L961 67');
                    expect(chart.select('g._0 path.area').attr('d')).toMatchPath('M58 81L222 81L246 92L492 79L597 52L961 ' +
                        '67L961 73L597 73L492 73L246 73L222 73L58 73Z');
                });

                it('should generate negative lines and area for stack 1', function () {
                    expect(chart.select('g._1 path.line').attr('d')).toMatchPath('M58 88L222 88L246 111L492 84L597 31L961 61');
                    expect(chart.select('g._1 path.area').attr('d')).toMatchPath('M58 88L222 88L246 111L492 84L597 31L961 ' +
                        '61L961 67L597 52L492 79L246 92L222 81L58 81Z');
                });

                it('should generate y axis domain dynamically', function () {
                    var nthText = function (n) { return d3.select(chart.selectAll('g.y text')[0][n]); };

                    expect(nthText(0).text()).toBe('-20');
                    expect(nthText(1).text()).toBe('0');
                    expect(nthText(2).text()).toBe('20');
                });
            });
        });

        describe('legend hovering', function () {
            var firstItem;

            beforeEach(function () {
                chart.stack(group)
                    .legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
                    .renderArea(true)
                    .render();

                firstItem = chart.select('g.dc-legend g.dc-legend-item');
                firstItem.on('mouseover')(firstItem.datum());
            });

            describe('when a legend item is hovered over', function () {
                it('should highlight corresponding lines and areas', function () {
                    expect(nthLine(0).classed('highlight')).toBeTruthy();
                    expect(nthArea(0).classed('highlight')).toBeTruthy();
                });

                it('should fade out non-corresponding lines and areas', function () {
                    expect(nthLine(1).classed('fadeout')).toBeTruthy();
                    expect(nthArea(1).classed('fadeout')).toBeTruthy();
                });
            });

            describe('when a legend item is hovered out', function () {
                it('should remove highlighting from corresponding lines and areas', function () {
                    firstItem.on('mouseout')(firstItem.datum());
                    expect(nthLine(0).classed('highlight')).toBeFalsy();
                    expect(nthArea(0).classed('highlight')).toBeFalsy();
                });

                it('should fade in non-corresponding lines and areas', function () {
                    firstItem.on('mouseout')(firstItem.datum());
                    expect(nthLine(1).classed('fadeout')).toBeFalsy();
                    expect(nthArea(1).classed('fadeout')).toBeFalsy();
                });
            });

            function nthLine (n) {
                return d3.select(chart.selectAll('path.line')[0][n]);
            }

            function nthArea (n) {
                return d3.select(chart.selectAll('path.area')[0][n]);
            }
        });

        describe('filtering', function () {
            beforeEach(function () {
                chart.filter([makeDate(2012, 5, 1), makeDate(2012, 5, 30)]).redraw();
            });

            it('should set the chart filter', function () {
                expect(chart.filter()).toEqual([makeDate(2012, 5, 1), makeDate(2012, 5, 30)]);
            });

            it('should set the filter printer', function () {
                expect(chart.filterPrinter()).not.toBeNull();
            });

            it('should not generate tooltip circles with the default brush', function () {
                expect(chart.selectAll('circle.dot').empty()).toBeTruthy();
            });

            describe('when a brush is defined', function () {
                it('should position the brush with an offset', function () {
                    expect(chart.select('g.brush').attr('transform')).toMatchTranslate(chart.margins().left, 10);
                });

                it('should create a fancy brush resize handle', function () {
                    chart.select('g.brush').selectAll('.resize path').each(function (d, i) {
                        if (i === 0) {
                            expect(d3.select(this).attr('d'))
                                .toMatchPath('M0.5,53 A6,6 0 0 1 6.5,59 V100 A6,6 0 0 1 0.5,106 ZM2.5,61 V98 M4.5,61 V98');
                        } else {
                            expect(d3.select(this).attr('d'))
                                .toMatchPath('M-0.5,53 A6,6 0 0 0 -6.5,59 V100 A6,6 0 0 0 -0.5,106 ZM-2.5,61 V98 M-4.5,61 V98');
                        }
                    });
                });

                it('should stretch the background', function () {
                    expect(chart.select('g.brush rect.background').attr('width')).toBe('1020');
                });

                it('should set the background height to the chart height', function () {
                    expect(chart.select('g.brush rect.background').attr('height')).toBe('160');
                });

                it('should set extent height to the chart height', function () {
                    expect(chart.select('g.brush rect.extent').attr('height')).toBe('160');
                });

                it('should set extent width based on filter set', function () {
                    expect(chart.select('g.brush rect.extent').attr('width')).toBeWithinDelta(88, 1);
                });

                it('should not have an area path', function () {
                    expect(chart.selectAll('path.area').empty()).toBeTruthy();
                });

                it('should set the dash style to solid', function () {
                    expect(chart.selectAll('path.line').attr('stroke-dasharray')).toBeNull();
                });
            });
        });
        describe('changing data', function () {
            var stateDimension;
            beforeEach(function () {
                chart.brushOn(false)
                    .title(function (d) { return d.value; })
                    .render();
                stateDimension = data.dimension(function (d) { return d.state; });
                stateDimension.filter('CA');
                chart.redraw();
            });

            it('should update dot titles', function () {
                chart.selectAll('g._0 circle.dot').each(function (d) {
                    expect(d3.select(this).select('title').size()).toBe(1);
                    expect(+d3.select(this).select('title').text()).toBe(d.data.value);
                });
            });

            afterEach(function () {
                stateDimension.filter(null);
            });
        });
    });
    describe('change color', function () {
        beforeEach(function () {
            chart.brushOn(false)
                .ordinalColors(['#FF0000'])
                .colorAccessor(function () { return 0; })
                .render();
        });
        it('updates dot colors', function () {
            expect(chart.select('circle.dot')[0][0].attributes.fill.value).toMatch(/#FF0000/i);
        });
    });
});
