/**
 * Margin is a mixin that provides margin utility functions for both the Row Chart and Coordinate Grid
 * Charts.
 * @name marginMixin
 * @memberof dc
 * @mixin
 * @param {Object} _chart
 * @return {dc.marginMixin}
 */
dc.marginMixin = function (_chart) {
    var _margin = {top: 10, right: 50, bottom: 30, left: 30};

    /**
     * Get or set the margins for a particular coordinate grid chart instance. The margins is stored as
     * an associative Javascript array.
     * @method margins
     * @memberof dc.marginMixin
     * @instance
     * @example
     * var leftMargin = chart.margins().left; // 30 by default
     * chart.margins().left = 50;
     * leftMargin = chart.margins().left; // now 50
     * @param {{top: Number, right: Number, left: Number, bottom: Number}} [margins={top: 10, right: 50, bottom: 30, left: 30}]
     * @return {{top: Number, right: Number, left: Number, bottom: Number}}
     * @return {dc.marginMixin}
     */
    _chart.margins = function (margins) {
        if (!arguments.length) {
            return _margin;
        }
        _margin = margins;
        return _chart;
    };

    _chart.effectiveWidth = function () {
        return _chart.width() - _chart.margins().left - _chart.margins().right;
    };

    _chart.effectiveHeight = function () {
        return _chart.height() - _chart.margins().top - _chart.margins().bottom;
    };

    return _chart;
};
