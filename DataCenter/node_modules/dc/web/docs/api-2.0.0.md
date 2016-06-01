# DC API
  * [Utilities](#utilities)
  * [Filters](#filters)
  * [Base Mixin](#base-mixin)
  * [Listeners](#listeners)
  * [Margin Mixin](#margin-mixin)
  * [Color Mixin](#color-mixin)
  * [Coordinate Grid Mixin](#coordinate-grid-mixin)
  * [Stack Mixin](#stack-mixin)
  * [Cap Mixin](#cap-mixin)
  * [Bubble Mixin](#bubble-mixin)
  * [Pie Chart](#pie-chart)
  * [Bar Chart](#bar-chart)
  * [Line Chart](#line-chart)
  * [Data Count Widget](#data-count-widget)
  * [Data Table Widget](#data-table-widget)
  * [Data Grid Widget](#data-grid-widget)
  * [Bubble Chart](#bubble-chart)
  * [Composite Chart](#composite-chart)
  * [Series Chart](#series-chart)
  * [Geo Choropleth Chart](#geo-choropleth-chart)
  * [Bubble Overlay Chart](#bubble-overlay-chart)
  * [Row Chart](#row-chart)
  * [Legend](#legend)
  * [Scatter Plot](#scatter-plot)
  * [Number Display Widget](#number-display-widget)
  * [Heat Map](#heat-map)
  * [Box Plot](#box-plot)

#### Version 2.0.0-alpha.5
The entire dc.js library is scoped under the **dc** name space. It does not introduce anything else
into the global name space.
#### Function Chaining
Most dc functions are designed to allow function chaining, meaning they return the current chart
instance whenever it is appropriate. This way chart configuration can be written in the following
style:
```js
chart.width(300)
.height(300)
.filter('sunday')
```
The getter forms of functions do not participate in function chaining because they necessarily
return values that are not the chart.  (Although some, such as `.svg` and `.xAxis`, return values
that are chainable d3 objects.)

## Utilities

#### dc.filterAll([chartGroup])
Clear all filters on all charts within the given chart group. If the chart group is not given then
only charts that belong to the default chart group will be reset.

#### dc.refocusAll([chartGroup])
Reset zoom level / focus on all charts that belong to the given chart group. If the chart group is
not given then only charts that belong to the default chart group will be reset.

#### dc.renderAll([chartGroup])
Re-render all charts belong to the given chart group. If the chart group is not given then only
charts that belong to the default chart group will be re-rendered.

#### dc.redrawAll([chartGroup])
Redraw all charts belong to the given chart group. If the chart group is not given then only charts
that belong to the default chart group will be re-drawn. Redraw is different from re-render since
when redrawing dc tries to update the graphic incrementally, using transitions, instead of starting
from scratch.

#### dc.disableTransitions
If this boolean is set truthy, all transitions will be disabled, and changes to the charts will happen
immediately.  Default: false

#### dc.units.integers
`dc.units.integers` is the default value for `xUnits` for the [Coordinate Grid
Chart](#coordinate-grid-chart) and should be used when the x values are a sequence of integers.

It is a function that counts the number of integers in the range supplied in its start and end parameters.

```js
chart.xUnits(dc.units.integers) // already the default
```

#### dc.units.ordinal
This argument can be passed to the `xUnits` function of the to specify ordinal units for the x
axis. Usually this parameter is used in combination with passing `d3.scale.ordinal()` to `.x`.

It just returns the domain passed to it, which for ordinal charts is an array of all values.

```js
chart.xUnits(dc.units.ordinal)
.x(d3.scale.ordinal())
```

#### dc.units.fp.precision(precision)
This function generates an argument for the [Coordinate Grid Chart's](#coordinate-grid-chart)
`xUnits` function specifying that the x values are floating-point numbers with the given
precision.

The returned function determines how many values at the given precision will fit into the range
supplied in its start and end parameters.

```js
// specify values (and ticks) every 0.1 units
chart.xUnits(dc.units.fp.precision(0.1)
// there are 500 units between 0.5 and 1 if the precision is 0.001
var thousandths = dc.units.fp.precision(0.001);
thousandths(0.5, 1.0) // returns 500
```

#### dc.events.trigger(function[, delay])
This function triggers a throttled event function with a specified delay (in milli-seconds).  Events
that are triggered repetitively due to user interaction such brush dragging might flood the library
and invoke more renders than can be executed in time. Using this function to wrap your event
function allows the library to smooth out the rendering by throttling events and only responding to
the most recent event.

```js
chart.renderlet(function(chart){
    // smooth the rendering through event throttling
    dc.events.trigger(function(){
        // focus some other chart to the range selected by user on this chart
        someOtherChart.focus(chart.filter());
    });
})
```

## Filters
The dc.js filters are functions which are passed into crossfilter to chose which records will be
accumulated to produce values for the charts.  In the crossfilter model, any filters applied on one
dimension will affect all the other dimensions but not that one.  dc always applies a filter
function to the dimension; the function combines multiple filters and if any of them accept a
record, it is filtered in.

These filter constructors are used as appropriate by the various charts to implement brushing.  We
mention below which chart uses which filter.  In some cases, many instances of a filter will be added.

#### dc.filters.RangedFilter(low, high)
RangedFilter is a filter which accepts keys between `low` and `high`.  It is used to implement X
axis brushing for the [coordinate grid charts](#coordinate-grid-mixin).

#### dc.filters.TwoDimensionalFilter(array)
TwoDimensionalFilter is a filter which accepts a single two-dimensional value.  It is used by the
[heat map chart](#heat-map) to include particular cells as they are clicked.  (Rows and columns are
filtered by filtering all the cells in the row or column.)

#### dc.filters.RangedTwoDimensionalFilter(array)
The RangedTwoDimensionalFilter allows filtering all values which fit within a rectangular
region. It is used by the [scatter plot](#scatter-plot) to implement rectangular brushing.

It takes two two-dimensional points in the form `[[x1,y1],[x2,y2]]`, and normalizes them so that
`x1 <= x2` and `y1 <- y2`. It then returns a filter which accepts any points which are in the
rectangular range including the lower values but excluding the higher values.

If an array of two values are given to the RangedTwoDimensionalFilter, it interprets the values as
two x coordinates `x1` and `x2` and returns a filter which accepts any points for which `x1 <= x <
x2`.

## Base Mixin
Base Mixin is an abstract functional object representing a basic dc chart object
for all chart and widget implementations. Methods from the Base Mixin are inherited
and available on all chart implementation in the DC library.

#### .width([value])
Set or get the width attribute of a chart. See `.height` below for further description of the
behavior.

#### .height([value])
Set or get the height attribute of a chart. The height is applied to the SVG element generated by
the chart when rendered (or rerendered). If a value is given, then it will be used to calculate
the new height and the chart returned for method chaining.  The value can either be a numeric, a
function, or falsy. If no value is specified then the value of the current height attribute will
be returned.

By default, without an explicit height being given, the chart will select the width of its
anchor element. If that isn't possible it defaults to 200. Setting the value falsy will return
the chart to the default behavior

Examples:

```js
chart.height(250); // Set the chart's height to 250px;
chart.height(function(anchor) { return doSomethingWith(anchor); }); // set the chart's height with a function
chart.height(null); // reset the height to the default auto calculation
```

#### .minWidth([value])
Set or get the minimum width attribute of a chart. This only applicable if the width is
calculated by dc.

#### .minHeight([value])
Set or get the minimum height attribute of a chart. This only applicable if the height is
calculated by dc.

#### .dimension([value]) - **mandatory**
Set or get the dimension attribute of a chart. In dc a dimension can be any valid [crossfilter
dimension](https://github.com/square/crossfilter/wiki/API-Reference#wiki-dimension).

If a value is given, then it will be used as the new dimension. If no value is specified then
the current dimension will be returned.

#### .data([callback])
Set the data callback or retrieve the chart's data set. The data callback is passed the chart's
group and by default will return `group.all()`. This behavior may be modified to, for instance,
return only the top 5 groups:
```
    chart.data(function(group) {
        return group.top(5);
    });
```

#### .group([value, [name]]) - **mandatory**
Set or get the group attribute of a chart. In dc a group is a [crossfilter
group](https://github.com/square/crossfilter/wiki/API-Reference#wiki-group). Usually the group
should be created from the particular dimension associated with the same chart. If a value is
given, then it will be used as the new group.

If no value specified then the current group will be returned.
If `name` is specified then it will be used to generate legend label.

#### .ordering([orderFunction])
Get or set an accessor to order ordinal charts

#### .filterAll()
Clear all filters associated with this chart.

#### .select(selector)
Execute d3 single selection in the chart's scope using the given selector and return the d3
selection. Roughly the same as:
```js
d3.select('#chart-id').select(selector);
```
This function is **not chainable** since it does not return a chart instance; however the d3
selection result can be chained to d3 function calls.

#### .selectAll(selector)
Execute in scope d3 selectAll using the given selector and return d3 selection result. Roughly
the same as:
```js
d3.select('#chart-id').selectAll(selector);
```
This function is **not chainable** since it does not return a chart instance; however the d3
selection result can be chained to d3 function calls.

#### .anchor([anchorChart|anchorSelector|anchorNode], [chartGroup])
Set the svg root to either be an existing chart's root; or any valid [d3 single
selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying a dom
block element such as a div; or a dom element or d3 selection. Optionally registers the chart
within the chartGroup. This class is called internally on chart initialization, but be called
again to relocate the chart. However, it will orphan any previously created SVG elements.

#### .anchorName()
Returns the dom id for the chart's anchored location.

#### .root([rootElement])
Returns the root element where a chart resides. Usually it will be the parent div element where
the svg was created. You can also pass in a new root element however this is usually handled by
dc internally. Resetting the root element on a chart outside of dc internals may have
unexpected consequences.

#### .svg([svgElement])
Returns the top svg element for this specific chart. You can also pass in a new svg element,
however this is usually handled by dc internally. Resetting the svg element on a chart outside
of dc internals may have unexpected consequences.

#### .resetSvg()
Remove the chart's SVG elements from the dom and recreate the container SVG element.

#### .filterPrinter([filterPrinterFunction])
Set or get the filter printer function. The filter printer function is used to generate human
friendly text for filter value(s) associated with the chart instance. By default dc charts use a
default filter printer `dc.printers.filter` that provides simple printing support for both
single value and ranged filters.

#### .turnOnControls() & .turnOffControls()
Turn on/off optional control elements within the root element. dc currently supports the
following html control elements.

* root.selectAll('.reset') - elements are turned on if the chart has an active filter. This type
 of control element is usually used to store a reset link to allow user to reset filter on a
 certain chart. This element will be turned off automatically if the filter is cleared.
* root.selectAll('.filter') elements are turned on if the chart has an active filter. The text
 content of this element is then replaced with the current filter value using the filter printer
 function. This type of element will be turned off automatically if the filter is cleared.

#### .transitionDuration([duration])
Set or get the animation transition duration(in milliseconds) for this chart instance. Default
duration is 750ms.

#### .render()
Invoking this method will force the chart to re-render everything from scratch. Generally it
should only be used to render the chart for the first time on the page or if you want to make
sure everything is redrawn from scratch instead of relying on the default incremental redrawing
behaviour.

#### .redraw()
Calling redraw will cause the chart to re-render data changes incrementally. If there is no
change in the underlying data dimension then calling this method will have no effect on the
chart. Most chart interaction in dc will automatically trigger this method through internal
events (in particular [dc.redrawAll](#dcredrawallchartgroup)); therefore, you only need to
manually invoke this function if data is manipulated outside of dc's control (for example if
data is loaded in the background using `crossfilter.add()`).

#### .hasFilterHandler([function])
Set or get the has filter handler. The has filter handler is a function that checks to see if
the chart's current filters include a specific filter.  Using a custom has filter handler allows
you to change the way filters are checked for and replaced.

```js
// default has filter handler
function (filters, filter) {
    if (filter === null || typeof(filter) === 'undefined') {
        return filters.length > 0;
    }
    return filters.some(function (f) {
        return filter <= f && filter >= f;
    });
}

// custom filter handler (no-op)
chart.hasFilterHandler(function(filters, filter) {
    return false;
});
```

#### .hasFilter([filter])
Check whether any active filter or a specific filter is associated with particular chart instance.
This function is **not chainable**.

#### .removeFilterHandler([function])
Set or get the remove filter handler. The remove filter handler is a function that removes a
filter from the chart's current filters. Using a custom remove filter handler allows you to
change how filters are removed or perform additional work when removing a filter, e.g. when
using a filter server other than crossfilter.

Any changes should modify the `filters` array argument and return that array.

```js
// default remove filter handler
function (filters, filter) {
    for (var i = 0; i < filters.length; i++) {
        if (filters[i] <= filter && filters[i] >= filter) {
            filters.splice(i, 1);
            break;
        }
    }
    return filters;
}

// custom filter handler (no-op)
chart.removeFilterHandler(function(filters, filter) {
    return filters;
});
```

#### .addFilterHandler([function])
Set or get the add filter handler. The add filter handler is a function that adds a filter to
the chart's filter list. Using a custom add filter handler allows you to change the way filters
are added or perform additional work when adding a filter, e.g. when using a filter server other
than crossfilter.

Any changes should modify the `filters` array argument and return that array.

```js
// default add filter handler
function (filters, filter) {
    filters.push(filter);
    return filters;
}

// custom filter handler (no-op)
chart.addFilterHandler(function(filters, filter) {
    return filters;
});
```

#### .resetFilterHandler([function])
Set or get the reset filter handler. The reset filter handler is a function that resets the
chart's filter list by returning a new list. Using a custom reset filter handler allows you to
change the way filters are reset, or perform additional work when resetting the filters,
e.g. when using a filter server other than crossfilter.

This function should return an array.

```js
// default remove filter handler
function (filters) {
    return [];
}

// custom filter handler (no-op)
chart.resetFilterHandler(function(filters) {
    return filters;
});
```

#### .filter([filterValue])
Filter the chart by the given value or return the current filter if the input parameter is missing.
```js
// filter by a single string
chart.filter('Sunday');
// filter by a single age
chart.filter(18);
```

#### .filters()
Returns all current filters. This method does not perform defensive cloning of the internal
filter array before returning, therefore any modification of the returned array will effect the
chart's internal filter storage.

#### .onClick(datum)
This function is passed to d3 as the onClick handler for each chart. The default behavior is to
filter on the clicked datum (passed to the callback) and redraw the chart group.

#### .filterHandler([function])
Set or get the filter handler. The filter handler is a function that performs the filter action
on a specific dimension. Using a custom filter handler allows you to perform additional logic
before or after filtering.

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
Set or get the key accessor function. The key accessor function is used to retrieve the key
value from the crossfilter group. Key values are used differently in different charts, for
example keys correspond to slices in a pie chart and x axis positions in a grid coordinate chart.
```js
// default key accessor
chart.keyAccessor(function(d) { return d.key; });
// custom key accessor for a multi-value crossfilter reduction
chart.keyAccessor(function(p) { return p.value.absGain; });
```

#### .valueAccessor([valueAccessorFunction])
Set or get the value accessor function. The value accessor function is used to retrieve the
value from the crossfilter group. Group values are used differently in different charts, for
example values correspond to slice sizes in a pie chart and y axis positions in a grid
coordinate chart.
```js
// default value accessor
chart.valueAccessor(function(d) { return d.value; });
// custom value accessor for a multi-value crossfilter reduction
chart.valueAccessor(function(p) { return p.value.percentageGain; });
```

#### .label([labelFunction])
Set or get the label function. The chart class will use this function to render labels for each
child element in the chart, e.g. slices in a pie chart or bubbles in a bubble chart. Not every
chart supports the label function for example bar chart and line chart do not use this function
at all.
```js
// default label function just return the key
chart.label(function(d) { return d.key; });
// label function has access to the standard d3 data binding and can get quite complicated
chart.label(function(d) { return d.data.key + '(' + Math.floor(d.data.value / all.value() * 100) + '%)'; });
```

#### .renderLabel(boolean)
Turn on/off label rendering

#### .title([titleFunction])
Set or get the title function. The chart class will use this function to render the svg title
(usually interpreted by browser as tooltips) for each child element in the chart, e.g. a slice
in a pie chart or a bubble in a bubble chart. Almost every chart supports the title function;
however in grid coordinate charts you need to turn off the brush in order to see titles, because
otherwise the brush layer will block tooltip triggering.
```js
// default title function just return the key
chart.title(function(d) { return d.key + ': ' + d.value; });
// title function has access to the standard d3 data binding and can get quite complicated
chart.title(function(p) {
    return p.key.getFullYear()
        + '\n'
        + 'Index Gain: ' + numberFormat(p.value.absGain) + '\n'
        + 'Index Gain in Percentage: ' + numberFormat(p.value.percentageGain) + '%\n'
        + 'Fluctuation / Index Ratio: ' + numberFormat(p.value.fluctuationPercentage) + '%';
});
```

#### .renderTitle(boolean)
Turn on/off title rendering, or return the state of the render title flag if no arguments are
given.

#### .renderlet(renderletFunction)
A renderlet is similar to an event listener on rendering event. Multiple renderlets can be added
to an individual chart.  Each time a chart is rerendered or redrawn the renderlets are invoked
right after the chart finishes its own drawing routine, giving you a way to modify the svg
elements. Renderlet functions take the chart instance as the only input parameter and you can
use the dc API or use raw d3 to achieve pretty much any effect.
```js
// renderlet function
chart.renderlet(function(chart){
    // mix of dc API and d3 manipulation
    chart.select('g.y').style('display', 'none');
    // its a closure so you can also access other chart variable available in the closure scope
    moveChart.filter(chart.filter());
});
```

#### .chartGroup([group])
Get or set the chart group to which this chart belongs. Chart groups are rendered or redrawn
together since it is expected they share the same underlying crossfilter data set.

#### .expireCache()
Expire the internal chart cache. dc charts cache some data internally on a per chart basis to
speed up rendering and avoid unnecessary calculation; however it might be useful to clear the
cache if you have changed state which will affect rendering.  For example if you invoke the
`crossfilter.add` function or reset group or dimension after rendering it is a good idea to
clear the cache to make sure charts are rendered properly.

#### .legend([dc.legend])
Attach a dc.legend widget to this chart. The legend widget will automatically draw legend labels
based on the color setting and names associated with each group.

```js
chart.legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
```

#### .chartID()
Returns the internal numeric ID of the chart.

#### .options(optionsObject)
Set chart options using a configuration object. Each key in the object will cause the method of
the same name to be called with the value to set that attribute for the chart.

Example:
```
chart.options({dimension: myDimension, group: myGroup});
```

## Listeners
All dc chart instance supports the following listeners.

#### .on('preRender', function(chart){...})
This listener function will be invoked before chart rendering.

#### .on('postRender', function(chart){...})
This listener function will be invoked after chart finish rendering including all renderlets' logic.

#### .on('preRedraw', function(chart){...})
This listener function will be invoked before chart redrawing.

#### .on('postRedraw', function(chart){...})
This listener function will be invoked after chart finish redrawing including all renderlets' logic.

#### .on('filtered', function(chart, filter){...})
This listener function will be invoked after a filter is applied, added or removed.

#### .on('zoomed', function(chart, filter){...})
This listener function will be invoked after a zoom is triggered.

## Margin Mixin
Margin is a mixin that provides margin utility functions for both the Row Chart and Coordinate Grid
Charts.

#### .margins([margins])
Get or set the margins for a particular coordinate grid chart instance. The margins is stored as
an associative Javascript array. Default margins: {top: 10, right: 50, bottom: 30, left: 30}.

The margins can be accessed directly from the getter.
```js
var leftMargin = chart.margins().left; // 30 by default
chart.margins().left = 50;
leftMargin = chart.margins().left; // now 50
```

## Color Mixin
The Color Mixin is an abstract chart functional class providing universal coloring support
as a mix-in for any concrete chart implementation.

#### .colors([colorScale])
Retrieve current color scale or set a new color scale. This methods accepts any function that
operates like a d3 scale. If not set the default is
`d3.scale.category20c()`.
```js
// alternate categorical scale
chart.colors(d3.scale.category20b());

// ordinal scale
chart.colors(d3.scale.ordinal().range(['red','green','blue']));
// convenience method, the same as above
chart.ordinalColors(['red','green','blue']);

// set a linear scale
chart.linearColors(["#4575b4", "#ffffbf", "#a50026"]);
```

#### .ordinalColors(r)
Convenience method to set the color scale to d3.scale.ordinal with range `r`.

#### .linearColors(r)
Convenience method to set the color scale to an Hcl interpolated linear scale with range `r`.

#### .colorAccessor([colorAccessorFunction])
Set or the get color accessor function. This function will be used to map a data point in a
crossfilter group to a color value on the color scale. The default function uses the key
accessor.
```js
// default index based color accessor
.colorAccessor(function (d, i){return i;})
// color accessor for a multi-value crossfilter reduction
.colorAccessor(function (d){return d.value.absGain;})
```

#### .colorDomain([domain])
Set or get the current domain for the color mapping function. The domain must be supplied as an
array.

Note: previously this method accepted a callback function. Instead you may use a custom scale
set by `.colors`.

#### .calculateColorDomain()
Set the domain by determining the min and max values as retrieved by `.colorAccessor` over the
chart's dataset.

#### .getColor(d [, i])
Get the color for the datum d and counter i. This is used internally by charts to retrieve a color.

#### .colorCalculator([value])
Gets or sets chart.getColor.

## Coordinate Grid Mixin
Includes: [Color Mixin](#color-mixin), [Margin Mixin](#margin-mixin), [Base Mixin](#base-mixin)

Coordinate Grid is an abstract base chart designed to support a number of coordinate grid based
concrete chart types, e.g. bar chart, line chart, and bubble chart.

#### .rangeChart([chart])
Get or set the range selection chart associated with this instance. Setting the range selection
chart using this function will automatically update its selection brush when the current chart
zooms in. In return the given range chart will also automatically attach this chart as its focus
chart hence zoom in when range brush updates. See the [Nasdaq 100
Index](http://dc-js.github.com/dc.js/) example for this effect in action.

#### .zoomScale([extent])
Get or set the scale extent for mouse zooms.

#### .zoomOutRestrict([true/false])
Get or set the zoom restriction for the chart. If true limits the zoom to origional domain of the chart.

#### .g([gElement])
Get or set the root g element. This method is usually used to retrieve the g element in order to
overlay custom svg drawing programatically. **Caution**: The root g element is usually generated
by dc.js internals, and resetting it might produce unpredictable result.

#### .mouseZoomable([boolean])
Set or get mouse zoom capability flag (default: false). When turned on the chart will be
zoomable using the mouse wheel. If the range selector chart is attached zooming will also update
the range selection brush on the associated range selector chart.

#### .chartBodyG()
Retrieve the svg group for the chart body.

#### .x([xScale]) - **mandatory**
Get or set the x scale. The x scale can be any d3
[quantitive scale](https://github.com/mbostock/d3/wiki/Quantitative-Scales) or
[ordinal scale](https://github.com/mbostock/d3/wiki/Ordinal-Scales).
```js
// set x to a linear scale
chart.x(d3.scale.linear().domain([-2500, 2500]))
// set x to a time scale to generate histogram
chart.x(d3.time.scale().domain([new Date(1985, 0, 1), new Date(2012, 11, 31)]))
```

#### .xUnits([xUnits function])
Set or get the xUnits function. The coordinate grid chart uses the xUnits function to calculate
the number of data projections on x axis such as the number of bars for a bar chart or the
number of dots for a line chart. This function is expected to return a Javascript array of all
data points on x axis, or the number of points on the axis. [d3 time range functions
d3.time.days, d3.time.months, and
d3.time.years](https://github.com/mbostock/d3/wiki/Time-Intervals#aliases) are all valid xUnits
function. dc.js also provides a few units function, see the [Utilities](#utilities) section for
a list of built-in units functions. The default xUnits function is dc.units.integers.
```js
// set x units to count days
chart.xUnits(d3.time.days);
// set x units to count months
chart.xUnits(d3.time.months);
```
A custom xUnits function can be used as long as it follows the following interface:
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
Set or get the x axis used by a particular coordinate grid chart instance. This function is most
useful when x axis customization is required. The x axis in dc.js is an instance of a [d3
axis object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-axis); therefore it supports any
valid d3 axis manipulation. **Caution**: The x axis is usually generated internally by dc;
resetting it may cause unexpected results.
```js
// customize x axis tick format
chart.xAxis().tickFormat(function(v) {return v + '%';});
// customize x axis tick values
chart.xAxis().tickValues([0, 100, 200, 300]);
```

#### .elasticX([boolean])
Turn on/off elastic x axis behavior. If x axis elasticity is turned on, then the grid chart will
attempt to recalculate the x axis range whenever a redraw event is triggered.

#### .xAxisPadding([padding])
Set or get x axis padding for the elastic x axis. The padding will be added to both end of the x
axis if elasticX is turned on; otherwise it is ignored.

* padding can be an integer or percentage in string (e.g. '10%'). Padding can be applied to
number or date x axes.  When padding a date axis, an integer represents number of days being padded
and a percentage string will be treated the same as an integer.

#### .xUnitCount()
Returns the number of units displayed on the x axis using the unit measure configured by
.xUnits.

#### .useRightYAxis()
Gets or sets whether the chart should be drawn with a right axis instead of a left axis. When
used with a chart in a composite chart, allows both left and right Y axes to be shown on a
chart.

#### isOrdinal()
Returns true if the chart is using ordinal xUnits ([dc.units.ordinal](#dcunitsordinal)), or false
otherwise. Most charts behave differently with ordinal data and use the result of this method to
trigger the appropriate logic.

#### .xAxisLabel([labelText, [, padding]])
Set or get the x axis label. If setting the label, you may optionally include additional padding to
the margin to make room for the label. By default the padded is set to 12 to accomodate the text height.

#### .yAxisLabel([labelText, [, padding]])
Set or get the y axis label. If setting the label, you may optionally include additional padding
to the margin to make room for the label. By default the padded is set to 12 to accomodate the
text height.

#### .y([yScale])
Get or set the y scale. The y scale is typically automatically determined by the chart implementation.

#### .yAxis([yAxis])
Set or get the y axis used by the coordinate grid chart instance. This function is most useful
when y axis customization is required. The y axis in dc.js is simply an instance of a [d3 axis
object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-_axis); therefore it supports any
valid d3 axis manipulation. **Caution**: The y axis is usually generated internally by dc;
resetting it may cause unexpected results.
```js
// customize y axis tick format
chart.yAxis().tickFormat(function(v) {return v + '%';});
// customize y axis tick values
chart.yAxis().tickValues([0, 100, 200, 300]);
```

#### .elasticY([boolean])
Turn on/off elastic y axis behavior. If y axis elasticity is turned on, then the grid chart will
attempt to recalculate the y axis range whenever a redraw event is triggered.

#### .renderHorizontalGridLines([boolean])
Turn on/off horizontal grid lines.

#### .renderVerticalGridLines([boolean])
Turn on/off vertical grid lines.

#### .xAxisMin()
Calculates the minimum x value to display in the chart. Includes xAxisPadding if set.

#### .xAxisMax()
Calculates the maximum x value to display in the chart. Includes xAxisPadding if set.

#### .yAxisMin()
Calculates the minimum y value to display in the chart. Includes yAxisPadding if set.

#### .yAxisMax()
Calculates the maximum y value to display in the chart. Includes yAxisPadding if set.

#### .yAxisPadding([padding])
Set or get y axis padding for the elastic y axis. The padding will be added to the top of the y
axis if elasticY is turned on; otherwise it is ignored.

* padding can be an integer or percentage in string (e.g. '10%'). Padding can be applied to
number or date axes. When padding a date axis, an integer represents number of days being padded
and a percentage string will be treated the same as an integer.

#### .round([rounding function])
Set or get the rounding function used to quantize the selection when brushing is enabled.
```js
// set x unit round to by month, this will make sure range selection brush will
// select whole months
chart.round(d3.time.month.round);
```

#### .clipPadding([padding])
Get or set the padding in pixels for the clip path. Once set padding will be applied evenly to
the top, left, right, and bottom when the clip path is generated. If set to zero, the clip area
will be exactly the chart body area minus the margins.  Default: 5

#### .focus([range])
Zoom this chart to focus on the given range. The given range should be an array containing only
2 elements (`[start, end]`) defining a range in the x domain. If the range is not given or set
to null, then the zoom will be reset. _For focus to work elasticX has to be turned off;
otherwise focus will be ignored._
```js
chart.renderlet(function(chart){
    // smooth the rendering through event throttling
    dc.events.trigger(function(){
        // focus some other chart to the range selected by user on this chart
        someOtherChart.focus(chart.filter());
    });
})
```

#### .brushOn([boolean])
Turn on/off the brush-based range filter. When brushing is on then user can drag the mouse
across a chart with a quantitative scale to perform range filtering based on the extent of the
brush, or click on the bars of an ordinal bar chart or slices of a pie chart to filter and
unfilter them. However turning on the brush filter will disable other interactive elements on
the chart such as highlighting, tool tips, and reference lines. Zooming will still be possible
if enabled, but only via scrolling (panning will be disabled.) Default: true

## Stack Mixin
Stack Mixin is an mixin that provides cross-chart support of stackability using d3.layout.stack.

#### .stack(group[, name, accessor])
Stack a new crossfilter group onto this chart with an optional custom value accessor. All stacks
in the same chart will share the same key accessor and therefore the same set of keys.

For example, in a stacked bar chart, the bars of each stack will be positioned using the same set
of keys on the x axis, while stacked vertically. If name is specified then it will be used to
generate the legend label.
```js
// stack group using default accessor
chart.stack(valueSumGroup)
// stack group using custom accessor
.stack(avgByDayGroup, function(d){return d.value.avgByDay;});
```

#### .hidableStacks([boolean])
Allow named stacks to be hidden or shown by clicking on legend items.
This does not affect the behavior of hideStack or showStack.

#### .hideStack(name)
Hide all stacks on the chart with the given name.
The chart must be re-rendered for this change to appear.

#### .showStack(name)
Show all stacks on the chart with the given name.
The chart must be re-rendered for this change to appear.

#### .title([stackName], [titleFunction])
Set or get the title function. Chart class will use this function to render svg title (usually interpreted by
browser as tooltips) for each child element in the chart, i.e. a slice in a pie chart or a bubble in a bubble chart.
Almost every chart supports title function however in grid coordinate chart you need to turn off brush in order to
use title otherwise the brush layer will block tooltip trigger.

If the first argument is a stack name, the title function will get or set the title for that stack. If stackName
is not provided, the first stack is implied.
```js
// set a title function on 'first stack'
chart.title('first stack', function(d) { return d.key + ': ' + d.value; });
// get a title function from 'second stack'
var secondTitleFunction = chart.title('second stack');
);
```

#### .stackLayout([layout])
Gets or sets the stack layout algorithm, which computes a baseline for each stack and
propagates it to the next.  The default is
[d3.layout.stack](https://github.com/mbostock/d3/wiki/Stack-Layout#stack).

## Cap Mixin
Cap is a mixin that groups small data elements below a _cap_ into an *others* grouping for both the
Row and Pie Charts.

The top ordered elements in the group up to the cap amount will be kept in the chart, and the rest
will be replaced with an *others* element, with value equal to the sum of the replaced values. The
keys of the elements below the cap limit are recorded in order to filter by those keys when the
*others* element is clicked.

#### .cap([count])
Get or set the count of elements to that will be included in the cap.

#### .othersLabel([label])
Get or set the label for *Others* slice when slices cap is specified. Default label is **Others**.

#### .othersGrouper([grouperFunction])
Get or set the grouper function that will perform the insertion of data for the *Others* slice
if the slices cap is specified. If set to a falsy value, no others will be added. By default the
grouper function computes the sum of all values below the cap.
```js
chart.othersGrouper(function (data) {
    // compute the value for others, presumably the sum of all values below the cap
    var othersSum  = yourComputeOthersValueLogic(data)

    // the keys are needed to properly filter when the others element is clicked
    var othersKeys = yourComputeOthersKeysArrayLogic(data);

    // add the others row to the dataset
    data.push({'key': 'Others', 'value': othersSum, 'others': othersKeys });

    return data;
});
```

## Bubble Mixin
Includes: [Color Mixin](#color-mixin)

This Mixin provides reusable functionalities for any chart that needs to visualize data using bubbles.

#### .r([bubbleRadiusScale])
Get or set the bubble radius scale. By default the bubble chart uses
`d3.scale.linear().domain([0, 100])` as its r scale .

#### .radiusValueAccessor([radiusValueAccessor])
Get or set the radius value accessor function. If set, the radius value accessor function will
be used to retrieve a data value for each bubble. The data retrieved then will be mapped using
the r scale to the actual bubble radius. This allows you to encode a data dimension using bubble
size.

#### .minRadiusWithLabel([radius])
Get or set the minimum radius for label rendering. If a bubble's radius is less than this value
then no label will be rendered.  Default: 10

#### .maxBubbleRelativeSize([relativeSize])
Get or set the maximum relative size of a bubble to the length of x axis. This value is useful
when the difference in radius between bubbles is too great. Default: 0.3

## Pie Chart
Includes: [Cap Mixin](#cap-mixin), [Color Mixin](#color-mixin), [Base Mixin](#base-mixin)

The pie chart implementation is usually used to visualize a small categorical distribution.  The pie
chart uses keyAccessor to determine the slices, and valueAccessor to calculate the size of each
slice relative to the sum of all values. Slices are ordered by `.ordering` which defaults to sorting
by key.

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
#### dc.pieChart(parent[, chartGroup])
Create a pie chart instance and attaches it to the given parent element.

Parameters:

* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created pie chart instance

```js
// create a pie chart under #chart-container1 element using the default global chart group
var chart1 = dc.pieChart('#chart-container1');
// create a pie chart under #chart-container2 element using chart group A
var chart2 = dc.pieChart('#chart-container2', 'chartGroupA');
```

#### .slicesCap([cap])
Get or set the maximum number of slices the pie chart will generate. The top slices are determined by
value from high to low. Other slices exeeding the cap will be rolled up into one single *Others* slice.
The resulting data will still be sorted by .ordering (default by key).

#### .innerRadius([innerRadius])
Get or set the inner radius of the pie chart. If the inner radius is greater than 0px then the
pie chart will be rendered as a doughnut chart. Default inner radius is 0px.

#### .radius([radius])
Get or set the outer radius. If the radius is not set, it will be half of the minimum of the
chart width and height.

#### .cx([cx])
Get or set center x coordinate position. Default is center of svg.

#### .cy([cy])
Get or set center y coordinate position. Default is center of svg.

#### .minAngleForLabel([minAngle])
Get or set the minimal slice angle for label rendering. Any slice with a smaller angle will not
display a slice label.  Default min angle is 0.5.

## Bar Chart
Includes: [Stack Mixin](#stack Mixin), [Coordinate Grid Mixin](#coordinate-grid-mixin)

Concrete bar chart/histogram implementation.

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)
#### dc.barChart(parent[, chartGroup])
Create a bar chart instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection | compositeChart - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
If the bar chart is a sub-chart in a [Composite Chart](#composite-chart) then pass in the parent composite
chart instance.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created bar chart instance

```js
// create a bar chart under #chart-container1 element using the default global chart group
var chart1 = dc.barChart('#chart-container1');
// create a bar chart under #chart-container2 element using chart group A
var chart2 = dc.barChart('#chart-container2', 'chartGroupA');
// create a sub-chart under a composite parent chart
var chart3 = dc.barChart(compositeChart);
```

#### .centerBar(boolean)
Whether the bar chart will render each bar centered around the data position on x axis. Default: false

#### .barPadding([padding])
Get or set the spacing between bars as a fraction of bar size. Valid values are between 0-1.
Setting this value will also remove any previously set `gap`. See the
[d3 docs](https://github.com/mbostock/d3/wiki/Ordinal-Scales#wiki-ordinal_rangeBands)
for a visual description of how the padding is applied.

#### .outerPadding([padding])
Get or set the outer padding on an ordinal bar chart. This setting has no effect on non-ordinal charts.
Will pad the width by `padding * barWidth` on each side of the chart.

Default: 0.5

#### .gap(gapBetweenBars)
Manually set fixed gap (in px) between bars instead of relying on the default auto-generated
gap.  By default the bar chart implementation will calculate and set the gap automatically
based on the number of data points and the length of the x axis.

#### .alwaysUseRounding([boolean])
Set or get whether rounding is enabled when bars are centered.  Default: false.  If false, using
rounding with centered bars will result in a warning and rounding will be ignored.  This flag
has no effect if bars are not centered.

When using standard d3.js rounding methods, the brush often doesn't align correctly with
centered bars since the bars are offset.  The rounding function must add an offset to
compensate, such as in the following example.
```js
chart.round(function(n) {return Math.floor(n)+0.5});
```

## Line Chart
Includes [Stack Mixin](#stack-mixin), [Coordinate Grid Mixin](#coordinate-grid-mixin)

Concrete line/area chart implementation.

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)
#### dc.lineChart(parent[, chartGroup])
Create a line chart instance and attach it to the given parent element.

Parameters:

* parent : string | node | selection | compositeChart - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
If the line chart is a sub-chart in a [Composite Chart](#composite-chart) then pass in the parent composite
chart instance.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created line chart instance

```js
// create a line chart under #chart-container1 element using the default global chart group
var chart1 = dc.lineChart('#chart-container1');
// create a line chart under #chart-container2 element using chart group A
var chart2 = dc.lineChart('#chart-container2', 'chartGroupA');
// create a sub-chart under a composite parent chart
var chart3 = dc.lineChart(compositeChart);
```

#### .interpolate([value])
Gets or sets the interpolator to use for lines drawn, by string name, allowing e.g. step
functions, splines, and cubic interpolation.  This is passed to
[d3.svg.line.interpolate](https://github.com/mbostock/d3/wiki/SVG-Shapes#line_interpolate) and
[d3.svg.area.interpolate](https://github.com/mbostock/d3/wiki/SVG-Shapes#area_interpolate),
where you can find a complete list of valid arguments

#### .tension([value]) Gets or sets the tension to use for lines drawn, in the range 0 to 1.
This parameter further customizes the interpolation behavior.  It is passed to
[d3.svg.line.tension](https://github.com/mbostock/d3/wiki/SVG-Shapes#line_tension) and
[d3.svg.area.tension](https://github.com/mbostock/d3/wiki/SVG-Shapes#area_tension).  Default:
0.7

#### .defined([value])
Gets or sets a function that will determine discontinuities in the line which should be
skipped: the path will be broken into separate subpaths if some points are undefined.
This function is passed to
[d3.svg.line.defined](https://github.com/mbostock/d3/wiki/SVG-Shapes#line_defined)

Note: crossfilter will sometimes coerce nulls to 0, so you may need to carefully write
custom reduce functions to get this to work, depending on your data. See
https://github.com/dc-js/dc.js/issues/615#issuecomment-49089248

#### .dashStyle([array])
Set the line's d3 dashstyle. This value becomes the 'stroke-dasharray' of line. Defaults to empty
array (solid line).
 ```js
 // create a Dash Dot Dot Dot
 chart.dashStyle([3,1,1,1]);
 ```

#### .renderArea([boolean])
Get or set render area flag. If the flag is set to true then the chart will render the area
beneath each line and the line chart effectively becomes an area chart.

#### .dotRadius([dotRadius])
Get or set the radius (in px) for dots displayed on the data points. Default dot radius is 5.

#### .renderDataPoints([options])
Always show individual dots for each datapoint.

Options, if given, is an object that can contain the following:

* fillOpacity (default 0.8)
* strokeOpacity (default 0.8)
* radius (default 2)

If `options` is falsy, it disables data point rendering.

If no `options` are provided, the current `options` values are instead returned.

Example:
```
chart.renderDataPoints({radius: 2, fillOpacity: 0.8, strokeOpacity: 0.8})
```

## Data Count Widget
Includes: [Base Mixin](#base-mixin)

The data count widget is a simple widget designed to display the number of records selected by the
current filters out of the total number of records in the data set. Once created the data count widget
will automatically update the text content of the following elements under the parent element.

* '.total-count' - total number of records
* '.filter-count' - number of records matched by the current filters

Examples:

* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
#### dc.dataCount(parent[, chartGroup])
Create a data count widget and attach it to the given parent element.

Parameters:

* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
* chartGroup : string (optional) - name of the chart group this widget should be placed in.
The data count widget will only react to filter changes in the chart group.

Returns:
A newly created data count widget instance
#### .dimension(allData) - **mandatory**
For the data count widget the only valid dimension is the entire data set.
#### .group(groupAll) - **mandatory**
For the data count widget the only valid group is the group returned by `dimension.groupAll()`.

```js
var ndx = crossfilter(data);
var all = ndx.groupAll();

dc.dataCount('.dc-data-count')
   .dimension(ndx)
   .group(all);
```

#### html([object])
Gets or sets an optional object specifying HTML templates to use depending how many items are
selected. The text `%total-count` will replaced with the total number of records, and the text
`%filter-count` will be replaced with the number of selected records.
- all: HTML template to use if all items are selected
- some: HTML template to use if not all items are selected

```js
counter.html({
    some: '%filter-count out of %total-count records selected',
    all: 'All records selected. Click on charts to apply filters'
})
```

#### formatNumber([formatter])
Gets or sets an optional function to format the filter count and total count.

```js
counter.formatNumber(d3.format('.2g'))
```

## Data Table Widget
Includes: [Base Mixin](#base-mixin)

The data table is a simple widget designed to list crossfilter focused data set (rows being
filtered) in a good old tabular fashion.

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
#### dc.dataTable(parent[, chartGroup])
Create a data table widget instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created data table widget instance

#### .size([size])
Get or set the table size which determines the number of rows displayed by the widget.

#### .columns([columnFunctionArray])
Get or set column functions. The data table widget now supports several methods of specifying
the columns to display.  The original method, first shown below, uses an array of functions to
generate dynamic columns. Column functions are simple javascript functions with only one input
argument `d` which represents a row in the data set. The return value of these functions will be
used directly to generate table content for each cell. However, this method requires the .html
table entry to have a fixed set of column headers.

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

The next example shows you can simply list the data (d) content directly without
specifying it as a function, except where necessary (ie, computed columns).  Note
the data element accessor name is capitalized when displayed in the table. You can
also mix in functions as desired or necessary, but you must use the
    Object = [Label, Fn] method as shown below.
You may wish to override the following two functions, which are internally used to
translate the column information or function into a displayed header. The first one
is used on the simple "string" column specifier, the second is used to transform the
String(fn) into something displayable. For the Stock example, the function for Change
becomes a header of 'd.close - d.open'.
    _chart._doColumnHeaderCapitalize _chart._doColumnHeaderFnToString
You may use your own Object definition, however you must then override
    _chart._doColumnHeaderFormat , _chart._doColumnValueFormat
Be aware that fields without numberFormat specification will be displayed just as
they are stored in the data, unformatted.
```js
    chart.columns([
            "date",    // d["date"], ie, a field accessor; capitalized automatically
            "open",    // ...
            "close",   // ...
            ["Change", // Specify an Object = [Label, Fn]
                  function (d) {
                      return numberFormat(d.close - d.open);
                  }],
            "volume"   // d["volume"], ie, a field accessor; capitalized automatically
    ]);
```

A third example, where all fields are specified using the Object = [Label, Fn] method.

```js
    chart.columns([
        ["Date",   // Specify an Object = [Label, Fn]
         function (d) {
             return d.date;
         }],
        ["Open",
         function (d) {
             return numberFormat(d.open);
         }],
        ["Close",
         function (d) {
             return numberFormat(d.close);
         }],
        ["Change",
         function (d) {
             return numberFormat(d.close - d.open);
         }],
        ["Volume",
         function (d) {
             return d.volume;
         }]
    ]);
```

#### .sortBy([sortByFunction])
Get or set sort-by function. This function works as a value accessor at row level and returns a
particular field to be sorted by. Default value: identity function

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

## Data Grid Widget

Includes: [Base Mixin](#base-mixin)

Data grid is a simple widget designed to list the filtered records, providing
a simple way to define how the items are displayed.

Examples:
* [List of members of the european parliament](http://europarl.me/dc.js/web/ep/index.html)

#### dc.dataGrid(parent[, chartGroup])
Create a data grid widget instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created data grid widget instance

#### .size([size])
Get or set the grid size which determines the number of items displayed by the widget.

#### .html( function (data) { return '<html>'; })
Get or set the function that formats an item. The data grid widget uses a
function to generate dynamic html. Use your favourite templating engine or
generate the string directly.
```js
chart.html(function (d) { return '<div class='item '+data.exampleCategory+''>'+data.exampleString+'</div>';});
```

#### .htmlGroup( function (data) { return '<html>'; })
Get or set the function that formats a group label.
```js
chart.htmlGroup (function (d) { return '<h2>'.d.key . 'with ' . d.values.length .' items</h2>'});
```

#### .sortBy([sortByFunction])
Get or set sort-by function. This function works as a value accessor at the item
level and returns a particular field to be sorted.
by. Default: identity function

```js
chart.sortBy(function(d) {
    return d.date;
});
```

#### .order([order])
Get or set sort order function. Default value: ``` d3.ascending ```

```js
chart.order(d3.descending);
```

## Bubble Chart
Includes: [Bubble Mixin](#bubble-mixin), [Coordinate Grid Mixin](#coordinate-grid-mixin)

A concrete implementation of a general purpose bubble chart that allows data visualization using the
following dimensions:

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
* parent : string | node | selection | compositeChart - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created bubble chart instance

```js
// create a bubble chart under #chart-container1 element using the default global chart group
var bubbleChart1 = dc.bubbleChart('#chart-container1');
// create a bubble chart under #chart-container2 element using chart group A
var bubbleChart2 = dc.bubbleChart('#chart-container2', 'chartGroupA');
```

#### .elasticRadius([boolean])
Turn on or off the elastic bubble radius feature, or return the value of the flag. If this
feature is turned on, then bubble radii will be automatically rescaled to fit the chart better.

## Composite Chart
Includes: [Coordinate Grid Mixin](#coordinate-grid-mixin)

Composite charts are a special kind of chart that render multiple charts on the same Coordinate
Grid. You can overlay (compose) different bar/line/area charts in a single composite chart to
achieve some quite flexible charting effects.
#### dc.compositeChart(parent[, chartGroup])
Create a composite chart instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created composite chart instance

```js
// create a composite chart under #chart-container1 element using the default global chart group
var compositeChart1 = dc.compositeChart('#chart-container1');
// create a composite chart under #chart-container2 element using chart group A
var compositeChart2 = dc.compositeChart('#chart-container2', 'chartGroupA');
```

#### .useRightAxisGridLines(bool)
Get or set whether to draw gridlines from the right y axis.  Drawing from the left y axis is the
default behavior. This option is only respected when subcharts with both left and right y-axes
are present.

#### .childOptions({object})
Get or set chart-specific options for all child charts. This is equivalent to calling `.options`
on each child chart.

#### .rightYAxisLabel([labelText])
Set or get the right y axis label.

#### .compose(subChartArray)
Combine the given charts into one single composite coordinate grid chart.

```js
// compose the given charts in the array into one single composite chart
moveChart.compose([
    // when creating sub-chart you need to pass in the parent chart
    dc.lineChart(moveChart)
        .group(indexAvgByMonthGroup) // if group is missing then parent's group will be used
        .valueAccessor(function (d){return d.value.avg;})
        // most of the normal functions will continue to work in a composed chart
        .renderArea(true)
        .stack(monthlyMoveGroup, function (d){return d.value;})
        .title(function (d){
            var value = d.value.avg?d.value.avg:d.value;
            if(isNaN(value)) value = 0;
            return dateFormat(d.key) + '\n' + numberFormat(value);
        }),
    dc.barChart(moveChart)
        .group(volumeByMonthGroup)
        .centerBar(true)
]);
```

#### .children()
Returns the child charts which are composed into the composite chart.

#### .shareColors([boolean])
Get or set color sharing for the chart. If set, the `.colors()` value from this chart
will be shared with composed children. Additionally if the child chart implements
Stackable and has not set a custom .colorAccessor, then it will generate a color
specific to its order in the composition.

#### .shareTitle([[boolean])
Get or set title sharing for the chart. If set, the `.title()` value from this chart will be
shared with composed children. Default value is true.

#### .rightY([yScale])
Get or set the y scale for the right axis. The right y scale is typically automatically
generated by the chart implementation.

#### .rightYAxis([yAxis])
Set or get the right y axis used by the composite chart. This function is most useful when y
axis customization is required. The y axis in dc.js is an instance of a [d3 axis
object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-_axis) therefore it supports any valid
d3 axis manipulation. **Caution**: The y axis is usually generated internally by dc;
resetting it may cause unexpected results.
```jså
// customize y axis tick format
chart.rightYAxis().tickFormat(function (v) {return v + '%';});
// customize y axis tick values
chart.rightYAxis().tickValues([0, 100, 200, 300]);
```

## Series Chart

Includes: [Composite Chart](#composite chart)

A series chart is a chart that shows multiple series of data overlaid on one chart, where the
series is specified in the data. It is a specialization of Composite Chart and inherits all
composite features other than recomposing the chart.

#### dc.seriesChart(parent[, chartGroup])
Create a series chart instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created series chart instance

```js
// create a series chart under #chart-container1 element using the default global chart group
var seriesChart1 = dc.seriesChart("#chart-container1");
// create a series chart under #chart-container2 element using chart group A
var seriesChart2 = dc.seriesChart("#chart-container2", "chartGroupA");
```

#### .chart([function])
Get or set the chart function, which generates the child charts.  Default: dc.lineChart

```
// put interpolation on the line charts used for the series
chart.chart(function(c) { return dc.lineChart(c).interpolate('basis'); })
// do a scatter series chart
chart.chart(dc.scatterPlot)
```

#### .seriesAccessor([accessor])
Get or set accessor function for the displayed series. Given a datum, this function
should return the series that datum belongs to.

#### .seriesSort([sortFunction])
Get or set a function to sort the list of series by, given series values.

Example:
```
chart.seriesSort(d3.descending);
```

#### .valueSort([sortFunction])
Get or set a function to sort each series values by. By default this is the key accessor which,
for example, will ensure a lineChart series connects its points in increasing key/x order,
rather than haphazardly.

## Geo Choropleth Chart
Includes: [Color Mixin](#color-mixin), [Base Mixin](#base-mixin)

The geo choropleth chart is designed as an easy way to create a crossfilter driven choropleth map
from GeoJson data. This chart implementation was inspired by [the great d3 choropleth
example](http://bl.ocks.org/4060606).

Examples:
* [US Venture Capital Landscape 2011](http://dc-js.github.com/dc.js/vc/index.html)
#### dc.geoChoroplethChart(parent[, chartGroup])
Create a choropleth chart instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created choropleth chart instance

```js
// create a choropleth chart under '#us-chart' element using the default global chart group
var chart1 = dc.geoChoroplethChart('#us-chart');
// create a choropleth chart under '#us-chart2' element using chart group A
var chart2 = dc.compositeChart('#us-chart2', 'chartGroupA');
```

#### .overlayGeoJson(json, name, keyAccessor) - **mandatory**
Use this function to insert a new GeoJson map layer. This function can be invoked multiple times
if you have multiple GeoJson data layers to render on top of each other. If you overlay multiple
layers with the same name the new overlay will override the existing one.

Parameters:
* json - GeoJson feed
* name - name of the layer
* keyAccessor - accessor function used to extract 'key' from the GeoJson data. The key extracted by
this function should match the keys returned by the crossfilter groups.

```js
// insert a layer for rendering US states
chart.overlayGeoJson(statesJson.features, 'state', function(d) {
    return d.properties.name;
});
```

#### .projection(projection)
Set custom geo projection function. See the available [d3 geo projection
functions](https://github.com/mbostock/d3/wiki/Geo-Projections).  Default value: albersUsa.

#### .geoJsons()
Returns all GeoJson layers currently registered with this chart. The returned array is a
reference to this chart's internal data structure, so any modification to this array will also
modify this chart's internal registration.

Returns an array of objects containing fields {name, data, accessor}

#### .geoPath()
Returns the [d3.geo.path](https://github.com/mbostock/d3/wiki/Geo-Paths#path) object used to
render the projection and features.  Can be useful for figuring out the bounding box of the
feature set and thus a way to calculate scale and translation for the projection.

#### .removeGeoJson(name)
Remove a GeoJson layer from this chart by name

## Bubble Overlay Chart
Includes: [Bubble Mixin](#bubble-mixin), [Base Mixin](#base-mixin)

The bubble overlay chart is quite different from the typical bubble chart. With the bubble overlay
chart you can arbitrarily place bubbles on an existing svg or bitmap image, thus changing the
typical x and y positioning while retaining the capability to visualize data using bubble radius
and coloring.

Examples:
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)
#### dc.bubbleOverlay(parent[, chartGroup])
Create a bubble overlay chart instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
off-screen. Typically this element should also be the parent of the underlying image.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created bubble overlay chart instance

```js
// create a bubble overlay chart on top of the '#chart-container1 svg' element using the default global chart group
var bubbleChart1 = dc.bubbleOverlayChart('#chart-container1').svg(d3.select('#chart-container1 svg'));
// create a bubble overlay chart on top of the '#chart-container2 svg' element using chart group A
var bubbleChart2 = dc.compositeChart('#chart-container2', 'chartGroupA').svg(d3.select('#chart-container2 svg'));
```
#### .svg(imageElement) - **mandatory**
Set the underlying svg image element. Unlike other dc charts this chart will not generate a svg
element; therefore the bubble overlay chart will not work if this function is not invoked. If the
underlying image is a bitmap, then an empty svg will need to be created on top of the image.

```js
// set up underlying svg element
chart.svg(d3.select('#chart svg'));
```

#### .point(name, x, y) - **mandatory**
Set up a data point on the overlay. The name of a data point should match a specific 'key' among
data groups generated using keyAccessor.  If a match is found (point name <-> data group key)
then a bubble will be generated at the position specified by the function. x and y
value specified here are relative to the underlying svg.

## Row Chart
Includes: [Cap Mixin](#cap-mixin), [Margin Mixin](#margin-mixin), [Color Mixin](#color-mixin), [Base Mixin](#base-mixin)

Concrete row chart implementation.
#### dc.rowChart(parent[, chartGroup])
Create a row chart instance and attach it to the given parent element.

Parameters:

* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created row chart instance

```js
// create a row chart under #chart-container1 element using the default global chart group
var chart1 = dc.rowChart('#chart-container1');
// create a row chart under #chart-container2 element using chart group A
var chart2 = dc.rowChart('#chart-container2', 'chartGroupA');
```

#### .x([scale])
Gets or sets the x scale. The x scale can be any d3
[quantitive scale](https://github.com/mbostock/d3/wiki/Quantitative-Scales)

#### .renderTitleLabel(boolean)
Turn on/off Title label rendering (values) using SVG style of text-anchor 'end'

#### .xAxis()
Get the x axis for the row chart instance.  Note: not settable for row charts.
See the [d3 axis object](https://github.com/mbostock/d3/wiki/SVG-Axes#wiki-axis) documention for more information.
```js
// customize x axis tick format
chart.xAxis().tickFormat(function (v) {return v + '%';});
// customize x axis tick values
chart.xAxis().tickValues([0, 100, 200, 300]);
```

#### .fixedBarHeight([height])
Get or set the fixed bar height. Default is [false] which will auto-scale bars.
For example, if you want to fix the height for a specific number of bars (useful in TopN charts)
you could fix height as follows (where count = total number of bars in your TopN and gap is
your vertical gap space).
```js
 chart.fixedBarHeight( chartheight - (count + 1) * gap / count);
```

#### .gap([gap])
Get or set the vertical gap space between rows on a particular row chart instance. Default gap is 5px;

#### .elasticX([boolean])
Get or set the elasticity on x axis. If this attribute is set to true, then the x axis will rescle to auto-fit the
data range when filtered.

#### .labelOffsetX([x])
Get or set the x offset (horizontal space to the top left corner of a row) for labels on a particular row chart.
Default x offset is 10px;

#### .labelOffsetY([y])
Get or set the y offset (vertical space to the top left corner of a row) for labels on a particular row chart.
Default y offset is 15px;

#### .titleLabelOffsetx([x])
Get of set the x offset (horizontal space between right edge of row and right edge or text.
Default x offset is 2px;

## Legend
Legend is a attachable widget that can be added to other dc charts to render horizontal legend
labels.

```js
chart.legend(dc.legend().x(400).y(10).itemHeight(13).gap(5))
```

Examples:
* [Nasdaq 100 Index](http://dc-js.github.com/dc.js/)
* [Canadian City Crime Stats](http://dc-js.github.com/dc.js/crime/index.html)

#### .x([value])
Set or get x coordinate for legend widget. Default: 0.

#### .y([value])
Set or get y coordinate for legend widget. Default: 0.

#### .gap([value])
Set or get gap between legend items. Default: 5.

#### .itemHeight([value])
Set or get legend item height. Default: 12.

#### .horizontal([boolean])
Position legend horizontally instead of vertically

#### .legendWidth([value])
Maximum width for horizontal legend. Default: 560.

#### .itemWidth([value])
legendItem width for horizontal legend. Default: 70.

#### .autoItemWidth([value])
Turn automatic width for legend items on or off. If true, itemWidth() is ignored.
This setting takes into account gap(). Default: false.

## Scatter Plot
Includes: [Coordinate Grid Mixin](#coordinate-grid-mixin)

A scatter plot chart
#### dc.scatterPlot(parent[, chartGroup])
Create a scatter plot instance and attach it to the given parent element.

Parameters:

* parent : string | node | selection | compositeChart - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
If the scatter plot is a sub-chart in a [Composite Chart](#composite-chart) then pass in the parent composite
chart instance.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created scatter plot instance

```js
// create a scatter plot under #chart-container1 element using the default global chart group
var chart1 = dc.scatterPlot('#chart-container1');
// create a scatter plot under #chart-container2 element using chart group A
var chart2 = dc.scatterPlot('#chart-container2', 'chartGroupA');
// create a sub-chart under a composite parent chart
var chart3 = dc.scatterPlot(compositeChart);
```

#### .existenceAccessor([accessor])
Get or set the existence accessor.  If a point exists, it is drawn with symbolSize radius and
opacity 1; if it does not exist, it is drawn with hiddenSize radius and opacity 0. By default,
the existence accessor checks if the reduced value is truthy.

#### .symbol([type])
Get or set the symbol type used for each point. By default the symbol is a circle. See the D3
[docs](https://github.com/mbostock/d3/wiki/SVG-Shapes#wiki-symbol_type) for acceptable types.
Type can be a constant or an accessor.

#### .symbolSize([radius])
Set or get radius for symbols. Default: 3.

#### .highlightedSize([radius])
Set or get radius for highlighted symbols. Default: 4.

#### .hiddenSize([radius])
Set or get radius for symbols when the group is empty. Default: 0.

## Number Display Widget
Includes: [Base Mixin](#base-mixin)

A display of a single numeric value.

Examples:

* [Test Example](http://dc-js.github.io/dc.js/examples/number.html)
#### dc.numberDisplay(parent[, chartGroup])
Create a Number Display instance and attach it to the given parent element.

Unlike other charts, you do not need to set a dimension. Instead a group object must be provided and
a valueAccessor that returns a single value.

Parameters:

* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
The number display widget will only react to filter changes in the chart group.

Returns:
A newly created number display instance

```js
// create a number display under #chart-container1 element using the default global chart group
var display1 = dc.numberDisplay('#chart-container1');
```

#### .html([object])
 Gets or sets an optional object specifying HTML templates to use depending on the number
 displayed.  The text `%number` will be replaced with the current value.
 - one: HTML template to use if the number is 1
 - zero: HTML template to use if the number is 0
 - some: HTML template to use otherwise

 ```js
 numberWidget.html({
     one:'%number record',
     some:'%number records',
     none:'no records'})
 ```

#### .value()
Calculate and return the underlying value of the display

#### .formatNumber([formatter])
Get or set a function to format the value for the display. By default `d3.format('.2s');` is used.

## Heat Map

Includes: [Color Mixin](#color-mixin), [Margin Mixin](#margin-mixin), [Base Mixin](#base-mixin)

A heat map is matrix that represents the values of two dimensions of data using colors.

#### dc.heatMap(parent[, chartGroup])
Create a heat map instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) specifying
a dom block element such as a div; or a dom element or d3 selection.

* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created heat map instance

```js
// create a heat map under #chart-container1 element using the default global chart group
var heatMap1 = dc.heatMap('#chart-container1');
// create a heat map under #chart-container2 element using chart group A
var heatMap2 = dc.heatMap('#chart-container2', 'chartGroupA');
```

#### .rows([values])
Gets or sets the values used to create the rows of the heatmap, as an array. By default, all
the values will be fetched from the data using the value accessor, and they will be sorted in
ascending order.

#### .cols([keys])
Gets or sets the keys used to create the columns of the heatmap, as an array. By default, all
the values will be fetched from the data using the key accessor, and they will be sorted in
ascending order.

#### .boxOnClick([handler])
Gets or sets the handler that fires when an individual cell is clicked in the heatmap.
By default, filtering of the cell will be toggled.

#### .xAxisOnClick([handler])
Gets or sets the handler that fires when a column tick is clicked in the x axis.
By default, if any cells in the column are unselected, the whole column will be selected,
otherwise the whole column will be unselected.

#### .yAxisOnClick([handler])
Gets or sets the handler that fires when a row tick is clicked in the y axis.
By default, if any cells in the row are unselected, the whole row will be selected,
otherwise the whole row will be unselected.

## Box Plot

Includes: [Coordinate Grid Mixin](#coordinate-grid-mixin)

A box plot is a chart that depicts numerical data via their quartile ranges.

#### dc.boxPlot(parent[, chartGroup])
Create a box plot instance and attach it to the given parent element.

Parameters:
* parent : string | node | selection - any valid
[d3 single selector](https://github.com/mbostock/d3/wiki/Selections#selecting-elements) representing
a dom block element such as a div; or a dom element or d3 selection.
* chartGroup : string (optional) - name of the chart group this chart instance should be placed in.
Interaction with a chart will only trigger events and redraws within the chart's group.

Returns:
A newly created box plot instance

```js
// create a box plot under #chart-container1 element using the default global chart group
var boxPlot1 = dc.boxPlot('#chart-container1');
// create a box plot under #chart-container2 element using chart group A
var boxPlot2 = dc.boxPlot('#chart-container2', 'chartGroupA');
```

#### .boxPadding([padding])
Get or set the spacing between boxes as a fraction of box size. Valid values are within 0-1.
See the [d3 docs](https://github.com/mbostock/d3/wiki/Ordinal-Scales#wiki-ordinal_rangeBands)
for a visual description of how the padding is applied.

Default: 0.8

#### .outerPadding([padding])
Get or set the outer padding on an ordinal box chart. This setting has no effect on non-ordinal charts
or on charts with a custom `.boxWidth`. Will pad the width by `padding * barWidth` on each side of the chart.

Default: 0.5

#### .boxWidth(width || function(innerChartWidth, xUnits) { ... })
Get or set the numerical width of the boxplot box. The width may also be a function taking as
parameters the chart width excluding the right and left margins, as well as the number of x
units.

#### .tickFormat()
Set the numerical format of the boxplot median, whiskers and quartile labels. Defaults to
integer formatting.
```js
// format ticks to 2 decimal places
chart.tickFormat(d3.format('.2f'));
```