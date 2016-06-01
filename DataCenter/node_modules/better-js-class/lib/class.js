
module.exports = function() {
    var Class = function () {
        var extend = function (subclass, superclass, overrides) {
            var magic = function(fn) {
                return function() {
                    var tmp = this.parent;
                    this.parent = superclass.prototype;
                    var res = fn.apply(this, arguments);
                    this.parent = tmp;
                    return res;
                };
            };

            var k,
                TempClass = function () {};

            TempClass.prototype = superclass.prototype;
            subclass.prototype = new TempClass();

            for (k in overrides) {
                subclass.prototype[k] = magic(overrides[k]);
            }

            return superclass.prototype;
        };

        var Class = function () {
            var superclass, methods;

            if (arguments.length === 1) {
                methods = arguments[0];
            } else {
                superclass = arguments[0];
                methods = arguments[1];
            }

            var cls = function () {
                this._init.apply(this, arguments);
            }

            if (superclass) {
                extend(cls, superclass, methods);
            } else {
                if (methods._init == null) {
                    methods._init = function() {};
                }
                cls.prototype = methods;
            }

            return cls;
        };

        return Class;
    }();

    return Class;
}();
