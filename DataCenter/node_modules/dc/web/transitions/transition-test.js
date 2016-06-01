var transitionTest = (function() {

    // http://stackoverflow.com/questions/901115/how-can-i-get-query-string-values-in-javascript
    var querystring = (function(a) {
        if (a == "") return {};
        var b = {};
        for (var i = 0; i < a.length; ++i)
        {
            var p=a[i].split('=', 2);
            if (p.length == 1)
                b[p[0]] = "";
            else
                b[p[0]] = decodeURIComponent(p[1].replace(/\+/g, " "));
        }
        return b;
    })(window.location.search.substr(1).split('&'));

    var inter, duration = +querystring.duration, pause = +querystring.pause;
    if(isNaN(duration)) duration = 3000;
    if(isNaN(pause)) pause = 500;
    function stop() {
        window.clearInterval(inter);
    }
    function oscillate(f1, f2) {
        return function() {
            stop();
            var which = false;
            f1();
            dc.redrawAll();
            inter = window.setInterval(function() {
                if((which = !which))
                    f2();
                else
                    f1();
                dc.redrawAll();
            }, duration+pause);
        };
    }
    return {
        duration: duration,
        pause: pause,
        stop: stop,
        oscillate: oscillate
    };
})();
