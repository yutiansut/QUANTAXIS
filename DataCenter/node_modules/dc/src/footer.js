// Renamed functions

dc.abstractBubbleChart = dc.bubbleMixin;
dc.baseChart = dc.baseMixin;
dc.capped = dc.capMixin;
dc.colorChart = dc.colorMixin;
dc.coordinateGridChart = dc.coordinateGridMixin;
dc.marginable = dc.marginMixin;
dc.stackableChart = dc.stackMixin;

// Expose d3 and crossfilter, so that clients in browserify
// case can obtain them if they need them.
dc.d3 = d3;
dc.crossfilter = crossfilter;

return dc;}
    if(typeof define === "function" && define.amd) {
        define(["d3", "crossfilter"], _dc);
    } else if(typeof module === "object" && module.exports) {
        var _d3 = require('d3');
        var _crossfilter = require('crossfilter');
        // When using npm + browserify, 'crossfilter' is a function,
        // since package.json specifies index.js as main function, and it
        // does special handling. When using bower + browserify,
        // there's no main in bower.json (in fact, there's no bower.json),
        // so we need to fix it.
        if (typeof _crossfilter !== "function") {
            _crossfilter = _crossfilter.crossfilter;
        }
        module.exports = _dc(_d3, _crossfilter);
    } else {
        this.dc = _dc(d3, crossfilter);
    }
}
)();
