
var Tail = function() {
    this._q = [];
    this._running = false;
};

Tail.prototype = {
    run: function(fn) {
        this._q.push(fn);
        if (!this._running) {
            this._run();
        }
    },

    _run: function() {
        while(true) {
            var fn = this._q.shift();
            if (fn) {
                this._running = true;
                fn();
            } else {
                this._running = false;
                break;
            }
        }
    }
};

module.exports = new Tail();
    
