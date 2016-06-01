
var Class = require('better-js-class');
var cps = require('cps');
var $U = require('underscore');

var DB = require('./db.js');

module.exports = function() {
    var Model = {
        OPTIMISTIC_LOCK_EXCEPTION: 'optimistic_lock_exception'
    };

    var Row  = Class({
        _init: function(data, cfg) {
            this._table = cfg.table;
            this._data = data;
        },

        getId: function() {
            return this._data[this._table.getIdFieldName()];
        },

        _getVersion: function() {
            return this._data[this._table.getVersionFieldName()];
        },

        _nextVersion: function() {
            return this._data[this._table.getVersionFieldName()] + 1;
        },

        _updateLocalData: function(dto) {
            for (var k in dto) {
                var v = dto[k];
                this._data[k] = v;
            }
        },

        _refineDtoForUpdate: function(dto) {

            var res = {};

            for (var k in dto) {
                if (this._table._hasUpdatableField(k)) {
                    res[k] = dto[k];
                }
            }

            var d = new Date();
            res[this._table.getUpdatedFieldName()] = d;

            return res;
        },

        updateWithoutOptimisticLock: function(conn, dto, cb) {
            this._update(conn, dto, null, cb);
        },

        update: function(conn, dto, cb) {
            var me = this;

            dto['version'] = this._nextVersion();
            var cond = DB.format('version = ?', [this._getVersion()]);

            cps.seq([
                function(_, cb) {
                    me._update(conn, dto, cond, cb);
                },
                function(res, cb) {
                    if (res.changedRows === 0) {
                        throw new Error(Model.OPTIMISTIC_LOCK_EXCEPTION);
                    } else {
                        cb(null, res);
                    }
                }
            ], cb);
        },

        _update: function(conn, dto, conditions, cb) {
            var me = this;

            // dto[this._table.getUpdatedFieldName()] = new Date();
            dto = this._refineDtoForUpdate(dto);

            var l = [
                ' update ', this._table.getName(), ' set '
            ];

            var first = true;
            for (var k in dto) {
                var v = dto[k];
                if (first) {
                    first = false;
                } else {
                    l.push(', ');
                }
                l.push(
                    ' ', k, ' = ', conn.escape(v)
                );
            }

            l.push(
                ' where ', this._table.getIdFieldName(), ' = ', this.getId()
            );

            if (conditions) {
                l.push(
                    ' and ', conditions
                );
            }

            l.push(' ; ');

            var q = l.join('');

            // console.log(q);

            cps.seq([
                function(_, cb) {
                    conn.query(q, cb);
                },
                function(res, cb) {
                    me._updateLocalData(dto);
                    cb(null, res);
                }
            ], cb);
        },

        get: function(fieldName) {
            return this._data[fieldName]
        },

        _load: function(conn, name, cb) {
            var cfg = this._table._lookupLinksToMap(name);
            if (cfg) {
                return this.linksTo(conn, name, cb);
            }

            var cfg = this._table._lookupLinkedByMap(name);
            if (cfg) {
                return this.linkedBy(conn, name, cb);
            }

            var cfg = this._table._lookupRelatesToMap(name);
            if (cfg) {
                return this.relatesTo(conn, name, cb);
            }

            throw new Error('no linksTo or linkedBy or relatesTo: ' + name + ' defined on: ' + this._table.getName());
        },

        load: function(conn, name, cb) {
            var value = this.get(name);
            if (value) {
                cb(null, value);
            } else {
                this._load(conn, name, cb);
            }
        },

        linksTo: function(conn, name, cb) {
            var me = this;

            var cfg = this._table._lookupLinksToMap(name);

            if (cfg) {
                var otherTable = this._table._db.get(cfg.table).Table;
                return cps.seq([
                    function(_, cb) {
                        otherTable.findById(conn, me.get(cfg.key), cb);
                    },
                    function(res, cb) {
                        me._data[cfg.name] = res;
                        cb(null, res);
                    }
                ], cb);
            } else {
                throw new Error('no linksTo: ' + name + ' defined on: ' + this._table.getName());
            }
        },

        linkedBy: function(conn, name, cb) {
            var me = this;

            var cfg = this._table._lookupLinkedByMap(name);

            if (cfg) {
                var otherTable = this._table._db.get(cfg.table).Table;
                return cps.seq([
                    function(_, cb) {
                        otherTable.find(conn, otherTable.baseQuery('where ' + cfg.key + ' = ?', [me.getId()]), cb);
                    },
                    function(res, cb) {
                        me._data[cfg.name] = res;
                        cb(null, me._data[cfg.name]);
                    }
                ], cb);
            } else {
                throw new Error('no linkedBy: ' + name + ' defined on: ' + this._table.getName());
            }
        },

        relatesTo: function(conn, name, cb) {
            var me = this;

            var cfg = this._table._lookupRelatesToMap(name);
            if (cfg) {
                var otherTable = this._table._db.get(cfg.table).Table;
                var throughTable = this._table._db.get(cfg.through).Table;

                return cps.seq([
                    function(_, cb) {
                        var _q = 'select t.* from ' +
                                otherTable.getName()  + ' t, ' +
                                throughTable.getName() + ' r where ' +
                                'r.' + cfg['leftKey'] + ' = ? and ' +
                                'r.' + cfg['rightKey'] + ' = t.' + otherTable.getIdFieldName()
                            ;
                        var q = DB.format(_q, [me.getId()]);
                        otherTable.find(conn, q, cb);
                    },
                    function(res, cb) {
                        me._data[cfg.name] = res;
                        cb(null, me._data[cfg.name]);
                    }
                ], cb);
            } else {
                throw new Error('no relatesTo: ' + name + ' defined on: ' + this._table.getName());
            }
        }
    });

    var Table = Class({
        _init: function(cfg) {
            this._name = cfg.name;
            this._idFieldName = cfg.idFieldName || 'id';
            this._versionFieldName = cfg.versionFieldName || 'version';
            this._createdFieldName = cfg.createdFieldName || 'date_created';
            this._updatedFieldName = cfg.updatedFieldName || 'last_updated';

            this._rowClass = cfg['rowClass'];
            // this._schema = cfg['schema'];
            this._db = cfg['db'];

            this._linksToMap = {};
            this._linkedByMap = {};
            this._relatesToMap = {};
        },

        getName: function() {
            return this._name;
        },

        getIdFieldName: function() {
            return this._idFieldName;
        },

        getVersionFieldName: function() {
            return this._versionFieldName;
        },

        getCreatedFieldName: function() {
            return this._createdFieldName;
        },

        getUpdatedFieldName: function() {
            return this._updatedFieldName;
        },

        _hasUpdatableField: function(field) {
            if (field == this.getIdFieldName()) {
                return false;
            }
            if (field == this.getCreatedFieldName()) {
                return false;
            }
            var schema = this._db._schema[this.getName()];
            return $U.contains(schema, field);
        },

        _refineDto: function(dto, autoId) {
            autoId = (autoId === undefined)? true: autoId;
            var res = {};

            var schema = this._db._schema[this.getName()];
            $U.each(schema, function(field) {
                res[field] = dto[field];
            });

            if (autoId) {
                delete res[this.getIdFieldName()];
            }

            return res;
        },

        _refineDtoForCreate: function(dto) {
            var res = this._refineDto(dto);

            var d = new Date();
            res[this.getCreatedFieldName()] = d;
            res[this.getUpdatedFieldName()] = d;
            res[this.getVersionFieldName()] = 0;

            return res;
        },

        create: function(conn, dto, cb) {
            dto = this._refineDtoForCreate(dto);
            this._create(conn, dto, cb);
        },

        _create: function(conn, dto, cb) {
            var me = this;

            var l = [
                ' insert into ' + this.getName() + ' set '
            ];

            var first = true;

            $U.each(dto, function(v, k) {
                if (first) {
                    first = false;
                } else {
                    l.push(', ');
                }
                l.push(
                    ' ', k, ' = ', conn.escape(v)
                );
            });

            l.push(' ; ');

            var q = l.join('');

            // console.log(q);

            cps.seq([
                function(_, cb) {
                    conn.query(q, cb);
                },
                function(res, cb) {
                    dto[me._idFieldName] = res.insertId;
                    cb(null, new me._rowClass(dto));
                }
            ], cb);
        },

        clone: function(conn, dto, cb) {
            dto = this._refineDto(dto, false);
            this._create(conn, dto, cb);
        },

        baseQuery: function(str, bindings) {
            var q = ' select * from ' + this.getName() + ' ';
            var further;

            if (str != null) {
                if (bindings == null) {
                    further = str;
                } else {
                    further = DB.format(str, bindings);
                }
            }

            if (further != null) {
                q += further;
            }
            return q;
        },

        findById: function(conn, id, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me.find(conn, me.baseQuery('where ' + me.getIdFieldName() + ' = ? ', [id]), cb);
                },
                function(res) {
                    cb(null, res[0])
                }
            ], cb);
        },

        lockById: function(conn, id, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me.find(conn, me.baseQuery('where ' + me.getIdFieldName() + ' = ? for update', [id]), cb);
                },
                function(res) {
                    cb(null, res[0])
                }
            ], cb);
        },

        findAll: function(conn, cb) {
            this.find(conn, this.baseQuery(), cb);
        },

        find: function(conn, q, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    conn.query(q, cb);
                },
                function(res, cb) {
                    cb(null, $U.map(res, function(o) {
                        return new me._rowClass(o);
                    }));
                }
            ], cb);
        },

        linksTo: function(cfg) {
            this._linksToMap[cfg.name] = {
                table: cfg.table,
                key: cfg.key
            };
            return this;
        },

        linkedBy: function(cfg) {
            this._linkedByMap[cfg.name] = {
                table: cfg.table,
                key: cfg.key
            };
            return this;
        },

        relatesTo: function(cfg) {
            this._relatesToMap[cfg.name] = {
                table: cfg.table,
                through: cfg.through,
                leftKey: cfg.leftKey,
                rightKey: cfg.rightKey
            };
            return this;
        },

        _lookupLinksToMap: function(name) {
            var cfg = this._linksToMap[name];
            if (cfg) {
                cfg.name = name;
            }
            return cfg;
        },

        _lookupLinkedByMap: function(name) {
            var cfg = this._linkedByMap[name];
            if (cfg) {
                cfg.name = name;
            }
            return cfg;
        },

        _lookupRelatesToMap: function(name) {
            var cfg = this._relatesToMap[name];
            if (cfg) {
                cfg.name = name;
            }
            return cfg;
        },

        findFirst: function(conn, q, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me.find(conn, q, cb);
                },
                function(res, cb) {
                    cb(null, res[0]);
                }
            ], cb);
        }
    });

    $U.extend(Model, {
        Row: Row,
        Table: Table
    });

    return Model;
}();
