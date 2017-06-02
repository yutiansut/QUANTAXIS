<template>
    <div>
          <h1>实盘易</h1>
    <mu-table >手动下单</mu-table>
        <mu-th>s</mu-th>
    </div>

</template>

<script>        
import axios from 'axios'

export default {
name: 'shipan-e',
data: function () {
    return { 
      positions:[]
        
    }},
methods:{
  query_positions(){
    axios.get('http://localhost:8888/positions')
      .then(function (response) {
         var data1 = response.data;
         console.log(data1)
          })
  }

    },
     mounted() {
      this.$nextTick(function () {
        this.query_positions()
      })
    
    
    }}
/**
 * 查询账号
GET http://localhost:8888/accounts

查询资金股份
GET http://localhost:8888/positions

查询当日委托
GET http://localhost:8888/orders

查询撤单
GET http://localhost:8888/orders?status=open

查询当日成交
GET http://localhost:8888/orders?status=filled

买入
POST http://localhost:8888/orders
Content-Type: application/json

{
  "action": "BUY",
  "symbol" : "000001",
  "type": "LIMIT",
  "priceType" : 0,
  "price" : 9.00,
  "amount" : 100
}

type 可选择：

LIMIT - 限价单，需指定 price
MARKET - 市价单，需指定 priceType（非 0）
priceType 可选择：
上海交易所：

0 - 限价委托
4 - 五档即时成交剩余撤销
6 - 五档即时成交剩余转限
深圳交易所：

0 - 限价委托
1 - 对手方最优价格委托
2 - 本方最优价格委托
3 - 即时成交剩余撤销委托
4 - 五档即时成交剩余撤销
5 - 全额成交或撤销委托
amountProportion 和 amount 二选一
amountProportion 可选择：ALL, 1/2, 1/3, 1/4, 1/5

以上参数设置也适用于"卖出"

卖出
POST http://localhost:8888/orders
Content-Type: application/json

{
  "action": "SELL",
  "symbol" : "000001",
  "type": "LIMIT",
  "priceType" : 0,
  "price" : 9.00,
  "amount" : 100
}

撤单
DELETE http://localhost:8888/orders/O1234
（注：上面 URL 中的 O1234 应替换为相应的委托编号）

撤单全部
DELETE http://localhost:8888/orders

查询其他
GET http://localhost:8888?navigation=查询>当日委托

查询状态
GET http://localhost:8888/statuses

启动并自动登录通达信
PUT http://localhost:8888/clients

关闭所有通达信
DELETE http://localhost:8888/clients
                
*/
</script>
