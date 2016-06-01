# node-mysql

An enhancement to the mysql lib to make it a bit easier to use.  Based on the existing funtionalities of (npm) mysql, it also

* Handles transactions.
* Provides a simple ORM, which
  * Detects table schema automatically.
  * Provides handy functions for creating and updating rows.
  * Handles optimistic lock through versioning transparently.
  * Maintains "date_created" and "last_updated" automatically.
  * Provides database row level lock functionality.

## Install

```text
npm install node-mysql
```

### Dependencies

```json
    "dependencies": {
        "better-js-class": "*",
        "cps": "*",
        "mysql": "*",
        "underscore": "*"
    }
```

## Use

```javascript
var db = require('node-mysql');
var DB = db.DB;
var BaseRow = db.Row;
var BaseTable = db.Table;
```

## APIs

* DB
  * [new DB](#new-DB)
  * [db.connect](#db-connect)
  * [db.transaction](#db-transaction)
  * [db.cursor](#db-cursor)
  * [db.end](#db-end)
  * [db.add](#db-add)
  * [db.get](#db-get)
  * [DB.format](#DB-format)
* Table
  * [new Table](#new-Table)
  * [table.create](#table-create)
  * [table.clone](#table-clone)
  * [table.find](#table-find)
  * [table.findById](#table-findById)
  * [table.lockById](#table-lockById)
  * [table.findAll](#table-findAll)
  * [table.baseQuery](#table-baseQuery)
  * [table.linksTo](#table-linksTo)
  * [table.linkedBy](#table-linkedBy)
  * [table.relatesTo](#table-relatesTo)
* Row
  * [new Row](#new-Row)
  * [row.update](#row-update)
  * [row.updateWithoutOptimisticLock](#row-updateWithoutOptimisticLock)
  * [row.get](#row-get)
  * [row.getId](#row-getId)
  * [row.linksTo](#row-linksTo)
  * [row.linkedBy](#row-linkedBy)
  * [row.relatesTo](#row-relatesTo)

<a name="new-DB"/>
### new DB(conf)

Please refer to the the [connection pool conf](https://github.com/felixge/node-mysql#pooling-connections) in mysql package for the format of "conf".

__Example__

```javascript
var box = new DB({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone'
});
```

Beyond the configuration fields provided by mysql package, there are two additional configuration fields that can be used in "conf":

* useTransaction
* useCursor


#### useTransaction

Only if "useTransaction" is provided can "[db.transaction](#db-transaction)" API be called.  Otherwise, calls to "[db.transaction](#db-transaction)" will throw an error with the message "transation-not-setup-error".  The "useTransaction" field itself is an configuration object that overrides the fields in "conf" to set up a connection pool for transactions.  For instance:

__Example__

```javascript
var box = new DB({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50,
    useTransaction: {
        connectionLimit: 1
    }
});
```

will allow the db object "box" to use "box.transaction" API, with a connection pool for transactions set up the same way as the normal connection pool except for the connectionLimit field being overridden to 1.  So in "box", there are two mysql connection pools, for normal db requests and transactional db requests, repectively.  The normal connection pool's configuration is: 

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50
}
```

while the transactional connection pool's configuration is:

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 1
}
```

#### useCursor

Similarly to "useTransaction", only if "useCursor" is provided can "[db.cursor](#db-cursor)" API be called.  Otherwise, calls to "[db.cursor](#db-cursor)" will throw an exception with the error message "cursor-not-setup-error".  The field "useCursor" is very similar to the field "useTransaction", with the only difference that it is for setting up the mysql connection pool for cursors rather than transactions.  "useCursor" is also an overriding object based upon the connection pool configuration for normal connections.  For instance:

__Example__

```javascript
var box = new DB({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50,
    useCursor: {
        connectionLimit: 1
    }
});
```

will allow the API "box.cursor" to be called, with a connection pool for cursors set up the same way as the normal connection pool except for the connectionLimit field being overridden to 1.  So in "box", there are two mysql connection pools, for normal db requests and cursor db requests, repectively.  The normal connection pool's configuration is: 

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50
}
```

while the cursor connection pool's configuration is:

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 1
}
```

#### Use Both

"useTransaction" and "useCursor" can be used together:

__Example__

```javascript
var box = new DB({
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50,
    useTransaction: {
        connectionLimit: 20
    },
    useCursor: {
        connectionLimit: 1
    }
});
```

This will allow all of the three APIs, "box.connect", "box.transaction" and "box.cursor" to be called.  In this case, box hold three connection pools, for normal connections, transactional connections and cursor connections, respectively.  The normal connection pool is configured as:

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 50
}
```

the transactional connection pool is configured as:

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 20
}
```

and the cursor connection pool is configured as:

```javascript
{
    host     : 'localhost',
    user     : 'root',
    password : '',
    database : 'prod_clone',
    connectionLimit: 1
}
```


<a name="db-connect">
### db.connect(procedure, callback)

The procedure is a function of the type: 

```javascript
function(connection, callback) {
    // work with the database connection 
}
```

__Example__

```javascript
var basicTest = function(cb) {
    box.connect(function(conn, cb) {
        cps.seq([
            function(_, cb) {
                conn.query('select * from users limit 1', cb);
            },
            function(res, cb) {
                console.log(res);
                cb();
            }
        ], cb);
    }, cb);
};
```

<a name="db-transaction"/>
### db.transaction(db_connection, procedure, callback)

The procedure is a function of the type: 

```javascript
function(connection, callback) {
    // work with the database connection 
}
```

Note that db.transaction takes one more arguemnt than the db.connect,
which is a database connection object.  If this connection object is
already a transactional, then it will be used directly in the provided
procedure.  Otherwise, the connection will be "made transactional" and
then used in the provided procedure.

__Example__

```javascript
var txnTest = function(cb) {
    var add2Rows = function(conn, b, cb) {
        dw.transaction(
            conn/*This is a non-transactional connection.*/, 
            function(
                conn/*A new transactional connection is 
                      created to handle the transactional session.*/, 
                cb
            ) {
                cps.seq([
                    function(_, cb) {
                        Model.Table.create(conn, getSampleDto(), cb);
                    },
                    function(_, cb) {
                        dw.transaction(
                            conn/*This is already a transactional connection.*/, 
                            function(
                                conn/*No new transactional connection created. 
                                      This connection is the same one as 
                                      in the calling context*/, 
                                cb
                            ) {
                                console.log(conn.__transaction__)
                                Model.Table.create(conn, getSampleDto(), cb);
                            }, 
                            cb
                        );
                    },
                    function(_, cb) {
                        if (b) {
                            cb(null, "Commit");
                        } else {
                            throw new Error("Roll back");
                        }
                    }
                ], cb);
            }, 
            cb
        );
    };

    dw.connect(function(conn, cb) {
        /* Uncommenting the following line will merge the two calls 
           to add2Rows into one transaction. */
        // dw.transaction(conn, function(conn, cb) {
            cps.seq([
                function(_, cb) {
                    add2Rows(conn, true, cb);
                },
                function(_, cb) {
                    add2Rows(conn, true, cb);
                }
            ], cb);
        // }, cb);
    }, cb);
};
```

<a name="db-cursor"/>
### db.cursor(query_string, procedure, callback)

This API can be used to cursor thought the (potentially very long list
of) results of a query.  The procedure parameter is the operation to
be applied to each row in the results of the query.  Please note the following:

* db.cursor will create a separate db connection for cursoring
  purpose.  That is why this API does not take a db_connection in the
  parameter list, unlike most of the other db related APIs.  

* If there is an exception thrown out of the row handling procedure,
  the cursoring will be stopped and the exception will be thrown out
  to the top level callback (the 3rd parameter to db.cursor).  If you
  intend for the cursor to go over all the results, you need to catch
  any exceptions in the row handling procedure (using cps.rescue).

__Example__

```javascript
// cursor through all the users and update the active status to "1"
var cursorTest = function(cb) {
    db.connect(function(conn, cb) {
        var q = 'select * from users';

        db.cursor(q, function(row, cb) {
            cps.rescur({
                'try': function() {
                    cps.seq([
                        function(_, cb) {
                            var user = new User.Row(row);
                            user.update(conn, {active: 1}, cb);
                        }, 
                        function(res, cb) {
                            console.log(res);
                            cb();
                        }
                    ], cb);
                },
                'catch': function(err, cb) {
                    console.log(err);
                    cb();
                }
            }, cb);
        }, cb);
    }, cb);
};
```




<a name="db-end" />
### db.end();

This function destructs the db object.

<a name="db-add"/>

### db.add(config);

This function is used to define a model that belongs to the db object.  The model config object is of the following format:

```json
{
    "name": {
        "type": "String",
        "description": "the name of the table"
    },
    "idFieldName": {
        "type": "String",
        "optional": true, 
        "default": "id",
        "description": "the name of the primary id column"
    },
    "versionFieldName": {
        "type": "String", 
        "optional": true, 
        "default": "version", 
        "description": "optimistic lock version"
    },
    "createdFieldName": {
        "type": "String",
        "optional": true, 
        "default": "date_created",
        "description": "creation time of the row"
    },
    "updatedFieldName": {
        "type": "String",
        "optional": true, 
        "default": "last_updated",
        "description": "last update time of the row"
    },
    "Row": {
        "type": "Object",
        "optional": true,
        "default": "{}",
        "description": "the overriding method definition for the Row class of this model"
    },
    "Table": {
        "type": "Object",
        "optional": true,
        "default": "{}",
        "description": "the overriding method definition for the Table class of this model"
    }
}
```

Note that db.add returns a Table object, which can be further chained
with linking/joining functions such as [linksTo](#table-linksTo),
[linkedBy](#table-linkedBy) and [relatesTo](#table-relatesTo).

__Example__

```javascript
db.add({
    name: 'orders',
    idFieldName: 'order_id',
    Row: {
        getFirstOrderItem: function(conn, cb) {
            var me = this;

            cps.seq([
                function(_, cb) {
                    me.linkedBy(conn, 'items', cb);
                },
                function(items, cb) {
                    cb(null, items[0]);
                }
            ], cb);
        }
    },
    Table: {
        createOrderUsingCoupon: function(conn, dto, coupon, cb) {
            dto['coupon_id'] = coupon.getId();
            this.create(conn, dto, cb);
        }
    }
})
    .linkedBy({
        name: 'items',
        key: 'order_id',
        table: 'order_items'
    })
    .linksTo({
        name: 'user',
        key: 'user_id',
        table: 'users'
    })
    .linksTo({
        name: 'coupon',
        key: 'coupon_id',
        table: 'coupons'
    })
    .linksTo({
        name: 'credit_card',
        key: 'credit_card_id',
        table: 'credit_cards'
    })
;

```

In this example: 

* We created a model for the table "orders" in the database.  
* We add a method getFirstOrderItem into the Row class of this model.
* We add a method createOrderWithCoupon into the Table class of this model.
* We follow the foreign key relations of the "orders" table to define some link relations.

<a name="db-get"/>

### db.get(table_name)

Once you use db.add to create a model in the db object, you can then
use db.get to retrieve it by name.  The return value of
db.get if a object of the following format:

```json
{
    "Row": {
        "type": "Row object"
    },
    "Table": {
        "type": "Table object"
    }
}
```

__Example__

```javascript
var Order = db.get('orders');
var Coupon = db.get('coupons');

db.connect(function(conn, cb) {
    cps.seq([
        function(_, cb) {
            Coupon.Table.findByCode(conn, '10-percent-off', cb);
        }
        function(coupon, cb) {
            var dto = {/*dto data*/};
            Order.createOrderWithCoupon(conn, dto, coupon, cb);
        },
        function(order, cb) {
            order.getFirstOrderItem(conn, cb);
        },
        function(firstItem, cb) {
            console.log(firstItem);
            cb()
        }
    ], cb);
}, cb);
```


<a name="DB-format" />
### DB.format(query_string, variable_bindings)

This is a wrapper of the query string formatting functionality
provided by the mysql package.  Note that this is a global static
method defined on the class DB.  It is NOT an instance method defined
a a DB instance db.

__Example__

```javascript
DB.format('select * from users where id = ?' [userId]);
```
<a name="new-Table"/>
### new Table(table_config)

The table config schema is defined as follows:

```json
{
    "name": {
        "type": "String",
        "optional": false,
        "description": "the name of the database table"
    },
    "idFieldName": {
        "type": "String",
        "optional": true, 
        "default": "id",
        "description": "the name of the primary id column"
    },
    "versionFieldName": {
        "type": "String", 
        "optional": true, 
        "default": "version", 
        "description": "optimistic lock version"
    },
    "createdFieldName": {
        "type": "String",
        "optional": true, 
        "default": "date_created",
        "description": "creation time of the row"
    },
    "updatedFieldName": {
        "type": "String",
        "optional": true, 
        "default": "last_updated",
        "description": "last update time of the row"
    },
    "rowClass": {
        "type": "Row class",
        "optional": false,
        "description": "the Row class of this table"
    },
    "db": {
        "type": "DB class instance",
        "optional": false,
        "description": "the DB instance that the table belongs to"
    }   
}
```

See [here](#row-table-instantiation) for an example of creating a table.  


<a name="table-create"/>

### table.create(database_connection, data_object, callback)

The callback here takes a Row object as result.

__Example__

```javascript
var createTest = function(cb) {
    dw.connect(function(conn, cb) {
        cps.seq([
            function(_, cb) {
                User.Table.create(conn, {
                    first_name: 'Hannah',
                    last_name: 'Mckay',
                    gender: 'female'
                    // ....
                }, cb);
            },
            function(user, cb) {  // user is an object of the class User.Row
                console.log(user.get('first_name')); // print out 'Hannah'
                cb();
            }
        ], cb);
    }, cb);
};
```

In the input data object, please do NOT specify the following fields:

* primary ID
* date_created
* last_udpated
* version

All of the these fields will be filled by the invocation to table.create.


<a name="table-clone"/>

### table.clone(database_connection, data_object, callback)

This API is very similar to table.create.  The key difference is that
it does not mask out any data field carried in data_object.  Instead,
it literally uses every thing in data_object to create a new row.  In
other words, it'll honor the values of the following fields in
data_object:

* primary ID
* date_created
* last_udpated
* version

This API can be useful when one attempts to clone a row in a table
literally to another table (which might be in another database).

<a name="table-find"/>
### table.find(database_connection, query_string, callback)

This function is not too different from doing a query directly on a
database connection.  The only extra thing it does is to turn the
result from a list of simple hash objects to a list of Row objects of
the corresponding table's "rowClass".

__Example__

```javascript
dw.connect(function(conn, cb) {
    var o;
    cps.seq([
        function(_, cb) {
            User.Table.find(conn, 'select * from users', cb);
        },
        function(users, cb) { // users is a list of user object of the class User.Row
            console.log(users[0]);  // print the information of the first user
            cb();
        }
    ], cb);
}, cb);
```

<a name="table-findById"/>
### table.findById(database_connection, row_id, callback)

This is simply a short-hand for:

```javascript
cps.seq([
    function(_, cb) {
        table.find(
            conn, 
            DB.format('select * from table_name where primary_id = ?', [row_id]),
            cb
        );
    },
    function(res, cb) {
        cb(res[0]);
    }
], cb);
```

It finds a row in a table by its primary ID and returns a single row
object of the table's corresponding rowClass.

<a name="table-lockById"/>
### table.lockById(database_connection, row_id, callback)

This function does the same thing as findById and additionally, it
locks the corresponding row for an atomic update.  lockById can ONLY
be used in a transaction context.  Without a transaction context, it
behaves the same as findById.  Once a row is locked in one
transaction, attempts of locking the same row in other transactions
will hang until the current transaction either commits or rolls back,
which release the current lock.

__Example__

```javascript
var lockTest = function(cb) {
    var exclusiveUpdate = function(conn, delay, value, cb) {
        dw.transaction(null, function(conn, cb) {
            cps.seq([
                function(_, cb) {
                    Model.Table.lockById(conn, 1, cb);
                },
                function(res, cb) {
                    setTimeout(function() {
                        cb(null, res);
                    }, delay);
                },
                function(row, cb) {
                    row.update(conn, {'subscription_status': value}, cb);
                },
                function(res, cb) {
                    cb();
                }
            ], cb)
        }, cb);

    };

    var conn;

    dw.transaction(conn, function(conn, cb) {
        cps.seq([
            function(_, cb) {
                cps.parallel([
                    function(cb) {
                        exclusiveUpdate(conn, 2000, 'foo1', cb);
                    },
                    function(cb) {
                        exclusiveUpdate(conn, 0, 'bar1', cb);
                    }
                ], cb);
            },
            function(res, cb) {
                console.log(res);
                cb();
            }
        ], cb);
    }, cb);
};
```

In this example, two threads are executed in parallel.  The thread of
setting value "bar1" will be block by the thread of setting value
"foo1".

<a name="table-findAll"/>
### table.findAll(database_connection, callback)

This finds all the rows in a table.

<a name="table-baseQuery"/>
### table.baseQuery(query_string, variable_bindings)

This is a short-hand for:

```javascript
DB.format('select * from table_name' + query_string, variable_bindings);
```

It simply prepend a partial string indicating from which table the
query is being performed.  This might come handy in many cases.

<a name="table-linksTo"/>
### table.linksTo(config)

The config object has the following schema:

```json
{
    "name": {
        "type": "String",
        "description": "The name of the field to add to the row's data."
    },
    "key": {
        "type": "String",
        "description": "The key that belongs to the current table and links to another table."
    },
    "table": {
        "type": "String",
        "description": "The name of the table that the current table links to."
    }
}
```

__Example__

```javascript
    Order.Table
        .linksTo({
            name: 'credit_card',
            key: 'credit_card_id'
            table: 'credit_cards'
        })
        .linksTo({
            name: 'shipping_address',
            key: 'shipping_address_id'
            table: 'addresses'
        })
    ;
```

Note that for "linksTo", the (join) key is on the current table.  Once
a "linksTo" is set up, a row object that corresponds to this table can
call the "linksTo" method to pull more (associated) data into the row.
See examples [here](#row-linksTo).

<a name="table-linkedBy"/>
### table.linkedBy(config)

The config object has the following schema:

```json
{
    "name": {
        "type": "String",
        "description": "The name of the field to add to the row's data."
    },
    "key": {
        "type": "String",
        "description": "The key that belongs to the other table and links to the current table."
    },
    "table": {
        "type": "String",
        "description": "The name of the table that the current table is linked by."
    }
}
```

__Example__

```javascript
    Order.Table
        .linkedBy({
            name: 'items',
            table: OrderItem.Table,
            key: 'order_id'
        })
    ;
```

Once a "linkedBy" is set up on a table, a row object corresponding to
this table can call the "linkedBy" method to pull more (associated)
data into the row.  See examples [here](#row-linkedBy).

<a name="table-relatesTo"/>

### table.relatesTo(config)

The config object has the following schema:

```json
{
    "name": {
        "type": "String",
        "description": "The name of the field to add to the row's data."
    },
    "through": {
        "type": "String",
        "description": "The name of the through table, which joins both the current table and the target table."
    },
    "leftKey": {
        "type": "String",
        "description": "The key that belongs to the current table and joins with the through table."
    },
    "table": {
        "type": "String",
        "description": "The name of the target table that the current table is joining thourgh the through-table."
    },
    "rightKey": {
        "type": "String",
        "description": "The key that belongs to the target table and joins with the through table."
    }
}
```

__Example__

```javascript
    Order.Table
        .relatesTo({
            name: 'coupons',
            leftKey: 'order_id',
            through: 'order_coupons',
            rightKey: 'coupon_id',
            table: 'coupons'
        })
    ;
```

table.relatesTo is designed to represent ORM of a many-to-many
relation.  Once a "relatesTo" is set up on a table, a row object
corresponding to this table can call the "relatesTo" method to pull
more (associated) data into the row.  See examples
[here](#row-relatesTo).

<a name="new-Row" />
### new Row(row_data)

After having a concrete Row class, row instances can be created using
it.  The row_data parameter is an object mapping database table column
names to their corresponding values.

__Example__

```javascript
new User.Row({
    first_name: 'Hannah',
    last_name: 'Mckay',
    gender: 'female'
    //....
});
```
<a name="row-update"/>

### row.update(database_connection, update_object, callback)

This function will set the following column automatically:

* last_updated.  This field will be set to the present time stamp.
* version.  This field will be increased.

Other than these columns, only columns listed in the update_object will be updated.

__Example__

```javascript
var findAndUpdateTest = function(cb) {
    dw.connect(function(conn, cb) {
        cps.seq([
            function(_, cb) {
                User.Table.findById(conn, id, cb);
            },
            function(user, cb) {
                var dto = {
                    'last_name': 'Morgan'
                };
                user.update(conn, dto, cb);
            }
        ], cb);
    }, cb);
};
```

<a name="row-updateWithoutOptimisticLock"/>
### row.updateWithoutOptimisticLock(database_connection, update_object, callback)

This function is the same as row.update with only one difference: it
does not care about the optimistic lock version field.  It neither
looks at this field nor update field.  This might be useful
ocasionally when optimistic lock functionality needs to be overriden.


<a name="row-get"/>
### row.get(column_name)

Get the value of a certain column from the row object.

<a name="row-getId"/>
### row.getId()

Get the primary ID of the row object.

<a name="row-linksTo"/>
### row.linksTo(database_connection, field_name, callback)

Given a "linksTo" setup in the corresponding "Table" object, row.linksTo pulls further relevant data into the row.

__Example__

```javascript
var order;

cps.seq([
    function(_, cb) {
        Order.Table.findById(conn, id, cb);
    },
    function(res, cb) {
        order = res;
        order.linksTo(conn, 'credit_card', cb);
    },
    function(_, cb) {
        order.linksTo(conn, 'shipping_address', cb);
    },
    function(_, cb) {
        console.log(order.get('credit_card').getId());
        console.log(order.get('shipping_address').getId());
        cb();
    }
], cb);
```

<a name="row-linkedBy"/>
### row.linkedBy(database_connection, field_name, callback)

Given a "linkedBy" setup in the corresponding "Table" object, row.linkedBy pulls further relevant data into the row.

__Example__

```javascript
var order;

cps.seq([
    function(_, cb) {
        Order.Table.findById(conn, id, cb);
    },
    function(res, cb) {
        order = res;
        order.linkedBy(conn, 'items', cb);
    },
    function(items, cb) {
        // items will both be bound to the return value and be assigned to the 'items' field.
        console.log(items);
        console.log(order.get('items'));
        cb();
    }
], cb);
```

<a name="row-relatesTo"/>
### row.relatesTo(database_connection, field_name, callback)

Given a "relatesTo" setup in the corresponding "Table" object, row.relatesTo pulls further relevant data into the row.

__Example__

```javascript
var order;

cps.seq([
    function(_, cb) {
        Order.Table.findById(conn, id, cb);
    },
    function(res, cb) {
        order = res;
        order.relatesTo(conn, 'coupons', cb);
    },
    function(coupons, cb) {
        // coupons will both be bound to the return value and be assigned to the 'coupons' field.
        console.log(coupons); 
        console.log(order.get('coupons'));
        cb();
    }
], cb);
```
