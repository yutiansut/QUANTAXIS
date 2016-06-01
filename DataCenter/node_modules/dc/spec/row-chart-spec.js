/* global appendChartID, loadDateFixture, makeDate */
describe('dc.rowChart', function () {
    var id, chart;
    var data, dimension, nvdimension;
    var positiveGroupHolder = {groupType: 'positive signed'};
    var negativeGroupHolder = {groupType: 'negative signed'};
    var mixedGroupHolder = {groupType: 'mixed signed'};
    var largerGroupHolder = {groupType: 'larger'};

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        dimension = data.dimension(function (d) { return +d.value; });

        positiveGroupHolder.group = dimension.group().reduceSum(function (d) {return Math.abs(+d.nvalue);});
        positiveGroupHolder.dimension = dimension;
        negativeGroupHolder.group = dimension.group().reduceSum(function (d) {return -Math.abs(+d.nvalue);});
        negativeGroupHolder.dimension = dimension;
        mixedGroupHolder.group = dimension.group().reduceSum(function (d) {return +d.nvalue;});
        mixedGroupHolder.dimension = dimension;

        nvdimension = data.dimension(function (d) { return +d.nvalue; });
        largerGroupHolder.group = nvdimension.group().reduceSum(function (d) {return +d.value;});
        largerGroupHolder.dimension = nvdimension;

        id = 'row-chart';
        appendChartID(id);

        chart = dc.rowChart('#' + id);
        chart.dimension(dimension)
            .width(600).height(200).gap(10)
            .transitionDuration(0);
    });

    describe('enabling the chart title and label with a value accessor', function () {
        beforeEach(function () {
            chart.group(mixedGroupHolder.group);
            chart.valueAccessor(function (d) {
                return d.value + 100;
            }).renderLabel(true).renderTitle(true).render();
        });

        it('should use the default function to dynamically generate the label', function () {
            expect(chart.select('text.row').text()).toBe('22');
        });

        it('should use the default function to dynamically generate the title', function () {
            expect(chart.select('g.row title').text()).toBe('22: 108');
        });
    });

    describe('with a logarithmic X axis and positive data', function () {
        beforeEach(function () {
            chart.group(positiveGroupHolder.group);
            chart.elasticX(false);
            chart.x(d3.scale.log());
            chart.render();
        });

        it('should render valid rect widths', function () {
            expect(chart.select('g.row rect').attr('width')).toBeWithinDelta(1, 0.5);
        });
    });

    describe('with a fixedBarHeight', function () {
        beforeEach(function () {
            chart.group(positiveGroupHolder.group);
            chart.elasticX(false);
            chart.x(d3.scale.log());
            chart.fixedBarHeight(10);
            chart.render();
        });

        it('should render fixed rect height', function () {
            expect(chart.select('g.row rect').attr('height')).toBeWithinDelta(10, 0.0);
        });
    });

    function itShouldBehaveLikeARowChartWithGroup (groupHolder, N) {
        describe('for ' + groupHolder.groupType + ' data', function () {
            beforeEach(function () {
                chart.group(groupHolder.group);
            });

            describe('rendering the row chart', function () {
                beforeEach(function () {
                    chart.render();
                });

                it('should create a root svg node', function () {
                    expect(chart.select('svg').size()).toBe(1);
                });

                it('should create a row group for each datum', function () {
                    expect(chart.selectAll('svg g g.row').size()).toBe(N);
                });

                it('should number each row sequentially with classes', function () {
                    chart.selectAll('svg g g.row').each(function (r, i) {
                        expect(d3.select(this).attr('class')).toBe('row _' + i);
                    });
                });

                it('should fill each row rect with pre-defined colors', function () {
                    expect(d3.select(chart.selectAll('g.row rect')[0][0]).attr('fill')).toBe('#3182bd');
                    expect(d3.select(chart.selectAll('g.row rect')[0][1]).attr('fill')).toBe('#6baed6');
                    expect(d3.select(chart.selectAll('g.row rect')[0][2]).attr('fill')).toBe('#9ecae1');
                    expect(d3.select(chart.selectAll('g.row rect')[0][3]).attr('fill')).toBe('#c6dbef');
                    expect(d3.select(chart.selectAll('g.row rect')[0][4]).attr('fill')).toBe('#e6550d');
                });

                it('should create a row label from the data for each row', function () {
                    expect(chart.selectAll('svg text.row').size()).toBe(N);

                    chart.selectAll('svg g text.row').call(function (t) {
                        expect(+t.text()).toBe(t.datum().key);
                    });
                });

                describe('row label vertical position', function () {
                    var labels, rows;
                    beforeEach(function () {
                        labels = chart.selectAll('svg text.row');
                        rows = chart.selectAll('g.row rect');
                    });

                    function itShouldVerticallyCenterLabelWithinRow (i) {
                        it('should place label ' + i + ' within row ' + i, function () {
                            var rowpos = rows[0][i].getBoundingClientRect(),
                                textpos = labels[0][i].getBoundingClientRect();
                            expect((textpos.top + textpos.bottom) / 2)
                                .toBeWithinDelta((rowpos.top + rowpos.bottom) / 2, 2);
                        });
                    }
                    for (var i = 0; i < N ; ++i) {
                        itShouldVerticallyCenterLabelWithinRow(i);
                    }
                });

                describe('re-rendering the chart', function () {
                    beforeEach(function () {
                        chart.render();
                    });

                    it('should leave a single instance of the chart', function () {
                        expect(d3.selectAll('#row-chart svg').size()).toBe(1);
                    });
                });
            });

            describe('chart filters', function () {
                beforeEach(function () {
                    chart.render();
                    d3.select('#' + id).append('span').classed('filter', true);
                });

                it('should not have filter by default', function () {
                    expect(chart.hasFilter()).toBeFalsy();
                });

                it('should not modify the underlying crossfilter group', function () {
                    var oldGroupData = chart.group().all().slice(0);
                    chart.ordering(dc.pluck('value'));
                    chart.filter('66').render();

                    expect(chart.group().all().length).toBe(oldGroupData.length);
                    for (var i = 0; i < oldGroupData.length; i++) {
                        expect(chart.group().all()[i]).toBe(oldGroupData[i]);
                    }
                });

                describe('filtering a row', function () {
                    beforeEach(function () {
                        chart.filter('66');
                        chart.render();
                    });

                    it('should apply a filter to the chart', function () {
                        expect(chart.filter()).toBe('66');
                        expect(chart.hasFilter()).toBeTruthy();
                    });

                    it('should highlight any selected rows', function () {
                        chart.filter('22');
                        chart.render();
                        chart.selectAll('g.row rect').each(function (d) {
                            if (d.key === 66 || d.key === 22) {
                                expect(d3.select(this).classed('selected')).toBeTruthy();
                                expect(d3.select(this).classed('deselected')).toBeFalsy();
                            } else {
                                expect(d3.select(this).classed('deselected')).toBeTruthy();
                                expect(d3.select(this).classed('selected')).toBeFalsy();
                            }
                        });
                    });

                    it('should generate filter info in a filter-classed element', function () {
                        expect(chart.select('span.filter').style('display')).not.toBe('none');
                        expect(chart.select('span.filter').text()).toBe('66');
                    });

                    describe('removing filters', function () {
                        beforeEach(function () {
                            chart.filterAll();
                            chart.render();
                        });

                        it('should remove highlighting', function () {
                            chart.selectAll('g.row rect').each(function (d) {
                                expect(d3.select(this).classed('deselected')).toBeFalsy();
                                expect(d3.select(this).classed('selected')).toBeFalsy();
                            });
                        });
                    });
                });
            });

            describe('filtering related dimensions', function () {
                beforeEach(function () {
                    chart.render();
                    data.dimension(function (d) { return d.status; }).filter('E');
                });

                it('should preserve the labels', function () {
                    chart.selectAll('svg g text.row').each(function () {
                        expect(d3.select(this).text()).not.toBe('');
                    });
                });
            });

            describe('clicking on a row', function () {
                beforeEach(function () {
                    chart.render();
                    chart.onClick(chart.group().all()[0]);
                });

                it('should filter the corresponding group', function () {
                    expect(chart.filter()).toBe(chart.group().all()[0].key);
                });

                describe('clicking again', function () {
                    beforeEach(function () {
                        chart.onClick(chart.group().all()[0]);
                    });

                    it('should reset the filter', function () {
                        expect(chart.filter()).toBe(null);
                    });
                });
            });

            describe('specifying a group ordering', function () {
                beforeEach(function () {
                    chart.render();
                });

                it('should order values when by value', function () {
                    chart.ordering(dc.pluck('value'));
                    expect(chart.data().map(dc.pluck('value')).sort(d3.ascending)).toEqual(chart.data().map(dc.pluck('value')));
                });

                it('should order keys when by keys', function () {
                    chart.ordering(dc.pluck('key'));
                    expect(chart.data().map(dc.pluck('key')).sort(d3.ascending)).toEqual(chart.data().map(dc.pluck('key')));
                });
            });

            describe('redrawing after an empty selection', function () {
                beforeEach(function () {
                    chart.render();
                    // fixme: huh?  this isn't even the right data type
                    groupHolder.dimension.filter([makeDate(2010, 0, 1), makeDate(2010, 0, 3)]);
                    chart.redraw();
                    groupHolder.dimension.filter([makeDate(2012, 0, 1), makeDate(2012, 11, 30)]);
                    chart.redraw();
                });

                it('should restore the row chart', function () {
                    chart.selectAll('g.row rect').each(function (p) {
                        expect(d3.select(this).attr('width').indexOf('NaN') < 0).toBeTruthy();
                    });
                });
            });

            describe('custom labels', function () {
                beforeEach(function () {
                    chart.label(function () {
                        return 'custom label';
                    }).render();
                });

                it('should render a label for each datum', function () {
                    expect(chart.selectAll('text.row').size()).toBe(N);
                });

                it('should use the custom function for each label', function () {
                    chart.selectAll('text.row').each(function () {
                        expect(d3.select(this).text()).toBe('custom label');
                    });
                });

                describe('with labels disabled', function () {
                    beforeEach(function () {
                        chart.renderLabel(false).render();
                    });

                    it('should not display labels', function () {
                        expect(chart.selectAll('text.row').size()).toBe(0);
                    });
                });
            });

            describe('custom titles', function () {
                beforeEach(function () {
                    chart.title(function () {
                        return 'custom title';
                    }).render();
                });

                it('should render a title for each datum', function () {
                    expect(chart.selectAll('g.row title').size()).toBe(N);
                });

                it('should use the custom function for each title', function () {
                    chart.selectAll('g.row title').each(function () {
                        expect(d3.select(this).text()).toBe('custom title');
                    });
                });

                describe('with titles disabled', function () {
                    beforeEach(function () {
                        chart.renderTitle(false).render();
                    });

                    it('should not display labels', function () {
                        expect(chart.selectAll('g.row title').size()).toBe(0);
                    });
                });
            });
        });
    }

    itShouldBehaveLikeARowChartWithGroup(positiveGroupHolder, 5);
    itShouldBehaveLikeARowChartWithGroup(negativeGroupHolder, 5);
    itShouldBehaveLikeARowChartWithGroup(mixedGroupHolder, 5);
    itShouldBehaveLikeARowChartWithGroup(largerGroupHolder, 7);
});

