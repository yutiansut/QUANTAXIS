/* global appendChartID, flushAllD3Transitions, loadDateFixture */
describe('dc.baseMixin', function () {
    var id, chart, dimension, group, addFilterHandler, removeFilterHandler, hasFilterHandler, resetFilterHandler;

    beforeEach(function () {
        var data = crossfilter(loadDateFixture());
        dimension = data.dimension(function (d) {
            return d3.time.day.utc(d.dd);
        });
        group = dimension.group().reduceSum(function (d) {
            return d.value;
        });

        chart = dc.baseMixin({})
            .options({
                dimension: dimension,
                group: group,
                transitionDuration: 100
            });
        id = 'base-chart';
        appendChartID(id);
        chart.anchor('#' + id)
            .resetSvg(); // so that renderlets can fire
        addFilterHandler = chart.addFilterHandler();
        hasFilterHandler = chart.hasFilterHandler();
        removeFilterHandler = chart.removeFilterHandler();
        resetFilterHandler = chart.resetFilterHandler();
    });

    describe('renderlets', function () {
        var firstRenderlet, secondRenderlet, thirdRenderlet,
            pretransition;
        beforeEach(function () {
            var expectedCallbackSignature = function (callbackChart) {
                expect(callbackChart).toBe(chart);
            };
            firstRenderlet = jasmine.createSpy().and.callFake(expectedCallbackSignature);
            secondRenderlet = jasmine.createSpy().and.callFake(expectedCallbackSignature);
            thirdRenderlet = jasmine.createSpy().and.callFake(expectedCallbackSignature);
            pretransition = jasmine.createSpy().and.callFake(expectedCallbackSignature);
            chart.renderlet(firstRenderlet); // still testing renderlet event-namespace generation here
            chart.renderlet(secondRenderlet);
            chart.on('renderlet.third', thirdRenderlet);
            chart.on('pretransition.pret', pretransition);
        });

        it('should not execute a renderlet until after the render transitions', function () {
            chart.render();
            expect(firstRenderlet).not.toHaveBeenCalled();
            flushAllD3Transitions();
            expect(firstRenderlet).toHaveBeenCalled();
        });

        it('should not execute a renderlet until after the redraw transitions', function () {
            chart.redraw();
            expect(firstRenderlet).not.toHaveBeenCalled();
            flushAllD3Transitions();
            expect(firstRenderlet).toHaveBeenCalled();
        });

        it('should execute pretransition event before the render transitions', function () {
            chart.render();
            expect(pretransition).toHaveBeenCalled();
            flushAllD3Transitions();
        });

        it('should execute pretransition event before the redraw transitions', function () {
            chart.redraw();
            expect(pretransition).toHaveBeenCalled();
            flushAllD3Transitions();
        });

        it('should execute each renderlet after a render', function () {
            chart.render();
            flushAllD3Transitions();
            expect(firstRenderlet).toHaveBeenCalled();
            expect(secondRenderlet).toHaveBeenCalled();
        });

        it('should execute each renderlet after a redraw', function () {
            chart.redraw();
            flushAllD3Transitions();
            expect(firstRenderlet).toHaveBeenCalled();
            expect(secondRenderlet).toHaveBeenCalled();
        });

        it('should execute a named renderlet after a render', function () {
            chart.render();
            flushAllD3Transitions();
            expect(thirdRenderlet).toHaveBeenCalled();
        });

        it('should execute a named renderlet after a redraw', function () {
            chart.redraw();
            flushAllD3Transitions();
            expect(thirdRenderlet).toHaveBeenCalled();
        });

        it('should remove a named renderlet expect no call after a redraw', function () {
            chart.on('renderlet.third');
            chart.redraw();
            flushAllD3Transitions();
            expect(secondRenderlet).toHaveBeenCalled();
            expect(thirdRenderlet).not.toHaveBeenCalled();
        });

        it('should remove a named renderlet and expect no call after a redraw', function () {
            chart.on('renderlet.third');
            chart.render();
            flushAllD3Transitions();
            expect(secondRenderlet).toHaveBeenCalled();
            expect(thirdRenderlet).not.toHaveBeenCalled();
        });
    });

    describe('event listeners', function () {
        describe('on render', function () {
            var preRenderSpy, postRenderSpy;
            beforeEach(function () {
                var expectedCallbackSignature = function (callbackChart) {
                    expect(callbackChart).toBe(chart);
                };

                preRenderSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);
                postRenderSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);

                chart.on('preRender', preRenderSpy);
                chart.on('postRender', postRenderSpy);
            });

            it('should execute the preRender callback', function () {
                chart.render();
                flushAllD3Transitions();
                expect(preRenderSpy).toHaveBeenCalled();
            });

            it('should execute the postRender callback', function () {
                chart.render();
                flushAllD3Transitions();
                expect(postRenderSpy).toHaveBeenCalled();
            });
        });

        describe('on filter double', function () {
            var filterSpy, filterSpy2, filter;
            beforeEach(function () {
                filter = '1';

                var expectedCallbackSignature = function (callbackChart, callbackFilter) {
                    expect(callbackChart).toBe(chart);
                    expect(callbackFilter).toEqual(filter);
                };

                filterSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);
                filterSpy2 = jasmine.createSpy().and.callFake(expectedCallbackSignature);
                chart.on('filtered.one', filterSpy);
                chart.on('filtered.two', filterSpy2);
            });

            it('should execute first callback after setting through #filter', function () {
                chart.filter(filter);
                expect(filterSpy).toHaveBeenCalled();
            });

            it('should execute second callback after setting through #filter', function () {
                chart.filter(filter);
                expect(filterSpy2).toHaveBeenCalled();
            });

            it('should not execute callback after reading from #filter', function () {
                chart.filter();
                expect(filterSpy).not.toHaveBeenCalled();
            });
        });

        describe('on filter', function () {
            var filterSpy, filter;
            beforeEach(function () {
                filter = '1';

                var expectedCallbackSignature = function (callbackChart, callbackFilter) {
                    expect(callbackChart).toBe(chart);
                    expect(callbackFilter).toEqual(filter);
                };

                filterSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);
                chart.on('filtered', filterSpy);
            });

            it('should execute callback after setting through #filter', function () {
                chart.filter(filter);
                expect(filterSpy).toHaveBeenCalled();
            });

            it('should not execute callback after reading from #filter', function () {
                chart.filter();
                expect(filterSpy).not.toHaveBeenCalled();
            });
        });

        describe('on redraw', function () {
            var preRedrawSpy, postRedrawSpy;
            beforeEach(function () {
                var expectedCallbackSignature = function (callbackChart) {
                    expect(callbackChart).toBe(chart);
                };

                preRedrawSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);
                postRedrawSpy = jasmine.createSpy().and.callFake(expectedCallbackSignature);

                chart.on('preRedraw', preRedrawSpy);
                chart.on('postRedraw', postRedrawSpy);
            });

            it('should execute the preRedraw callback before transitions', function () {
                chart.redraw();
                expect(preRedrawSpy).toHaveBeenCalled();
                flushAllD3Transitions();
            });

            it('should execute the postRedraw callback after transitions', function () {
                chart.redraw();
                expect(postRedrawSpy).not.toHaveBeenCalled();
                flushAllD3Transitions();
                expect(postRedrawSpy).toHaveBeenCalled();
            });
        });
    });

    describe('validations', function () {

        it('should require dimension', function () {
            try {
                dc.baseMixin({}).group(group).render();
                throw new Error('That should\'ve thrown');
            } catch (e) {
                expect(e instanceof dc.errors.InvalidStateException).toBeTruthy();
            }
        });

        it('should require group', function () {
            try {
                dc.baseMixin({}).dimension(dimension).render();
                throw new Error('That should\'ve thrown');
            } catch (e) {
                expect(e instanceof dc.errors.InvalidStateException).toBeTruthy();
            }
        });
    });

    describe('anchoring chart to dom', function () {
        var id;

        beforeEach(function () {
            id = 'chart-id';
        });

        describe('using a d3-created dom element', function () {
            var anchorDiv;

            beforeEach(function () {
                anchorDiv = d3.select('body').append('div').attr('id', id).node();
                chart.anchor(anchorDiv);
            });

            it('should register the chart', function () {
                expect(dc.hasChart(chart)).toBeTruthy();
            });

            it('should return the node, when anchor is called', function () {
                expect(chart.anchor()).toEqual(anchorDiv);
            });

            it('should return the id, when anchorName is called', function () {
                expect(chart.anchorName()).toEqual(id);
            });

            describe('without an id', function () {
                beforeEach(function () {
                    d3.select('#' + id).remove();
                    anchorDiv = d3.select('body').append('div').attr('class', 'no-id').node();
                    chart.anchor(anchorDiv);
                });

                it('should return the node, when anchor is called', function () {
                    expect(chart.anchor()).toEqual(anchorDiv);
                });

                it('should return a valid, selectable id', function () {
                    // see http://stackoverflow.com/questions/70579/what-are-valid-values-for-the-id-attribute-in-html
                    expect(chart.anchorName()).toMatch(/^[a-zA-Z][a-zA-Z0-9_:.-]*$/);
                });

            });
        });

        describe('using a d3 selection', function () {
            var anchorDiv;

            beforeEach(function () {
                anchorDiv = d3.select('body').append('div').attr('id', id);
                chart.anchor(anchorDiv);
            });

            it('should register the chart', function () {
                expect(dc.hasChart(chart)).toBeTruthy();
            });

            it('should return the node, when anchor is called', function () {
                expect(chart.anchor()).toEqual(anchorDiv.node());
            });

            it('should return the id, when anchorName is called', function () {
                expect(chart.anchorName()).toEqual(id);
            });

            describe('without an id', function () {
                beforeEach(function () {
                    d3.select('#' + id).remove();
                    anchorDiv = d3.select('body').append('div').attr('class', 'no-id').node();
                    chart.anchor(anchorDiv);
                });

                it('should return the node, when anchor is called', function () {
                    expect(chart.anchor()).toEqual(anchorDiv);
                });

                it('should return a valid, selectable id', function () {
                    // see http://stackoverflow.com/questions/70579/what-are-valid-values-for-the-id-attribute-in-html
                    expect(chart.anchorName()).toMatch(/^[a-zA-Z][a-zA-Z0-9_:.-]*$/);
                });

            });
        });

        describe('using an id selector', function () {
            beforeEach(function () {
                d3.select('body').append('div').attr('id', id);
                chart.anchor('#' + id);
            });

            it('should add the dc chart class to its parent div', function () {
                expect(chart.root().classed('dc-chart')).toBeTruthy();
            });

            it('should return the id selector when anchor is called', function () {
                expect(chart.anchor()).toEqual('#' + id);
            });

            it('should return the id when anchorName is called', function () {
                expect(chart.anchorName()).toEqual(id);
            });
        });
    });

    describe('calculation of dimensions', function () {
        var dimdiv, bodyWidth;
        beforeEach(function () {
            dimdiv = appendChartID('dimensionTest');
            chart.anchor('#dimensionTest');
            bodyWidth = d3.select('body')[0][0].getBoundingClientRect().width;
        });

        describe('when set to a falsy on a sized div', function () {
            var h0, w0;
            beforeEach(function () {
                dimdiv.style({
                    height: '220px',
                    width: '230px'
                });
                chart.width(null).height(null).render();
                w0 = chart.width();
                h0 = chart.height();
            });

            it('should set the height to the div size', function () {
                expect(chart.height()).toBeCloseTo(220,1);
            });

            it('should set the width to the div size', function () {
                expect(chart.width()).toBeCloseTo(230,1);
            });

            describe('and redrawn', function () {
                beforeEach(function () {
                    chart.redraw();
                });

                it('should keep the size the same', function () {
                    expect(chart.height()).toEqual(h0,1);
                    expect(chart.width()).toEqual(w0);
                });
            });

            describe('and minimums set', function () {
                beforeEach(function () {
                    chart.minHeight(234).minWidth(976)
                        .render();
                });

                it('should set the height to the minimum', function () {
                    expect(chart.height()).toBeCloseTo(234,1);
                });

                it('should set the width to the minimum', function () {
                    expect(chart.width()).toBeCloseTo(976,1);
                });
            });
        });

        describe('when set to a falsy on an unsized div with junk in it', function () {
            var h0, w0;
            beforeEach(function () {
                dimdiv.append('h1').text('helL0');
                chart.width(null).height(null)
                    .render()
                    .resetSvg(); // because all real charts generate svg
                w0 = chart.width();
                h0 = chart.height();
            });

            it('should set the height to at least the default minimum', function () {
                expect(chart.height()).not.toBeLessThan(200);
            });

            it('should set the width to at least the default minimum', function () {
                expect(chart.width()).not.toBeLessThan(200);
            });

            describe('and redrawn', function () {
                beforeEach(function () {
                    chart.redraw();
                });

                it('should keep the size the same', function () {
                    expect(chart.height()).toEqual(h0);
                    expect(chart.width()).toEqual(w0);
                });
            });
        });

        describe('when set with a number', function () {
            beforeEach(function () {
                chart.width(300).height(301).render();
            });

            it('should set the height', function () {
                expect(chart.height()).toEqual(301);
            });

            it('should set the width', function () {
                expect(chart.width()).toEqual(300);
            });
        });

        describe('when set to a callback function', function () {
            var setterSpy;
            beforeEach(function () {
                setterSpy = jasmine.createSpy().and.returnValue(800);
                chart.width(setterSpy).render();
            });

            it('should not execute callback before width() is called', function () {
                expect(setterSpy).not.toHaveBeenCalled();
            });

            it('should ask the callback for the width', function () {
                expect(chart.width()).toEqual(800);
                expect(setterSpy).toHaveBeenCalled();
            });
        });
    });

    describe('filter handling', function () {
        var filter, notFilter;
        beforeEach(function () {
            // 1 && 0 should handle most cases.  Could be true/false booleans...
            filter = 1;
            notFilter = 0;
            chart.addFilterHandler(addFilterHandler);
            chart.hasFilterHandler(hasFilterHandler);
            chart.removeFilterHandler(removeFilterHandler);
            chart.resetFilterHandler(resetFilterHandler);
            chart.filterAll();
        });
        it('with the default hasFilterHandler', function () {
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
        });
        it('with a truthy hasFilterHandler', function () {
            chart.filter(filter);
            chart.hasFilterHandler(function () { return true; });
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
        });
        it('with a falsy hasFilterHandler', function () {
            chart.filter(filter);
            chart.hasFilterHandler(function () { return false; });
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
        });
        it('with the default addFilterHandler', function () {
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.filters().length).toEqual(1);
        });
        it('with a noop addFilterHandler', function () {
            chart.addFilterHandler(function (filters, filter) {
                return filters;
            });
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
            expect(chart.filters().length).toEqual(0);
        });
        it('with a static addFilterHandler', function () {
            chart.addFilterHandler(function (filters, filter) {
                filters.push(notFilter);
                return filters;
            });
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(1);
        });
        it('with the default removeFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            expect(chart.filters().length).toEqual(2);
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(1);
            chart.filter(notFilter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
            expect(chart.filters().length).toEqual(0);
        });
        it('with a noop removeFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            chart.removeFilterHandler(function (filters, filter) {
                return filters;
            });
            expect(chart.filters().length).toEqual(2);
            chart.filter(filter);
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(2);
            chart.filter(notFilter);
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(2);
        });
        it('with a shift removeFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            chart.removeFilterHandler(function (filters, filter) {
                if (filters.length > 0) {
                    filters.shift();
                }
                return filters;
            });
            expect(chart.filters().length).toEqual(2);
            chart.filter(notFilter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(1);
            chart.filter(notFilter);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
            expect(chart.filters().length).toEqual(0);
        });
        it('with the default resetFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            chart.filter(null);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
            expect(chart.filters().length).toEqual(0);
        });
        it('with a noop resetFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            chart.resetFilterHandler(function (filters) {
                return filters;
            });
            chart.filter(null);
            expect(chart.hasFilter(filter)).toBeTruthy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(2);
        });
        it('with a shift resetFilterHandler', function () {
            chart.filter(filter);
            chart.filter(notFilter);
            chart.resetFilterHandler(function (filters) {
                filters.shift();
                return filters;
            });
            chart.filter(null);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeTruthy();
            expect(chart.filters().length).toEqual(1);
            chart.filter(null);
            expect(chart.hasFilter(filter)).toBeFalsy();
            expect(chart.hasFilter(notFilter)).toBeFalsy();
            expect(chart.filters().length).toEqual(0);
        });
    });
});
