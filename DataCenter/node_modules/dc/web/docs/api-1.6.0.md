#### Version 1.6.0

The entire dc.js library is scoped under **dc** name space. It does not introduce anything else into the global
name space.

* [Base Chart [abstract]](#base-chart)
* [Color Chart [abstract]](#color-chart)
* [Stackable Chart [abstract]](#stackable-chart)
* [Coordinate Grid Chart [abstract] < Color Chart < Base Chart](#coordinate-grid-chart)
* [Pie Chart [concrete] < Color Chart < Base Chart](#pie-chart)
* [Row Chart [concrete] < Color Chart < Base chart](#row-chart)
* [Bar Chart [concrete] < Stackable Chart < CoordinateGrid Chart](#bar-chart)
* [Line Chart [concrete] < Stackable Chart < CoordinateGrid Chart](#line-chart)
* [Composite Chart [concrete] < CoordinateGrid Chart](#composite-chart)
* [Abstract Bubble Chart [abstract] < Color Chart](#abstract-bubble-chart)
* [Bubble Chart [concrete] < Abstract Bubble Chart < CoordinateGrid Chart](#bubble-chart)
* [Bubble Overlay Chart [concrete] < Abstract Bubble Chart < Base Chart](#bubble-overlay-chart)
* [Geo Choropleth Chart [concrete] < Color Chart < Base Chart](#geo-choropleth-chart)
* [Data Count Widget [concrete] < Base Chart](#data-count)
* [Data Table Widget [concrete] < Base Chart](#data-table)
* [Number Display [Concrete] < Base Chart](#number-display)
* [Legend [concrete]](#legend)
* [Listeners](#listeners)
* [Utilities](#util)

#### Function Chain
Majority of dc functions are designed to allow function chaining, meaning it will return the current chart instance
whenever it is appropriate. Therefore configuration of a chart can be written in the following style.
```js
chart.width(300)
.height(300)
.filter("sunday")
```
The API references will highlight the fact if a particular function is not chainable.

## <a name="util" href="#util">#</a> Utilities

#### dc.filterAll([chartGroup])
Clear all filters on every chart within the given chart group. If the chart group is not given then only charts that
belong to the default chart group will be reset.

#### dc.renderAll([chartGroup])
Re-render all charts belong to the given chart group. If the chart group is not given then only charts that belong to
the default chart group will be re-rendered.

#### dc.redrawAll([chartGroup])
Redraw all charts belong to the given chart group. If the chart group is not given then only charts that belong to the
default chart group will be re-drawn. Redraw is different from re-render since when redrawing dc charts try to update
the graphic incrementally instead of starting from scratch.

#### dc.units.integers
This function can be used to in [Coordinate Grid Chart](#coordinate-grid-chart) to define units on x axis.
dc.units.integers is the default x unit scale used by [Coordinate Grid Chart](#coordinate-grid-chart) and should be
used when x range is a sequential of integers.

#### dc.units.ordinal
This function can be used to in [Coordinate Grid Chart](#coordinate-grid-chart) to define ordinal units on x axis.
Usually this function is used in combination with d3.scale.ordinal() on x axis.

#### dc.units.fp.precision(precision)
This function generates xunit function in floating-point numbers with the given precision. For example if the function
is invoked with 0.001 precision then the function created will devide a range [0.5, 1.0] with 500 units.

#### dc.events.trigger(function[, delay])
This function is design to trigger throttled event function optionally with certain amount of delay(in milli-seconds).
Events that are triggered repetitively due to user interaction such as the dragging of the brush might over flood
library and cause too much rendering being scheduled. In this case, using this function to wrap your event function
allows the library to smooth out the rendering by throttling event flood and only respond to the most recent event.

```js
chart.renderlet(function(chart){
    // smooth the rendering through event throttling
    dc.events.trigger(function(){
        // focus some other chart to the range selected by user on this chart
        someOtherChart.focus(chart.filter());
    });
})
```

## <a name="base-chart" href="#base-chart">#</a> Base Chart [Abstract]
Base chart is an abstract functional object representing a basic dc chart object for all chart and widget implementation.
Every function on base chart are also inherited available on all concrete chart implementation in dc library.

#### .width([value])
Set or get width attribute of a chart. If the value is given, then it will be used as the new width.

If no value specified then value of the current width attribute will be returned.

#### .height([value])
Set or get height attribute of a chart. If the value is given, then it will be used as the new height.

If no value specified then value of the current height attribute will be returned.

#### .dimension([value]) - **mandatory**
Set or get dimension attribute of a chart. In dc a dimension can be any valid
[crossfilter dimension](https://github.com/square/crossfilter/wiki/API-Reference#wiki-dimension). If the value is given,
then it will be used as the new dimension.

If no value specified then the current dimension will be returned.

#### .group([value], [name]) - **mandatory**
Set or get group attribute of a chart. In dc a group is a
[crossfilter group](https://github.com/square/crossfilter/wiki/API-Reference#wiki-group). Usually the group should be
created from the particular dimension associated with the same chart. If the value is given, then it will be used as
the new group.

If no value specified then the current group will be returned.
If name is specified then it will be used to generate legend label.

#### .filterAll()
Clear all filters associated with this chart.

#### .select(selector)
Execute in scope d3 single selection using the given selector and return d3 selection result. Roughly the same as:
```js
d3.select("#chart-id").select(selector);
```
This function is **not chainable** since it does not return a chart instance; however the d3 selection result is chainable
from d3's perspective.

#### .selectAll(selector)
Execute in scope d3 selectAll using the given selector and return d3 selection result. Roughly the same as:
```js
d3.select("#chart-id").selectAll(selector);
```
This function is **not chainable** since it does not return a chart instance; however the d3 selection result is
chainable from d3's perspective.

#### .anchor([anchorChart/anchorSelector], [chartGroup])
Set the svg root to either be an existing chart's root or the first element returned from a d3 css string selector. Optionally registers the chart within the chartGroup. This class is called internally on chart initialization, but be called again to relocate the chart. However, it will orphan any previously created SVG elements.

#### .anchorName()
Return the dom ID for chart's anchored location

#### .root([rootElement])
Returns the root element where a chart resides. Usually it will be the parent div element where svg was created. You
can also pass in a new root element however this is usually handled as part of the dc internal. Resetting root element
on a chart outside of dc internal might have unexpected consequences.

#### .svg([svgElement])
Returns the top svg element for this specific chart. You can also pass in a new svg element however this is usually
handled as part of the dc internal. Resetting svg element on a chart outside of dc internal might have unexpected
consequences.

#### .resetSvg()
Remove the chart's SVG elements from the dom and recreate the container SVG element.

#### .filterPrinter([filterPrinterFunction])
Set or get filter printer function. Filter printer function is used to generate human friendly text for filter value(s)
associated with the chart instance. By default dc charts shipped with a default filter printer implementation dc.printers.filter
that provides simple printing support for both single value and ranged filters.

#### .turnOnControls() & .turnOffControls()
Turn on/off optional control elements within the root element. dc.js currently support the following html control elements.

* root.selectAll(".reset") elements are turned on if the chart has an active filter. This type of control elements are usually used to store reset link to allow user to reset filter on a certain chart. This element will be turned off automatically if the filter is cleared.
* root.selectAll(".filter") elements are turned on if the chart has an active filter. The text content of this element is then replaced with the current filter value using the filter printer function. This type of element will be turned off automatically if the filter is cleared.

#### .transitionDuration([duration])
Set or get animation transition duration(in milliseconds) for specific chart instance. Default duration is 750ms.

#### .render()
Invoke this method will force the chart to re-render everything from scratch. Generally it should be only used to
render the chart for the first time on the page or if you want to make sure everything is redrawn from scratch instead
of relying on the default incremental redrawing behaviour.

#### .redraw()
Calling redraw will cause the chart to re-render delta in data change incrementally. If there is no change in the
underlying data dimension then calling this method will have no effect on the chart. Most of the chart interaction in
dc library will automatically trigger this method through its internal event engine, therefore you only need to manually
invoke this function if data is manipulated outside of dc's control; for example if data is loaded on a periodic basis
in the background using crossfilter.add().

#### .hasFilter([filter])
Check whether is any active filter or a specific filter is associated with particular chart instance.
This function is **not chainable**.

#### .filter([filterValue])
Filter the chart by the given value or return the current filter if the input parameter is missing.
```js
// filter by a single string
chart.filter("Sunday");
// filter by a single age
chart.filter(18);
```

#### .filters()
Return all current filters. This method does not perform defensive cloning of the internal filter array before returning
therefore any modification of returned array will affact chart's internal filter storage.

#### .filterHandler([function])
Set or get filter handler. Filter handler is a function that performs the filter action on a specific dimension. Using
custom filter handler give you the flexibility to perform additional logic before or after filtering.

```js
// default filter handler
function(dimension, filter){
    dimension.filter(filter); // perform filtering
    return filter; // return the actual filter value
}

// custom filter handler
chart.filterHandler(function(dimension, filter){
    var newFilter = filter + 10;
    dimension.filter(newFilter);
    return newFilter; // set the actual filter value to the new value
});
```

#### .keyAccessor([keyAccessorFunction])
Set or get the key accessor function. Key accessor function is used to retrieve key value in crossfilter group. Key
values are used differently in different charts, for example keys correspond to slices in pie chart and x axis position
in grid coordinate chart.
```js
// default key accessor
chart.keyAccessor(function(d) { return d.key; });
// custom key accessor for a multi-value crossfilter reduction
chart.keyAccessor(function(p) { return p.value.absGain; });
```

#### .valueAccessor([valueAccessorFunction])
Set or get the value accessor function. Value accessor function is used to retrieve value in crossfilter group. Group
values are used differently in different charts, for example group values correspond to slices size in pie chart and y
axis position in grid coordinate chart.
```js
// default value accessor
chart.valueAccessor(function(d) { return d.value; });
// custom value accessor for a multi-value crossfilter reduction
chart.valueAccessor(function(p) { return p.value.percentageGain; });
```

#### .label([labelFunction])
Set or get the label function. Chart class will use this function to render label for each child element in the chart,
i.e. a slice in a pie chart or a bubble in a bubble chart. Not every chart supports label function for example bar chart
and line chart do not use this function at all.
```js
// default label function just return the key
chart.label(function(d) { return d.key; });
// label function has access to the standard d3 data binding and can get quite complicated
chart.label(function(d) { return d.data.key + "(" + Math.floor(d.data.value / all.value() * 100) + "%)"; });
```

#### .renderLabel(boolean)
Turn on/off label rendering

#### .title([titleFunction])
Set or get the title function. Chart class will use this function to render svg title(usually interrupted by browser
as tooltips) for each child element in the chart, i.e. a slice in a pie chart or a bubble in a bubble chart. Almost
every chart supports title function however in grid coordinate chart you need to turn off brush in order to use title
otherwise the brush layer will block tooltip trigger.
```js
// default title function just return the key
chart.title(function(d) { return d.key + ": " + d.value; });
// title function has access to the standard d3 data binding and can get quite complicated
chart.title(function(p) {
    return p.key.getFullYear()
        + "\n"
        + "Index Gain: " + numberFormat(p.value.absGain) + "\n"
        + "Index Gain in Percentage: " + numberFormat(p.value.percentageGain) + "%\n"
        + "Fluctuation / Index Ratio: " + numberFormat(p.value.fluctuationPercentage) + "%";
});
```

#### .renderTitle(boolean)
Turn on/off title rendering

#### .renderlet(renderletFunction)
Renderlet is similar to an event listener on rendering event. Multiple renderlets can be added to an individual chart.
Every time when chart is rerendered or redrawn renderlet then will be invoked right after the chart finishes its own
drawing routine hence given you a way to override or modify certain behaviour. Renderlet function accepts the chart
instance as the only input parameter and you can either rely on dc API or use raw d3 to achieve pretty much any effect.
```js
// renderlet function
chart.renderlet(function(chart){
    // mix of dc API and d3 manipulation
    chart.select("g.y").style("display", "none");
    // its a closure so you can also access other chart variable available in the closure scope
    moveChart.filter(chart.filter());
});
```

#### .expireCache()
Expire internal chart cache. dc.js chart cache some data internally on a per chart basis so it can speed up rendering
and avoid unnecessary calculation however under certain circumstances it might be useful to clear the cache e.g. after
you invoke crossfilter.add function or if you reset group or dimension post render it is always a good idea to clear
the cache to make sure charts are rendered properly.

#### .legend([dc.legend])
Attach dc.legend widget to this chart. Legend widget will automatically draw legend labels based on the color setting
and names associated with each group.

```js
chart.legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
```

## <a name="listeners" href="#listeners">#</a> Listeners
All dc chart instance supports the following listeners.

#### .on("preRender", function(chart){...})
This listener function will be invoked before chart rendering.

#### .on("postRender", function(chart){...})
This listener function will be invoked after chart finish rendering including all renderlets' logic.

#### .on("preRedraw", function(chart){...})
This listener function will be invoked before chart redrawing.

#### .on("postRedraw", function(chart){...})
This listener function will be invoked after chart finish redrawing including all renderlets' logic.

#### .on("filtered", function(chart, filter){...})
This listener function will be invoked after a filter is applied, added or removed.

#### .on("zoomed", function(chart, filter){...})
This listener function will be invoked after a zoom is triggered.

## <a name="marginable" href="#marginable">#</a>  Marginable

Marginable is a mixin that provides margin utility functions for both the Row Chart and Coordinate Grid Charts.

#### .margins([margins])
Get or set the margins for a particular coordinate grid chart instance. The margins is stored as an associative Javascript
array. Default margins: {top: 10, right: 50, bottom: 30, left: 30}.

The margins can be accessed directly from the getter.
```js
var leftMargin = chart.margins().left; // 30 by default
chart.margins().left = 50;
leftMargin = chart.margins().left; // now 50
```

## <a name="coordinate-grid-chart" href="#coordinate-grid-chart">#</a> CoordinateGrid Chart [Abstract] < [Color Chart](#color-chart) < [Base Chart](#base-chart)
Coordinate grid chart is an abstract base chart designed to support a number of coordinate grid based concrete chart types,
i.e. bar chart, line chart, and bubble chart.

#### .rangeChart([chart])
Get or set the range selection chart associated with this instance. Setting the range selection chart using this function
will automatically update its selection brush when the current chart zooms in. In return the given range chart will also
automatically attach this chart as its focus chart hence zoom in when range brush updates. See the
[Nasdaq 100 Index](http://dc-js.github.com/dc.js/) example for this effect in action.

#### .zoomScale([extent])
Get or set the scale extent for mouse zooms.

#### .zoomOutRestrict([true/false])
Get or set the a zoom restriction to be limited at the origional extent of the range chart

#### .g([gElement])
Get or set the root g element. This method is usually used to retrieve the g element in order to overlay custom svg drawing
programatically. **Caution**: The root g element is usually generated by dc.js internals, and resetting it might produce unpredictable result.

#### .mouseZoomable([boolean])
Set or get mouse zoom capability flag (default: false). When turned on the chart will be zoomable through mouse wheel
 . If range selector chart is also attached zooming will also update the range selection brush on associated range
 selector chart.

#### .chartBodyG()
Retreive the svg group for the chart body.

#### .x([xScale]) - **mandatory**
Get or set the x scale. x scale could be any [d3 quatitive scales](https://github.com/mbostock/d3/wiki/Quantitative-Scales).
For example a time scale for histogram or a linear/ordinal scale for visualizing data distribution.
```js
// set x to a linear scale
chart.x(d3.scale.linear().domain([-2500, 2500]))
// set x to a time scale to generate histogram
chart.x(d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
```

#### .xUnits([xUnits function])
Set or get the xUnits function. xUnits function is the coordinate grid chart uses to calculate number of data
projections on x axis such as number bars for a bar chart and number of dots for a line chart. This function is
expected to return an Javascript array of all data points on x axis. d3 time range functions d3.time.days, d3.time.months,
and d3.time.years are all valid xUnits function. dc.js also provides a few units function, see [Utilities](#util)
section for a list of built-in units functions. Default xUnits function is dc.units.integers.
```js
// set x units to day for a histogram
chart.xUnits(d3.time.days);
// set x units to month for a histogram
chart.xUnits(d3.time.months);
```
Custom xUnits function can be easily created using as long as it follows the following inteface:
```js
// units in integer
function(start, end, xDomain) {
    // simply calculates how many integers in the domain
    return Math.abs(end - start);
};

// fixed units
function(start, end, xDomain) {
    // be aware using fixed units will disable the focus/zoom ability on the chart
    return 1000;
};
```

#### .xAxis([xAxis])
Set or get the x axis used by a particular coordinate grid chart instance. This function is most useful when certain x
axis customization is required. x axis in dc.js is simply an instance of
[d3 axis object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-_axis) therefore it supports any valid d3 axis
manipulation. **Caution**: The x axis is typically generated by dc chart internal, resetting it might cause unexpected
outcome.
```js
// customize x axis tick format
chart.xAxis().tickFormat(function(v) {return v + "%";});
// customize x axis tick values
chart.xAxis().tickValues([0, 100, 200, 300]);
```

#### .elasticX([boolean])
Turn on/off elastic x axis. If x axis elasticity is turned on, then the grid chart will attempt to generate and
recalculate x axis range whenever redraw event is triggered.

#### .xAxisPadding([padding])
Set or get x axis padding when elastic x axis is turned on. The padding will be added to both end of the x axis if and
only if elasticX is turned on otherwise it will be simply ignored.

* padding - could be integer or percentage in string (e.g. "10%"). Padding can be applied to number or date.
When padding with date, integer represents number of days being padded while percentage string will be treated
as number.

#### .y([yScale])
Get or set the y scale. y scale is typically automatically generated by the chart implementation.

#### .yAxis([yAxis])
Set or get the y axis used by a particular coordinate grid chart instance. This function is most useful when certain y
axis customization is required. y axis in dc.js is simply an instance
of [d3 axis object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-_axis) therefore it supports any valid d3 axis
manipulation. **Caution**: The y axis is typically generated by dc chart internal, resetting it might cause unexpected
outcome.
```js
// customize y axis tick format
chart.yAxis().tickFormat(function(v) {return v + "%";});
// customize y axis tick values
chart.yAxis().tickValues([0, 100, 200, 300]);
```

#### .elasticY([boolean])
Turn on/off elastic y axis. If y axis elasticity is turned on, then the grid chart will attempt to generate and recalculate
y axis range whenever redraw event is triggered.

#### .renderHorizontalGridLines([boolean])
Turn on/off horizontal grid lines.

#### .renderVerticalGridLines([boolean])
Turn on/off vertical grid lines.

#### .yAxisPadding([padding])
Set or get y axis padding when elastic y axis is turned on. The padding will be added to the top of the y axis if and only
if elasticY is turned on otherwise it will be simply ignored.

* padding - could be integer or percentage in string (e.g. "10%"). Padding can be applied to number or date.
When padding with date, integer represents number of days being padded while percentage string will be treated
as number.

#### .round([rounding function])
Set or get the rounding function for x axis. Rounding is mainly used to provide stepping capability when in place
selection based filter is enable.
```js
// set x unit round to by month, this will make sure range selection brash will
// extend on a month-by-month basis
chart.round(d3.time.month.round);
```

#### .clipPadding([padding])
Get or set padding in pixel for clip path. Once set padding will be applied evenly to top, left, right, and bottom padding
 when clip path is generated. If set to zero, then the clip area will be exactly the chart body area minus the margins.
 Default: 5

#### .brushOn([boolean])
Turn on/off the brush based in-place range filter. When the brush is on then user will be able to  simply drag the mouse
across the chart to perform range filtering based on the extend of the brush. However turning on brush filter will essentially
disable other interactive elements on the chart such as the highlighting, tool-tip, and reference lines on a chart. Default
value is "true".

#### .focus([range])
Zoom this chart to focus on the given range. The given range should be an array containing only 2 element([start, end]) defining an range in x domain. If the range is not given or set to null, then the zoom will be reset. _For focus to work elasticX has to be turned off otherwise focus will be ignored._
```js
chart.renderlet(function(chart){
    // smooth the rendering through event throttling
    dc.events.trigger(function(){
        // focus some other chart to the range selected by user on this chart
        someOtherChart.focus(chart.filter());
    });
})
```

## <a name="color-chart" href="#color-chart">#</a> Color Chart [Abstract]
Color chart is an abstract chart functional class created to provide universal coloring support as a mix-in for any concrete
chart implementation.

#### .colors([colorScale or colorArray])
Retrieve current color scale or set a new color scale. This function accepts both d3 color scale and arbitrary color
array. By default d3.scale.category20c() is used.
```js
// color scale
chart.colors(d3.scale.category20b());
// arbitrary color array
chart.colors(["#a60000","#ff0000", "#ff4040","#ff7373","#67e667","#39e639","#00cc00"]);
```

#### .colorAccessor([colorAccessorFunction])
Set or get color accessor function. This function will be used to map a data point on crossfilter group to a specific
color value on the color scale. Default implementation of this function simply returns the next color on the scale using
the index of a group.
```js
// default index based color accessor
.colorAccessor(function(d, i){return i;})
// color accessor for a multi-value crossfilter reduction
.colorAccessor(function(d){return d.value.absGain;})
```

#### .colorDomain([domain])
Set or get the current domain for the color mapping function. This allows user to provide a custom domain for the mapping
function used to map the return value of the colorAccessor function to the target color range calculated based on the
color scale. You value can either be an array with the start and end of the range or a function returning an array. Functions
are passed the chart in their `this` context.
```js
// custom domain for month of year
chart.colorDomain([0, 11])
// custom domain for day of year
chart.colorDomain([0, 364])
// custom domain function that scales with the group value range
chart.colorDomain(function() {
    return [dc.utils.groupMin(this.group(), this.valueAccessor()),
     dc.utils.groupMax(this.group(), this.valueAccessor())];
});
```

## <a name="stackable-chart" href="#stackable-chart">#</a> Stackable Chart [Abstract]
Stackable chart is an abstract chart introduced to provide cross-chart support of stackability. Concrete implementation of
charts can then selectively mix-in this capability.

#### .stack(group[, name, retriever])
Stack a new crossfilter group into this chart with optionally a custom value retriever. All stacks in the same chart will
share the same key accessor therefore share the same set of keys. In more concrete words, imagine in a stacked bar chart
all bars will be positioned using the same set of keys on the x axis while stacked vertically. If name is specified then
it will be used to generate legend label.
```js
// stack group using default accessor
chart.stack(valueSumGroup)
// stack group using custom accessor
.stack(avgByDayGroup, function(d){return d.value.avgByDay;});
```

## <a name="abstract-bubble-chart" href="#abstract-bubble-chart">#</a> Abstract Bubble Chart [Abstract] < [Color Chart](#color-chart)
An abstraction provides reusable functionalities for any chart that needs to visualize data using bubbles.

#### .r([bubbleRadiusScale])
Get or set bubble radius scale. By default bubble chart uses ```d3.scale.linear().domain([0, 100])``` as it's r scale .

#### .radiusValueAccessor([radiusValueAccessor])
Get or set the radius value accessor function. The radius value accessor function if set will be used to retrieve data value
for each and every bubble rendered. The data retrieved then will be mapped using r scale to be used as the actual bubble
radius. In other words, this allows you to encode a data dimension using bubble size.

#### .minRadiusWithLabel([radius])
Get or set the minimum radius for label rendering. If a bubble's radius is less than this value then no label will be rendered.
Default value: 10.

#### .maxBubbleRelativeSize([relativeSize])
Get or set the maximum relative size of a bubble to the length of x axis. This value is useful when the radius differences among
different bubbles are too great. Default value: 0.3

## <a name="pie-chart" href="#pie-chart">#</a> Pie Chart [Concrete] < [Color Chart](#color-chart) < [Base Chart](#base-chart)
This chart is a concrete pie chart implementation usually used to visualize small number of categorical distributions.
Pie chart implementation uses keyAccessor to generate slices, and valueAccessor to calculate the size of each slice(key)
relatively to the total sum of all values.

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)

#### dc.pieChart(parent[, chartGroup])
Create a pie chart instance and attach it to the given parent element.

Parameters:

* parent : string - any valid d3 single selector representing typically a dom block element such
as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created pie chart instance

```js
// create a pie chart under #chart-container1 element using the default global chart group
var chart1 = dc.pieChart("#chart-container1");
// create a pie chart under #chart-container2 element using chart group A
var chart2 = dc.pieChart("#chart-container2", "chartGroupA");
```

#### .slicesCap([cap])
Get or set the maximum number of slices the pie chart will generate. Slices are ordered by its value from high to low.
 Other slices exeeding the cap will be rolled up into one single *Others* slice.

#### .innerRadius([innerRadius])
Get or set the inner radius on a particular pie chart instance. If inner radius is greater than 0px then the pie chart
will be essentially rendered as a doughnut chart. Default inner radius is 0px.

#### .radius([radius])
Get or set the radius on a particular pie chart instance. Default radius is 90px.

#### .cx()
Get center x coordinate position. This function is **not chainable**.

#### .cy()
Get center y coordinate position. This function is **not chainable**.

#### .minAngleForLabel([minAngle])
Get or set the minimal slice angle for label rendering. Any slice with a smaller angle will not render slice label.
Default min angle is 0.5.

## <a name="bar-chart" href="#bar-chart">#</a> Bar Chart [Concrete] < [Stackable Chart](#stackable-chart) < [CoordinateGrid Chart](#coordinate-grid-chart)
Concrete bar chart/histogram implementation.

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)

#### dc.barChart(parent[, chartGroup])
Create a bar chart instance and attach it to the given parent element.

Parameters:
* parent : string|compositeChart - any valid d3 single selector representing typically a dom block element such
as a div, or if this bar chart is a sub-chart in a [Composite Chart](#composite-chart) then pass in the parent composite chart instance.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created bar chart instance

```js
// create a bar chart under #chart-container1 element using the default global chart group
var chart1 = dc.barChart("#chart-container1");
// create a bar chart under #chart-container2 element using chart group A
var chart2 = dc.barChart("#chart-container2", "chartGroupA");
// create a sub-chart under a composite parent chart
var chart3 = dc.barChart(compositeChart);
```

#### .centerBar(boolean)
Whether the bar chart will render each bar centered around the data position on x axis. Default to false.

#### .gap(gapBetweenBars)
Manually set fixed gap (in px) between bars instead of relying on the default auto-generated gap. By default bar chart
implementation will calculate and set the gap automatically based on the number of data points and the length of the x axis.

## <a name="line-chart" href="#line-chart">#</a> Line Chart [Concrete] < [Stackable Chart](#stackable-chart) < [CoordinateGrid Chart](#coordinate-grid-chart)
Concrete line/area chart implementation.

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)

#### dc.lineChart(parent[, chartGroup])
Create a line chart instance and attach it to the given parent element.

Parameters:

* parent : string|compositeChart - any valid d3 single selector representing typically a dom block element such
as a div, or if this line chart is a sub-chart in a [Composite Chart](#composite-chart) then pass in the parent composite chart instance.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created line chart instance

```js
// create a line chart under #chart-container1 element using the default global chart group
var chart1 = dc.lineChart("#chart-container1");
// create a line chart under #chart-container2 element using chart group A
var chart2 = dc.lineChart("#chart-container2", "chartGroupA");
// create a sub-chart under a composite parent chart
var chart3 = dc.lineChart(compositeChart);
```

#### .renderArea([boolean])
Get or set render area flag. If the flag is set to true then the chart will render the area beneath each line and effectively
becomes an area chart.

#### .dotRadius([dotRadius])
Get or set the radius (in px) for data points. Default dot radius is 5.

## <a name="data-count" href="#data-count">#</a> Data Count Widget [Concrete] < [Base Chart](#base-chart)
Data count is a simple widget designed to display total number records in the data set vs. the number records selected
by the current filters. Once created data count widget will automatically update the text content of the following elements
under the parent element.

* ".total-count" - total number of records
* ".filter-count" - number of records matched by the current filters

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)

#### dc.dataCount(parent[, chartGroup])
Create a data count widget instance and attach it to the given parent element.

Parameters:

* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created data count widget instance

#### .dimension(allData) - **mandatory**
For data count widget the only valid dimension is the entire data set.

#### .group(groupAll) - **mandatory**
For data count widget the only valid group is the all group.

```js
var ndx = crossfilter(data);
var all = ndx.groupAll();

dc.dataCount(".dc-data-count")
 .dimension(ndx)
 .group(all);
```

## <a name="data-table" href="#data-table">#</a> Data Table Widget [Concrete] < [Base Chart](#base-chart)
Data table is a simple widget designed to list crossfilter focused data set (rows being filtered) in a good old tabular
fashion.

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)

#### dc.dataTable(parent[, chartGroup])
Create a data table widget instance and attach it to the given parent element.

Parameters:
* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created data table widget instance

#### .size([size])
Get or set the table size which determines the number of rows displayed by the widget.

#### .columns([columnFunctionArray])
Get or set column functions. Data table widget uses an array of functions to generate dynamic columns. Column functions are
simple javascript function with only one input argument d which represents a row in the data set, and the return value of
these functions will be used directly to generate table content for each cell.

```js
    chart.columns([
        function(d) {
            return d.date;
        },
        function(d) {
            return d.open;
        },
        function(d) {
            return d.close;
        },
        function(d) {
            return numberFormat(d.close - d.open);
        },
        function(d) {
            return d.volume;
        }
    ]);
```

#### .sortBy([sortByFunction])
Get or set sort-by function. This function works as a value accessor at row level and returns a particular field to be sorted
by. Default value: ``` function(d) {return d;}; ```

```js
   chart.sortBy(function(d) {
        return d.date;
    });
```

#### .order([order])
Get or set sort order. Default value: ``` d3.ascending ```

```js
    chart.order(d3.descending);
```

## <a name="bubble-chart" href="#bubble-chart">#</a> Bubble Chart [Concrete] < [Abstract Bubble Chart](#abstract-bubble-chart) < [CoordinateGrid Chart](#coordinate-grid-chart)
A concrete implementation of a general purpose bubble chart that allows data visualization using the following dimensions:

* x axis position
* y axis position
* bubble radius
* color

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [US Venture Capital Landscape 2011](http://dc-js.github.com/dc.js/vc/index.html)

#### dc.bubbleChart(parent[, chartGroup])
Create a bubble chart instance and attach it to the given parent element.

Parameters:
* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created bubble chart instance

```js
// create a bubble chart under #chart-container1 element using the default global chart group
var bubbleChart1 = dc.bubbleChart("#chart-container1");
// create a bubble chart under #chart-container2 element using chart group A
var bubbleChart2 = dc.bubbleChart("#chart-container2", "chartGroupA");
```

#### .elasticRadius([boolean])
Turn on or off elastic bubble radius feature. If this feature is turned on, then bubble radiuses will be automatically rescaled
to fit the chart better.

## <a name="composite-chart" href="#composite-chart">#</a> Composite Chart [Concrete] < [CoordinateGrid Chart](#coordinate-grid-chart)
Composite chart is a special kind of chart that resides somewhere between abstract and concrete charts. It does not
generate data visualization directly, but rather working with other concrete charts to do the job. You can essentially
overlay(compose) different bar/line/area charts in a single composite chart to achieve some quite flexible charting
effects.

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)

#### dc.compositeChart(parent[, chartGroup])
Create a composite chart instance and attach it to the given parent element.

Parameters:
* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created composite chart instance

```js
// create a composite chart under #chart-container1 element using the default global chart group
var compositeChart1 = dc.compositeChart("#chart-container1");
// create a composite chart under #chart-container2 element using chart group A
var compositeChart2 = dc.compositeChart("#chart-container2", "chartGroupA");
```

#### .compose(subChartArray)
Combine the given charts into one single composite coordinate grid chart.

```js
// compose the given charts in the array into one single composite chart
moveChart.compose([
    // when creating sub-chart you need to pass in the parent chart
    dc.lineChart(moveChart)
        .group(indexAvgByMonthGroup) // if group is missing then parent's group will be used
        .valueAccessor(function(d){return d.value.avg;})
        // most of the normal functions will continue to work in a composed chart
        .renderArea(true)
        .stack(monthlyMoveGroup, function(d){return d.value;})
        .title(function(d){
            var value = d.value.avg?d.value.avg:d.value;
            if(isNaN(value)) value = 0;
            return dateFormat(d.key) + "\n" + numberFormat(value);
        }),
    dc.barChart(moveChart)
        .group(volumeByMonthGroup)
        .centerBar(true)
]);
```

## <a name="geo-choropleth-chart" href="#geo-choropleth-chart">#</a> Geo Choropleth Chart [Concrete] < [Color Chart](#color-chart) < [Base Chart](#base-chart)
Geo choropleth chart is design to make creating crossfilter driven choropleth map from GeoJson data an easy process. This
chart implementation was inspired by [the great d3 choropleth example](http://bl.ocks.org/4060606).

Examples:
* [US Venture Capital Landscape 2011](http://dc-js.github.com/dc.js/vc/index.html)

#### dc.geoChoroplethChart(parent[, chartGroup])
Create a choropleth chart instance and attach it to the given parent element.

Parameters:
* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created choropleth chart instance

```js
// create a choropleth chart under "#us-chart" element using the default global chart group
var chart1 = dc.geoChoroplethChart("#us-chart");
// create a choropleth chart under "#us-chart2" element using chart group A
var chart2 = dc.compositeChart("#us-chart2", "chartGroupA");
```

#### .overlayGeoJson(json, name, keyAccessor) - **mandatory**
Use this function to insert a new GeoJson map layer. This function can be invoked multiple times if you have multiple GeoJson
data layer to render on top of each other. If you overlay mutiple layers with the same name the new overlay will simply
override the existing one.

Parameters:
* json - GeoJson feed
* name - name of the layer
* keyAccessor - accessor function used to extract "key" from the GeoJson data. Key extracted by this function should match
 the keys generated in crossfilter groups.

```js
// insert a layer for rendering US states
chart.overlayGeoJson(statesJson.features, "state", function(d) {
    return d.properties.name;
});
```

#### .projection(projection)
Set custom geo projection function. Available [d3 geo projection functions](https://github.com/mbostock/d3/wiki/Geo-Projections).
Default value: albersUsa.

#### .geoJsons()
Return all GeoJson layers currently registered with thit chart. The returned array is a reference to this chart's internal
registration data structure without copying thus any modification to this array will also modify this chart's internal
registration.

Return:
An array of objects containing fields {name, data, accessor}

#### .removeGeoJson(name)
Remove a GeoJson layer from this chart by name

Return: chart instance

## <a name="bubble-overlay-chart" href="#bubble-overlay-chart">#</a> Bubble Overlay Chart [Concrete] < [Abstract Bubble Chart](#abstract-bubble-chart) < [Base Chart](#base-chart)
Bubble overlay chart is quite different from the typical bubble chart. With bubble overlay chart you can arbitrarily place
a finite number of bubbles on an existing svg or bitmap image (overlay on top of it), thus losing the typical x and y
positioning that we are used to whiling retaining the capability to visualize data using it's bubble radius and
coloring.

Examples:
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)

#### dc.bubbleOverlay(parent[, chartGroup])
Create a bubble overlay chart instance and attach it to the given parent element.

Parameters:
* parent : string - any valid d3 single selector representing typically a dom block element such as a div. Typically
this element should also be the parent of the underlying image.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created bubble overlay chart instance

```js
// create a bubble overlay chart on top of "#chart-container1 svg" element using the default global chart group
var bubbleChart1 = dc.bubbleOverlayChart("#chart-container1").svg(d3.select("#chart-container1 svg"));
// create a bubble overlay chart on top of "#chart-container2 svg" element using chart group A
var bubbleChart2 = dc.compositeChart("#chart-container2", "chartGroupA").svg(d3.select("#chart-container2 svg"));
```

#### .svg(imageElement) - **mandatory**
Set the underlying svg image element. Unlike other dc charts this chart will not generate svg element therefore bubble overlay
chart will not work if this function is not properly invoked. If the underlying image is a bitmap, then an empty svg will need
to be manually created on top of the image.

```js
// set up underlying svg element
chart.svg(d3.select("#chart svg"));
```

#### .point(name, x, y) - **mandatory**
Set up a data point on the overlay. The name of a data point should match a specific "key" among data groups generated using keyAccessor.
If a match is found (point name <-> data group key) then a bubble will be automatically generated at the position specified by the
function. x and y value specified here are relative to the underlying svg.

## <a name="row-chart" href="#row-chart">#</a> Row Chart [Concrete] < [Color Chart](#color-chart) < [Base Chart](#base-chart)
Concrete row chart implementation.

#### dc.rowChart(parent[, chartGroup])
Create a row chart instance and attach it to the given parent element.

Parameters:

* parent : string - any valid d3 single selector representing typically a dom block element such as a div.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed in a certain chart group then any interaction with such instance will only trigger events and redraw within the same chart group.

Return a newly created row chart instance

```js
// create a row chart under #chart-container1 element using the default global chart group
var chart1 = dc.rowChart("#chart-container1");
// create a row chart under #chart-container2 element using chart group A
var chart2 = dc.rowChart("#chart-container2", "chartGroupA");
```

#### .gap([gap])
Get or set the vertical gap space between rows on a particular row chart instance. Default gap is 5px;

#### .elasticX([boolean])
Get or set the elasticity on x axis. If this attribute is set to true, then the x axis will rescle to auto-fit the data
range when filtered.

#### .labelOffsetX([x])
Get or set the x offset (horizontal space to the top left corner of a row) for labels on a particular row chart. Default x offset is 10px;

#### .labelOffsetY([y])
Get of set the y offset (vertical space to the top left corner of a row) for labels on a particular row chart. Default y offset is 15px;

## <a name="legend" href="#legend">#</a> Legend [Concrete]
Legend is a attachable widget that can be added to other dc charts to render horizontal legend labels.

```js
chart.legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
```

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)

#### .x([value])
Set or get x coordinate for legend widget. Default value: 0.

#### .y([value])
Set or get y coordinate for legend widget. Default value: 0.

#### .gap([value])
Set or get gap between legend items. Default value: 5.

#### .itemHeight([value])
Set or get legend item height. Default value: 12.

#### .othersLabel([label])
Get or set the label for *Others* slice when slices cap is specified. Default label is **Others**.

#### .othersGrouper([grouperFunction])
Get or set the grouper funciton that will perform the insersion of data for the *Others* slice if the slices cap is
specified. By default the grouper function implements the following logic, you can and should change this function to
match your data structure. If set to a falsy value, no others will be added;
```js
function (data, sum) {
    data.push({"key": _othersLabel, "value": sum });
};
```

## <a name="number-display" href="#number-display">#</a> Number Display [Concrete] < [Base Chart](#base-chart)
A display of a single numeric value.

Examples:

* [Test Example](http://dc-js.github.io/dc.js/examples/number.html)

#### dc.numberDisplay(parent[, chartGroup])
Create a Number Display instance and attach it to the given parent element.

Unlike other charts, you do not need to set a dimension. Instead a valid group object must be provided and valueAccessor that is expected to return a single value.

Parameters:

* parent : string - any valid d3 single selector representing typically a dom block element such as a div or span
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in. Once a chart is placed
in a certain chart group then any interaction with such instance will only trigger events and redraw within the same
chart group.

Return:
A newly created number display instance

```js
// create a number display under #chart-container1 element using the default global chart group
var display1 = dc.numberDisplay("#chart-container1");
```

#### .value()
Calculate and return the underlying value of the display

#### .formatNumber([formatter])
Get or set a function to format the value for the display. By default `d3.format(".2s");` is used.
