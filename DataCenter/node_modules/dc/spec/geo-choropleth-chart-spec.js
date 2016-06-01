/* global appendChartID, loadDateFixture, loadGeoFixture, loadGeoFixture2, loadGeoFixture3 */
describe('dc.geoChoropleth', function () {
    var data;
    var stateDimension, stateValueSumGroup, districtDimension, districtValueEnrollGroup;
    var geoJson, geoJson2, geoJson3;

    beforeEach(function () {
        data = crossfilter(loadDateFixture());
        stateDimension = data.dimension(function (d) {return d.state;});
        stateValueSumGroup = stateDimension.group().reduceSum(function (d) {return d.value;});
        districtDimension = data.dimension(function (d) {return d.district;});
        districtValueEnrollGroup = districtDimension.group().reduceSum(function (d) {return d.value;});

        if (!geoJson) {
            geoJson = loadGeoFixture();
        }
        if (!geoJson2) {
            geoJson2 = loadGeoFixture2();
        }
        if (!geoJson3) {
            geoJson3 = loadGeoFixture3();
        }
    });

    function buildChart (id) {
        var div = appendChartID(id);
        div.append('a').attr('class', 'reset').style('display', 'none');
        div.append('span').attr('class', 'filter').style('display', 'none');
        var chart = dc.geoChoroplethChart('#' + id);
        chart.dimension(stateDimension)
            .group(stateValueSumGroup)
            .width(990)
            .height(600)
            .colors(['#ccc', '#E2F2FF', '#C4E4FF', '#9ED2FF', '#81C5FF', '#6BBAFF', '#51AEFF', '#36A2FF', '#1E96FF', '#0089FF'])
            .colorDomain([0, 155])
            .overlayGeoJson(geoJson.features, 'state', function (d) {
                return d.properties.name;
            })
            .overlayGeoJson(geoJson2.features, 'county')
            .transitionDuration(0)
            .title(function (d) {
                return d.key + ' : ' + (d.value ? d.value : 0);
            });
        chart.render();
        return chart;
    }

    function buildChartWithCustomProjection (id) {
        var div = appendChartID(id);
        div.append('a').attr('class', 'reset').style('display', 'none');
        div.append('span').attr('class', 'filter').style('display', 'none');
        var chart = dc.geoChoroplethChart('#' + id);
        chart.dimension(districtDimension)
            .group(districtValueEnrollGroup)
            .projection(d3.geo.mercator()
                        .scale(26778)
                        .translate([8227, 3207]))
            .width(990)
            .height(600)
            .colors(['#ccc', '#E2F2FF', '#C4E4FF', '#9ED2FF', '#81C5FF', '#6BBAFF', '#51AEFF', '#36A2FF', '#1E96FF', '#0089FF'])
            .colorDomain([0, 155])
            .overlayGeoJson(geoJson3.features, 'district', function (d) {
                return d.properties.NAME;
            })
            .transitionDuration(0)
            .title(function (d) {
                return d.key + ' : ' + (d.value ? d.value : 0);
            });
        chart.render();
        return chart;
    }

    describe('creation', function () {
        var chart;
        beforeEach(function () {
            chart = buildChart('choropleth-chart');
        });

        it('should return not null', function () {
            expect(chart).not.toBeNull();
        });
        it('should have a d3.geo.path', function () {
            expect(chart.geoPath()).not.toBeNull();
        });
        it('svg is created', function () {
            expect(chart.selectAll('svg').length).not.toEqual(0);
        });
        it('geo layer0 g is created', function () {
            expect(chart.selectAll('g.layer0').length).not.toEqual(0);
        });
        it('correct number of states should be generated', function () {
            expect(chart.selectAll('g.layer0 g.state')[0].length).toEqual(52);
        });
        it('correct css class should be set [Alaska]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][1].getAttribute('class')).toEqual('state alaska');
        });
        it('correct title should be set [Alaska]', function () {
            expect(chart.selectAll('g.layer0 g.state title')[0][1].textContent).toEqual('Alaska : 0');
        });
        it('correct color filling should be set [Alaska]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][1].getAttribute('fill')).toEqual('#ccc');
        });
        it('correct state boundary should be rendered [Alaska]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][1].getAttribute('d').length).not.toEqual(0);
        });
        it('correct css class should be set [California]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][4].getAttribute('class')).toEqual('state california');
        });
        it('correct css class should be set [District of Columbia]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][8].getAttribute('class')).toEqual('state district_of_columbia');
        });
        it('correct title should be set [California]', function () {
            expect(chart.selectAll('g.layer0 g.state title')[0][4].textContent).toEqual('California : 154');
        });
        it('correct color should be set [California]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][4].getAttribute('fill')).toMatch(/#0089FF/i);
        });
        it('correct state boundary should be rendered [California]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][4].getAttribute('d').length).not.toEqual(0);
        });
        it('correct css class should be set [Colorado]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][5].getAttribute('class')).toEqual('state colorado');
        });
        it('correct title should be set [Colorado]', function () {
            expect(chart.selectAll('g.layer0 g.state title')[0][5].textContent).toEqual('Colorado : 22');
        });
        it('correct color should be set [Colorado]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][5].getAttribute('fill')).toMatch(/#E2F2FF/i);
        });
        it('correct state boundary should be rendered [Colorado]', function () {
            expect(chart.selectAll('g.layer0 g.state path')[0][5].getAttribute('d').length).not.toEqual(0);
        });
        it('geo layer1 g is created', function () {
            expect(chart.selectAll('g.layer1').length).not.toEqual(0);
        });
        it('correct number of counties should be generated', function () {
            expect(chart.selectAll('g.layer1 g.county')[0].length).toEqual(5);
        });
        it('correct css class should be set [county]', function () {
            expect(chart.selectAll('g.layer1 g.county')[0][1].getAttribute('class')).toEqual('county');
        });
        it('correct title should be set [county]', function () {
            expect(chart.selectAll('g.layer1 g.county title')[0][1].textContent).toEqual('');
        });
        it('correct color filling should be set [county]', function () {
            expect(chart.selectAll('g.layer1 g.county path')[0][1].getAttribute('fill')).toEqual('white');
        });
        it('correct state boundary should be rendered [county]', function () {
            expect(chart.selectAll('g.layer1 g.county path')[0][1].getAttribute('d').length).not.toEqual(0);
        });

        afterEach(function () {
            stateDimension.filterAll();
            districtDimension.filterAll();
        });
    });

    describe('filter and highlight', function () {
        var chart;
        beforeEach(function () {
            chart = buildChart('choropleth-chart-with-filter');
            chart.filter('Colorado');
            chart.filter('California');
            chart.redraw();
        });

        it('correct color should be set [California]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][0].getAttribute('class')).toEqual('state alabama deselected');
            expect(chart.selectAll('g.layer0 g.state')[0][1].getAttribute('class')).toEqual('state alaska deselected');
        });
        it('correct color should be set [California, Colorado]', function () {
            expect(chart.selectAll('g.layer0 g.state')[0][4].getAttribute('class')).toEqual('state california selected');
            expect(chart.selectAll('g.layer0 g.state')[0][5].getAttribute('class')).toEqual('state colorado selected');
        });

        afterEach(function () {
            stateDimension.filterAll();
            districtDimension.filterAll();
        });
    });

    describe('custom projection', function () {
        var chart;
        beforeEach(function () {
            chart = buildChartWithCustomProjection('choropleth-chart-with-projection');
        });

        it('should return not null', function () {
            expect(chart).not.toBeNull();
        });
        it('svg is created', function () {
            expect(chart.selectAll('svg').length).not.toEqual(0);
        });

        afterEach(function () {
            stateDimension.filterAll();
            districtDimension.filterAll();
        });
    });

    describe('replace and remove layer', function () {
        var chart;
        beforeEach(function () {
            chart = buildChart('choropleth-chart-replace-layer');
            chart.overlayGeoJson(geoJson3.features, 'state', function (d) {
                return d.properties.name;
            });
        });
        it('geo json layer with the same name should be replaced', function () {
            expect(chart.geoJsons().filter(function (e) {
                return e.name === 'state';
            })[0].data).toBe(geoJson3.features);
        });
        it('geo json layer can be removed by name', function () {
            chart.removeGeoJson('state');
            expect(chart.geoJsons().filter(function (e) {
                return e.name === 'state';
            }).length).toEqual(0);
        });
        afterEach(function () {
            stateDimension.filterAll();
            districtDimension.filterAll();
        });
    });
});
