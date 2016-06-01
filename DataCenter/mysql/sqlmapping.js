var mysql =require('mysql');
module.exports = {

/**
 * 目前的打包几个模块
 * user
 * ts
 * strategy
 */
//需要注意的问题是所有的语句命名法则都要使用驼峰法则。
//语句的控制需要打包 对于不同模块的控制都需要用XX:{},来打包出来
//几个主要的应用场景是：
// A 用户的注册和登录控制
// B 用户登录后的控制面板需要展示用户的策略个数 这个查询要放在页面刷新的时候使用
// C 用户的策略展示  需要查询不同的策略的买卖数据 并且以json格式来传递给前台
/** TODO LIST
 *  D 修改密码
 *  E FORK操作
 * 
 */
    user: {
         //关于用户登录的控制集 CRUD
        insert: "INSERT INTO user(name, password) " + " VALUES(?,?)",
        update: 'update user set name=?, password=? where id=?',
        updatename: 'update users set name=?, age=? where id=?',
        delete: 'delete from users where id=?',
        queryAll: 'SELECT * from user',
        login: 'SELECT * from user where name=? and password=?'
    },

    ts: {
        //关于ts控制的语句集  关于日线数据
        //insert: 'INSERT INTO user(video) VALUES(?,?) where name=?',
        update: 'update user set video=? where name=?',
        queryTableById: 'SELECT * from ??',
        queryTable: 'SELECT * from userlist'
    },

    strategy: {
        //关于策略的语句集  只能对应查询
        //首先需要确定一个用户究竟有几个策略
        //从不同的策略中查询数据  然后做相关的运算 使用JavaScript来描述涨跌与收益
        //querytable就是查询该用户的策略个数
        //querystrategy
        queryTable: 'SELECT * from ?',
        queryStrategy:'SELECT * from ?'
    }


};
