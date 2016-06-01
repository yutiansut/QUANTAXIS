var mysql = require('mysql');
var $conf = require('./conn');
var $sql = require('./sqlmapping');
var express = require('express');
var router = express.Router();
// 使用连接池，提升性能
var pool = mysql.createPool($conf.mysql);


var jsonWrite = function (res, ret) {
    if (typeof ret === 'undefined') {
        res.json({
            code: '1',
            msg: '操作失败'
        });
    } else {
        res.json(ret);
    }
};


module.exports = {
    queryByName: function (req, res, next) {
        pool.getConnection(function (err, connection) {
            var name = +req.query.name; // 为了拼凑正确的sql语句，这里要转下整数

            var sqlq = mysql.format($sql.ts.queryts, name);
            console.log('name' + name)
            //connection.config.queryFormat = sqlsplit.yutiansutsqlsplit (sqlq, values) ;

            connection.config.queryFormat = function (query, values) {
                if (!values) return query;
                return query.replace(/\:(\w+)/g, function (txt, key) {
                    if (values.hasOwnProperty(key)) {
                        return this.escape(values[key]);
                    }
                    return txt;

                }.bind(this));
            };
            console.log(sqlq)
            console.log(name)
            pool.getConnection(function (err, connection) {
                console.log(sqlq)
                connection.query(sqlq, function (err, result) {
                    jsonWrite(res, result);
                    connection.release();

                });
            });
        });
    },
    querytable:function (req, res, next) {
        console.log('1'+req.body.name);
        console.log('2'+req.query.name);
        console.log('3'+req.param.name);
        pool.getConnection(function (err, connection) {
            if (err) console.log('err----'+err);
            connection.query($sql.ts.queryTable, function (err, result) {
                if (err) console.log('err----'+err);
                jsonWrite(res, result);
                connection.release();
            });
        });
    }, 
    queryTableById:function (req, res, next) {
       
        pool.getConnection(function (err, connection) {
            if (err) console.log('err----'+err);
            connection.query($sql.ts.queryTableById,req.query.name, function (err, result) {
                if (err) console.log('err----'+err);
                jsonWrite(res, result);
                connection.release();
            });
        });
    }
    


};