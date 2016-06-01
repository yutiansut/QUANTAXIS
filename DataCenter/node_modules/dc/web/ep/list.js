
function list (selector,path,data) {
  var ndx = crossfilter(data),
  all = ndx.groupAll();

  var pie_group = dc.pieChart(selector +  " .group").innerRadius(20).radius(70);
  var group = ndx.dimension(function(d) {
    if (typeof d.party == "undefined") return "";
    return d.party;
  });
  var groupGroup   = group.group().reduceSum(function(d) {   return 1; });

  var pie_gender = dc.pieChart(selector +  " .gender").radius(70);
  var gender = ndx.dimension(function(d) {
    if (typeof d.gender_id == "undefined") return "";
    return d.gender;
  });

  var groupGender   = gender.group().reduceSum(function(d) {   return 1; });

  var bar_country = dc.barChart(selector + " .country");
  var country = ndx.dimension(function(d) {
    if (typeof d.country == "undefined") return "";
    return d.country;
  });
  var countryGroup   = country.group().reduceSum(function(d) { return 1; });
 
 pie_gender
  .width(200)
  .height(200)
  .dimension(gender)
  .group(groupGender);

 pie_group
  .width(200)
  .height(200)
  .dimension(group)
  .colors(d3.scale.category10())
  .group(groupGroup)
  .on('renderlet', function (chart) {
  });

 bar_country
  .width(444)
  .height(200)
  .outerPadding(0)
  .gap(1)
  .margins({top: 0, right: 0, bottom: 95, left: 30})
  .x(d3.scale.ordinal())
  .xUnits(dc.units.ordinal)
  .brushOn(false)
  .elasticY(true)
  .yAxisLabel("#MEPs")
  .dimension(country)
  .group(countryGroup);

 bar_country.on("postRender", function(c) {rotateBarChartLabels();} );


function rotateBarChartLabels() {
  d3.selectAll(selector+ ' .country .axis.x text')
    .style("text-anchor", "end" )
    .attr("transform", function(d) { return "rotate(-90, -4, 9) "; });
}


  dc.dataCount(".dc-data-count")
    .dimension(ndx)
    .group(all);

  dc.dataTable(".dc-data-table")
        .dimension(country)
        .group(function (d) {
            return d.country;
        })
        .size(1000)
        .columns([
            function (d) {
                return d.gender || "";
            },
            function (d) {
                return d.first_name || "";
            },
            function (d) {
                return d.last_name || "";
            },
            function (d) {
                return d.country || "";
            },
            function (d) {
                return d.party || "";
            }
        ])
        .sortBy(function (d) {
            return d.last_name;
        })
        .order(d3.ascending)
        .on('renderlet', function (table) {
        });



  dc.renderAll();

}

