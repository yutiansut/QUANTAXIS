
var Class = require('better-js-class');
var $U = require('underscore');
var _DB = require('./db.js');
var $M = require('./model.js');

var DB = Class(_DB, {
    _init: function(cfg) {
        this.parent._init.call(this, cfg);
        this._models = {};
    },

    add: function(cfg) {
        var me = this;

        var model = {};

        var RowTemplate = function(model) {
            var closedRowClass = Class($M.Row, {
                _init: function(data) {
                    this.parent._init.call(this, data, {
                        table: model.Table
                    });
                }
            });
            return Class(closedRowClass, cfg.Row || {});
        };

        var Row = RowTemplate(model);

        $U.extend(model, {
            Row: Row,
            _RowTemplate: RowTemplate
        });


        var TableTemplate = function(model) {
            var closedTableClass = Class($M.Table, {
                _init: function() {
                    this.parent._init.call(this, {
                        db: me,
                        name: cfg.name,
                        rowClass: model.Row,
                        idFieldName: cfg.idFieldName || 'id',
                        versionFieldName: cfg.versionFieldName || 'version',
                        createdFieldName: cfg.createdFieldName || 'date_created',
                        updatedFieldName: cfg.updatedFieldName || 'last_updated'
                    });
                }
            });

            return Class(closedTableClass, cfg.Table || {});
        };

        var TableClass = TableTemplate(model);
        var Table = new TableClass();

        $U.extend(model, {
            Table: Table,
            _TableTemplate: TableTemplate
        });

        this._models[cfg.name] = model;

        return Table;
    },

    clone: function() {
        var tempClass = function() {
            this._models = $U.clone(this._models);
        };

        tempClass.prototype = this;
        return new tempClass();
    },

    extend: function(cfg) {
        var _model = this.get(cfg.name);

        if (!_model) {
            throw new Error('node-mysql-runtime-error: db.extend can not be used on empty model.');
        }

        var model = {};

        var _RowTemplate = _model._RowTemplate;

        var RowTemplate = function(model) {
            var superClass = _RowTemplate(model);
            return Class(superClass, cfg.Row || {});
        };

        var Row = RowTemplate(model);

        $U.extend(model, {
            Row: Row,
            _RowTemplate: RowTemplate
        });

        var _TableTemplate = _model._TableTemplate;

        var TableTemplate = function(model) {
            var superClass = _TableTemplate(model);
            return Class(superClass, cfg.Table || {});
        };

        var TableClass = TableTemplate(model);

        var Table = new TableClass();

        $U.extend(model, {
            Table: Table,
            _TableTemplate: TableTemplate
        });

        this._models[cfg.name] = model;

        return Table;
    },

    get: function(name) {
        return this._models[name];
    }
});

DB.format = _DB.format;

module.exports = {
    DB: DB,
    Row: $M.Row,
    Table: $M.Table,
    OPTIMISTIC_LOCK_EXCEPTION: $M.OPTIMISTIC_LOCK_EXCEPTION
}


