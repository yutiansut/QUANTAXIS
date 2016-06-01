/* global appendChartID */
describe('dc.seriesChart', function () {

    var chart;
    var colorRows = [
        {colData: 1, rowData: 1, colorData: 1},
        {colData: 1, rowData: 2, colorData: 2},
        {colData: 2, rowData: 1, colorData: 3},
        {colData: 2, rowData: 2, colorData: 4}
    ];
    var colorData;

    beforeEach(function () {
        colorData = crossfilter(colorRows);
        var dimensionColorData = colorData.dimension(function (d) { return [+d.colData, +d.rowData]; });
        var groupColorData = dimensionColorData.group().reduceSum(function (d) { return +d.colorData; });

        var id = 'series-chart';
        appendChartID(id);
        chart = dc.seriesChart('#' + id);

        chart
            .width(210)
            .height(210)
            .x(d3.scale.linear().domain([1,2]))
            .dimension(dimensionColorData)
            .group(groupColorData)
            .ordinalColors(['#000001', '#000002'])
            .seriesAccessor(function (d) { return +d.key[0];})
            .keyAccessor(function (d) { return +d.key[1];})
            .valueAccessor(function (d) { return +d.value ;})
            .childOptions({renderArea: true, dashStyle: [3, 1, 1]})
            .transitionDuration(0);
    });

    describe('#render', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should create the svg', function () {
            expect(chart.svg()).not.toBeNull();
        });

        it('should position generated lineCharts using the data', function () {
            var lines = chart.selectAll('path.line');

            expect(d3.select(lines[0][0]).attr('d')).toMatchPath('M0,128L130,85');
            expect(d3.select(lines[0][1]).attr('d')).toMatchPath('M0,43L130,0');
        });

        it('should color lines using the colors in the data', function () {
            var lines = chart.selectAll('path.line');

            expect(d3.select(lines[0][0]).attr('stroke')).toBe('#000001');
            expect(d3.select(lines[0][1]).attr('stroke')).toBe('#000002');
        });

        describe('with brush off', function () {
            it('should create line chart dots', function () {
                chart.brushOn(false).render();
                var dots = chart.selectAll('circle.dot');
                expect(dots[0].length).toEqual(4);
                chart.brushOn(true);
            });
        });
    });

    describe('series sorting', function () {
        beforeEach(function () {
            chart
                .seriesSort(d3.descending)
                .render();
        });

        it('should order lineCharts in the order specified', function () {
            var lines = chart.selectAll('path.line');

            expect(d3.select(lines[0][1]).attr('d')).toMatchPath('M0,128L130,85');
            expect(d3.select(lines[0][0]).attr('d')).toMatchPath('M0,43L130,0');
        });
    });

    describe('chart options', function () {
        beforeEach(function () {
            chart.render();
        });

        it('should apply options to all lines in the chart', function () {
            var lines = chart.selectAll('path.line');
            var areas = chart.selectAll('path.area');

            expect(d3.select(lines[0][0]).attr('stroke-dasharray')).toEqualIntList('3,1,1');
            expect(d3.select(lines[0][1]).attr('stroke-dasharray')).toEqualIntList('3,1,1');

            expect(d3.select(areas[0][0]).attr('fill')).toBe('#000001');
            expect(d3.select(areas[0][1]).attr('fill')).toBe('#000002');
        });
    });

    describe('#redraw', function () {
        var colorRows2 = [
            {colData: 1, rowData: 1, colorData: 1},
            {colData: 1, rowData: 2, colorData: 2},
            {colData: 2, rowData: 1, colorData: 3},
            {colData: 2, rowData: 2, colorData: 4},
            {colData: 3, rowData: 1, colorData: 5},
            {colData: 3, rowData: 2, colorData: 6}
        ];
        var colorData2;
        beforeEach(function () {
            colorData2 = crossfilter(colorRows2);
            chart.brushOn(false);
            chart.render();

            var dimensionData = colorData2.dimension(function (d) { return [+d.colData, +d.rowData]; });
            var groupData = dimensionData.group().reduceSum(function (d) { return +d.colorData; });

            chart.dimension(dimensionData).group(groupData);

            chart.redraw();
        });

        afterEach(function () {
            chart.brushOn(true);
        });

        it('is redrawn with dots', function () {
            var dots = chart.selectAll('circle.dot');
            expect(dots[0].length).toEqual(6);
        });
    });
});
