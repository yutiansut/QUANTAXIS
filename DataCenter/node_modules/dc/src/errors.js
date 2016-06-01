dc.errors = {};

dc.errors.Exception = function (msg) {
    var _msg = msg || 'Unexpected internal error';

    this.message = _msg;

    this.toString = function () {
        return _msg;
    };
    this.stack = (new Error()).stack;
};
dc.errors.Exception.prototype = Object.create(Error.prototype);
dc.errors.Exception.prototype.constructor = dc.errors.Exception;

dc.errors.InvalidStateException = function () {
    dc.errors.Exception.apply(this, arguments);
};

dc.errors.InvalidStateException.prototype = Object.create(dc.errors.Exception.prototype);
dc.errors.InvalidStateException.prototype.constructor = dc.errors.InvalidStateException;

dc.errors.BadArgumentException = function () {
    dc.errors.Exception.apply(this, arguments);
};

dc.errors.BadArgumentException.prototype = Object.create(dc.errors.Exception.prototype);
dc.errors.BadArgumentException.prototype.constructor = dc.errors.BadArgumentException;
