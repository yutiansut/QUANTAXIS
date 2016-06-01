# 2.0 Series
## 2.0.0 beta 27
* Improvements to HTML documentation, by Matt Traynham ([1096](https://github.com/dc-js/dc.js/issues/1096) / [1097](https://github.com/dc-js/dc.js/issues/1097) / [1099](https://github.com/dc-js/dc.js/issues/1099) / [1100](https://github.com/dc-js/dc.js/issues/1100) / [1101](https://github.com/dc-js/dc.js/pull/1101))
* Ability to set color and opacity of non-brushed ("excluded") points in scatterplot; also separate brushing from highlighting, which seems like a different thing. ([938](https://github.com/dc-js/dc.js/issues/938))

## 2.0.0 beta 26
* Apply pie chart labels before transition, so they are easier to manipulate with the pretransition hook. Added example of showing percentages in pie chart labels. (Workaround for [#703](https://github.com/dc-js/dc.js/issues/703))
* Documentation of chart registry, by Jasmine Hegman ([#676](https://github.com/dc-js/dc.js/issues/676) / [#1082](https://github.com/dc-js/dc.js/pull/1082))
* HTML documentation generation, by Matt Traynham. There are still some kinks to be worked out here, but in principle it should be more robust than the gigantic markdown file we are generating. ([#1086](https://github.com/dc-js/dc.js/pull/1086))
* Document that you need to use a `RangedFilter` when filtering a range, by koefoed ([#1090](https://github.com/dc-js/dc.js/pull/1090))
* Fix links to box plot examples, by Yuval Greenfield ([#1094](https://github.com/dc-js/dc.js/pull/1094))
* [Sparkline example](http://dc-js.github.io/dc.js/examples/sparkline.html) ([#1013](https://github.com/dc-js/dc.js/issues/1013))
* Example of [complex reductions](http://dc-js.github.io/dc.js/examples/complex-reduce.html) that need all the rows in each group, like min, max, median.
* [Time interval](http://dc-js.github.io/dc.js/examples/time-intervals.html) example.

## 2.0.0 beta 25
* Improved dataTable docs (including a fix for [#1030](https://github.com/dc-js/dc.js/issues/1030))
* Generate proper data table header ([#1015](https://github.com/dc-js/dc.js/issues/1015))
* Fix various test failures on Safari/IE/Edge (regular testing is on Chrome/Firefox/Opera) ([#1072](https://github.com/dc-js/dc.js/issues/1072), [#1073](https://github.com/dc-js/dc.js/issues/1073), [#1074](https://github.com/dc-js/dc.js/issues/1064))

## 2.0.0 beta 24
* Only auto-calculate width/height once each render - sizes were getting calculated wrong ([#1070](https://github.com/dc-js/dc.js/issues/1070)) and charts were changing size on redraw if they didn't have a fixed size in the chart spec or in the div style ([#980](https://github.com/dc-js/dc.js/issues/980))
* Tell browserify the correct entry point `browser: dc.js`, so it won't try to bundle jsdom, by Sam Dunster ([#1005](https://github.com/dc-js/dc.js/issues/1005) / ([#1062](https://github.com/dc-js/dc.js/pull/1062))
* Lighten the vertical lines in row chart (consistent with other charts), by Mike Vashevko ([#1046](https://github.com/dc-js/dc.js/issues/1046) / ([#1047](https://github.com/dc-js/dc.js/pull/1047))
* dc.utils docs, by Matt Traynham ([#961](https://github.com/dc-js/dc.js/issues/961) / ([#1041](https://github.com/dc-js/dc.js/pull/1041))

## 2.0.0 beta 23
* Domain was getting set for composite charts even when `elasticY` disabled. ([#1056](https://github.com/dc-js/dc.js/issues/1056)

## 2.0.0 beta 22
(no changes; bump due to botched npm publish)

## 2.0.0 beta 21
* Ability to use non-crossfilter backend with asynchronous connection (callback), via `commitHandler`.
* Domain comparison was failing for undefined/null domain values.
* Option `controlsUseVisibility` to use `visibility` attribute instead of `display` for `filter` and `reset` controls, to reduce disruption to the layout. Was originally on 2.1 branch with default true, now on 2.0 branch with default false. ([#888](https://github.com/dc-js/dc.js/issues/888), [#1016](https://github.com/dc-js/dc.js/issues/1016))
* Option to add labels above bars in bar chart (e.g. to show the value), by N Reese ([#211](https://github.com/dc-js/dc.js/issues/211) / [#1031](https://github.com/dc-js/dc.js/pull/1031))
* Option to sort bubbles with smaller bubbles in front; make bubble labels not clickable because they can get in the way, by Matt Traynham ([#1025](https://github.com/dc-js/dc.js/pull/1025))

## 2.0.0 beta 20
* Slicing functionality for basic data table paging, based on Chris Alvino's feature for the data grid ([#101](https://github.com/dc-js/dc.js/issues/101))
* Ability to customize the legend text, by Chris Alvino ([#982](https://github.com/dc-js/dc.js/pull/982))
* Option to align the left and right Y axes if either or both has negative values, by Mohomed Gazal ([#985](https://github.com/dc-js/dc.js/pull/985))
* Connector lines from pie wedges to external labels, by Alan Kavanagh ([#986](https://github.com/dc-js/dc.js/pull/986))
* Further documentation improvements, including lots more cross-linking, by Matt Traynham ([#1012](https://github.com/dc-js/dc.js/pull/1012))
* Minified CSS, by Indri Muska ([#1023](https://github.com/dc-js/dc.js/pull/1023))

## 2.0.0 beta 19
* Allow d3.selection to be passed as parent, as documented ([#1006](https://github.com/dc-js/dc.js/issues/1006))
* Properly derive dc.errors from Error prototype to get stack
* Add BadArgumentException and make .anchor() parent argument mandatory
* Enable crossfilter optimizations by not resetting the filter and by using filterExact and filterRange, by Ethan Jewett ([#990](https://github.com/dc-js/dc.js/pull/990) / [#989](https://github.com/dc-js/dc.js/issues/989) / [#478](https://github.com/dc-js/dc.js/issues/478))
* Add `filterType` to dc.filters, for filter optimizations and [easier serialization](https://github.com/dc-js/dc.js/issues/819)
* More documentation improvements, by Matt Traynham ([#999](https://github.com/dc-js/dc.js/pull/999))
* Fix method name in documentation ([#1009](https://github.com/dc-js/dc.js/issues/1009))
* Move x axis when row chart size changes, by Wang Xuan ([#1001](https://github.com/dc-js/dc.js/pull/1001)
* Fix css rule that was improperly selecting all axes, not just dc.js ones ([#1011](https://github.com/dc-js/dc.js/pull/1011) / ([#1005](https://github.com/dc-js/dc.js/issues/1007))
* Add pre-commit hook to hopefully avoid ever checking in merge artifacts again.

## 2.0.0 beta 18
* Fixes resizing examples to use `rescale` - currently all coordinate grid charts need to call this when changing width/height, in order to get axes moved ([#974](https://github.com/dc-js/dc.js/issues/974))
* Update all dependencies, continued linting, by Matt Traynham ([#975](https://github.com/dc-js/dc.js/pull/975))
* Bubble mixin minimum radius accessor ([#687](https://github.com/dc-js/dc.js/issues/687))
* Example of single selection of ordinal bar chart (for [#996](https://github.com/dc-js/dc.js/issues/996))
* Move documentation to JSDoc toolchain, by Matt Traynham ([#978](https://github.com/dc-js/dc.js/pull/978) / [#994](https://github.com/dc-js/dc.js/pull/994))
* Resize heat map axes when chart size changes, by Wang Xuan ([#995](https://github.com/dc-js/dc.js/pull/995)

## 2.0.0 beta 17
* Fixes issue where transitions were applied to the brush as it's being applied, causing it to lag ([#973](https://github.com/dc-js/dc.js/issues/973))

## 2.0.0 beta 16
* Reposition brush when coordinate grid chart size changes ([#972](https://github.com/dc-js/dc.js/pull/972))
* Ability to slice the data grid, by Chris Alvino ([#946](https://github.com/dc-js/dc.js/pull/946)). Also a much-needed warning that data table and data grid `.group()` means something completely different.
* Ability not to apply grouping to data table, by Emiliano Guevara ([#863](https://github.com/dc-js/dc.js/pull/863))

## 2.0.0 beta 15
* Reposition X axis on chart resize, by Rob Hardwick ([#856](https://github.com/dc-js/dc.js/pull/856)). Y axis as well
* More fixes for resizing charts, and [a new resizing examples directory](http://dc-js.github.io/dc.js/resizing/), mostly for testing.

## 2.0.0 beta 14
* Fix a test for IE and add svg subpath matcher, for #894

## 2.0.0 beta 13
* Pie chart radius padding, by Matt Traynham ([#894](https://github.com/dc-js/dc.js/pull/894))
* Example of a table showing group-aggregated data, by Ion Alberdi ([#929](https://github.com/dc-js/dc.js/pull/929))
* Filtered items were not displayed after render in coordinate grid charts, by Matt Traynham ([#900](https://github.com/dc-js/dc.js/pull/900))
* grammar/spelling/formatting fixes to annotated stock example, by Johnny Peck and Enrico Spinielli ([#956](https://github.com/dc-js/dc.js/pull/956), [#875](https://github.com/dc-js/dc.js/pull/875))
* document bower install, by Mayfarth ([#899](https://github.com/dc-js/dc.js/pull/899))
* remove unused bower version, by Kevin Kirsche ([#948](https://github.com/dc-js/dc.js/pull/948))
* Front page stable version automatically read from GitHub, by Enrico Spinielli ([#865](https://github.com/dc-js/dc.js/pull/865))

## 2.0.0 beta 12
 * axes should rescale on chart rescale (not just on zoom). ([#791](https://github.com/dc-js/dc.js/issues/791))
 * always rescale x axis on render, and detect domain change more thoroughly, by Matt Traynham
 ([#896](https://github.com/dc-js/dc.js/pull/896))

## 2.0.0 beta 11
 * pretransition event ([#806](https://github.com/dc-js/dc.js/issues/806))
 * replace `.renderlet(...)` with `.on("renderlet", ...)` in test and examples, by Alan Kavanagh ([#906](https://github.com/dc-js/dc.js/issues/906) / ([#917](https://github.com/dc-js/dc.js/pull/917))

## 2.0.0 beta 10
 * component package manager support, by Shobhit Gupta ([#860](https://github.com/dc-js/dc.js/pull/860))
 * add sourcemaps (*.map) to distributions ([#866](https://github.com/dc-js/dc.js/issues/866))
 * allow `.options()` to take an array of arguments (for better angular-dc support), by Tim Ruhle ([#886](https://github.com/dc-js/dc.js/pull/886) / ([#769](https://github.com/dc-js/dc.js/issues/769))
 * make bower distro smaller, by Matt Traynham and Tim Ruhle ([#925](https://github.com/dc-js/dc.js/pull/925 / [#935](https://github.com/dc-js/dc.js/pull/935))
 * added infrastructure for testing transitions by eye
 * added area and stacked bar examples ([#777](https://github.com/dc-js/dc.js/issues/#777))

## 2.0.0 beta 9
 * propagate elasticX to child charts so that domain can be calculated correctly ([#926](https://github.com/dc-js/dc.js/issues/926))

## 2.0.0 beta 8
 * simplify Gruntfile and further update dependencies, by Matt Traynham ([#849](https://github.com/dc-js/dc.js/pull/849))
 * setting the chart group should automatically put the chart in that group, by Matt Traynham ([#834](https://github.com/dc-js/dc.js/pull/834) / [#775](https://github.com/dc-js/dc.js/issues/775))

## 2.0.0 beta 7
 * fixes a bug introduced in the last release where the ordering function was defined inconsistently, causing the default ordering function to be incorrect and causing crashes with largish data in crossfilter's quicksort on IE. ([#909](https://github.com/dc-js/dc.js/issues/909))

## 2.0.0 beta 6
 * pie chart consistently pass data object to pie title function, by Jasmine Hegman ([#824](https://github.com/dc-js/dc.js/pull/824) / [#755](https://github.com/dc-js/dc.js/issues/755))
 * heatmap box titles were not updated on redraw, by hhravn ([#798](https://github.com/dc-js/dc.js/pull/798))
 * apply ordering to ordinal bar chart, by Mihai Hodorogea ([#766](https://github.com/dc-js/dc.js/pull/766) / [#772](https://github.com/dc-js/dc.js/issues/772))
 * add option to hide mouseover dots for line chart, by Davis Ford ([#735](https://github.com/dc-js/dc.js/pull/735))
 * adding example bar-extra-line, overlaying a line with a renderlet

## 2.0.0 beta 5
 * updating this doc to link to issues/PRs manually (until we get a better changelog
   system?), by Matt Traynham ([#845](https://github.com/dc-js/dc.js/issues/845))
 * update all NPM dependencies and fix tests that were not expecting any results,
   by Matt Traynham ([#844](https://github.com/dc-js/dc.js/issues/844))

## 2.0.0 beta 4
 * make barChart.onClick a proper override, by Gordon Woodhull (fixes the complaint in [#168](https://github.com/dc-js/dc.js/issues/168))

## 2.0.0 beta 3
 * Properly tagged this time.

## 2.0.0 beta 2
 * Re-implement renderlets as regular event `.on('renderlet')`. old function `.renderlet()`
   is deprecated, by Matt Traynham ([#776](https://github.com/dc-js/dc.js/issues/776) / [#833](https://github.com/dc-js/dc.js/issues/833), replaces [#779](https://github.com/dc-js/dc.js/issues/779))
 * Geochoropleth tests sped up, by Jasmine Hegman ([#825](https://github.com/dc-js/dc.js/issues/825) / [#817](https://github.com/dc-js/dc.js/issues/817))
 * Number display test cleaned up, by Jasmine Hegman ([#826](https://github.com/dc-js/dc.js/issues/826)/ [#783](https://github.com/dc-js/dc.js/issues/783))
 * Provide a way to override the heatmap labels, by hhravn ([#794](https://github.com/dc-js/dc.js/issues/794) / [#793](https://github.com/dc-js/dc.js/issues/793))

## add-logo tag
 * Added logo to main page and favicon ([#618](https://github.com/dc-js/dc.js/issues/618))

## 2.0.0 beta 1
 * Merged [#800](https://github.com/dc-js/dc.js/issues/800): unselectable ids starting with numbers [#789](https://github.com/dc-js/dc.js/issues/789). Thanks Jasmine Hegman!
 * Interface and features frozen - from this point all fixes will be merged to
   `master` and `develop`, and all interface changes only merged to `develop`.

## Starting dc.js Changelog
 * Here we start using git-flow, start a changelog, and start 2015.  Under git-flow,
   the latest release (starting with 2.0.0-beta.1) is always on the master branch,
   development (2.1.0-dev) is on the develop branch, and releases and fixes are always
   merged into develop.
 * Read about git-flow here: http://jeffkreeftmeijer.com/2010/why-arent-you-using-git-flow/
 * It follows that this document will always have two active sections: the master
   section, and the develop section.  Since any changes merged to master are also
   merged to develop, any changes added to the changelog for the master branch will
   get merged into the same section in the develop version of this document.
