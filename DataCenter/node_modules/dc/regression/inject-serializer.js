(function () {
    dc.disableTransitions = true;
    window.onload = function () {
        alert(JSON.stringify(['rendered', d3.select('html').node().innerHTML]));
    };
})();
