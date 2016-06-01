# class

A convenient way to emulated class and inheritance in Javascript.

Why is this "better"?  In the inheritance case, the super function can be called without explicitly referring to the parent class.  One can just write:

```javascript
this.parent.methodName.call(this, args);
```

__Example__

```javascript
var Class = require('better-js-class');

var A = Class({
    _init: function() {
        this._bar = 'bar';
    },

    foo: function() {
        console.log('foo ' + this._bar);
    }
});

var B = Class(A, {
    _init: function() {
        this.parent._init.call(this);
    },

    kaz: function() {
        console.log('kaz ' + this._bar);
    }
});

var a = new B();
a.foo();
a.kaz();
```

## Note

The constructor function's name is conventioned to be "_init".  

