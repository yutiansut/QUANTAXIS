/* global appendChartID, loadDateFixture */
describe('dc.bubbleOverlay', function () {
    var chart, data;
    var dimension, group;

    describe('creation', function () {
        beforeEach(function () {
            data = crossfilter(loadDateFixture());
            dimension = data.dimension(function (d) {return d.state;});
            group = dimension.group().reduceSum(function (d) {return d.value;});

            var id = 'bubble-overlay';
            var parent = appendChartID(id);
            var svg = parent.append('svg');

            chart = dc.bubbleOverlay('#' + id)
                .svg(svg)
                .dimension(dimension)
                .group(group)
                .width(300)
                .height(200)
                .transitionDuration(0)
                .title(function (d) {return 'Title: ' + d.key;})
                .r(d3.scale.linear().domain([0, 500]))
                .ordinalColors(['blue'])
                .point('California', 100, 120)
                .point('Colorado', 300, 120)
                .point('Delaware', 500, 220)
                .point('Ontario', 180, 90)
                .point('Mississippi', 120, 220)
                .point('Oklahoma', 200, 350);

            chart.render();
        });

        it('should generate an instance of the dc chart', function () {
            expect(dc.instanceOfChart(chart)).toBeTruthy();
        });

        it('should be registered', function () {
            expect(dc.hasChart(chart)).toBeTruthy();
        });

        it('should generate the correct number of overlay groups', function () {
            expect(chart.selectAll('g.node')[0].length).toEqual(6);
        });

        it('should generate a correct class name for the overlay groups', function () {
            expect(d3.select(chart.selectAll('g.node')[0][0]).attr('class')).toEqual('node california');
            expect(d3.select(chart.selectAll('g.node')[0][3]).attr('class')).toEqual('node ontario');
        });

        it('should generate the correct number of overlay bubbles', function () {
            expect(chart.selectAll('circle.bubble')[0].length).toEqual(6);
        });

        it('should generate a correct translate for overlay groups', function () {
            expect(d3.select(chart.selectAll('g.node')[0][0]).attr('transform')).toMatchTranslate(100, 120);
            expect(d3.select(chart.selectAll('g.node')[0][3]).attr('transform')).toMatchTranslate(180, 90);
        });

        it('should generate correct radii for circles', function () {
            expect(d3.select(chart.selectAll('circle.bubble')[0][0]).attr('r')).toEqual('34.64');
            expect(d3.select(chart.selectAll('circle.bubble')[0][3]).attr('r')).toEqual('22.32');
        });

        it('should generate correct labels', function () {
            expect(d3.select(chart.selectAll('g.node text')[0][0]).text()).toEqual('California');
            expect(d3.select(chart.selectAll('g.node text')[0][3]).text()).toEqual('Ontario');
        });

        it('should generate the label only once', function () {
            chart.redraw();
            expect(chart.selectAll('g.node text')[0].length).toEqual(6);
        });

        it('generate the correct titles', function () {
            expect(d3.select(chart.selectAll('g.node title')[0][0]).text()).toEqual('Title: California');
            expect(d3.select(chart.selectAll('g.node title')[0][3]).text()).toEqual('Title: Ontario');
        });

        it('should only generate titles once', function () {
            chart.redraw();
            expect(chart.selectAll('g.node title')[0].length).toEqual(6);
        });

        it('should fill circles with the specified colors', function () {
            expect(d3.select(chart.selectAll('circle.bubble')[0][0]).attr('fill')).toEqual('blue');
            expect(d3.select(chart.selectAll('circle.bubble')[0][3]).attr('fill')).toEqual('blue');
        });

        it('should highlight the filtered bubbles', function () {
            chart.filter('Colorado');
            chart.filter('California');
            chart.redraw();
            expect(d3.select(chart.selectAll('g.node')[0][0]).attr('class')).toEqual('node california selected');
            expect(d3.select(chart.selectAll('g.node')[0][1]).attr('class')).toEqual('node colorado selected');
            expect(d3.select(chart.selectAll('g.node')[0][3]).attr('class')).toEqual('node ontario deselected');
        });
    });
});

