<template>
  <div id="index">
    <h2 align='left'>> 实盘监控</h2>
  
    <h3 align='left'>最新时间 {{this.time['date']}} {{this.time['time']}}</h3>
    <mu-table :height="height" :showCheckbox=false>
      <mu-thead>
        <mu-tr>
          <mu-th>资金帐号</mu-th>
          <mu-th>可用资金 </mu-th>
          <mu-th>冻结资金</mu-th>
          <mu-th>在途资金 </mu-th>
          <mu-th>可取资金</mu-th>
  
        </mu-tr>
  
      </mu-thead>
  
      <mu-tbody>
        <tr>
          <mu-td>{{ this.cash['account_id']}}</mu-td>
          <mu-td>{{ this.cash['available']}}</mu-td>
          <mu-td>{{ this.cash['freeze']}}</mu-td>
          <mu-td>{{ this.cash['on_way']}}</mu-td>
          <mu-td>{{ this.cash['withdraw']}}</mu-td>
        </tr>
      </mu-tbody>
  
      <mu-thead>
        <mu-tr>
  
          <mu-th>证券代码</mu-th>
          <mu-th>证券名称 </mu-th>
  
          <mu-th>持仓量 </mu-th>
  
          <mu-th>可卖数量 </mu-th>
          <mu-th>当前价</mu-th>
          <mu-th> 最新市值</mu-th>
  
          <mu-th> 成本价</mu-th>
          <mu-th>浮动盈亏 </mu-th>
          <mu-th>盈亏比例(%) </mu-th>
          <mu-th>昨日价格 </mu-th>
  
        </mu-tr>
        <template v-for="item in items">
  
          <mu-tbody>
            <mu-tr>
              <!--
  
          temp['exchange']=stocks[i].split('\t')[13]
          temp['']=stocks[i].split('\t')[14]
          temp['insure_mark']=stocks[i].split('\t')[15]
          temp['buy_today']=stocks[i].split('\t')[16]
          temp['sell_today']=stocks[i].split('\t')[17]
          temp['position_buy']=stocks[i].split('\t')[18]
          temp['position_sell']=stocks[i].split('\t')[19]
          temp['price_yesterday']=stocks[i].split('\t')[20]
          temp['margin']=stocks[i].split('\t')[21]-->
              <mu-td>{{ item['code']}}</mu-td>
              <mu-td>{{ item['name']}}</mu-td>
              <mu-td>{{ item['hold']}}</mu-td>
              <mu-td>{{ item['sell_available']}}</mu-td>
              <mu-td>{{ item['price_now']}}</mu-td>
              <mu-td>{{ item['value_now']}}</mu-td>
              <mu-td>{{ item['price_buy']}}</mu-td>
              <mu-td>{{ item['pnl_float']}}</mu-td>
              <mu-td>{{ item['pnl_ratio']}}</mu-td>
              <mu-td>{{ item['price_yesterday']}}</mu-td>
  
            </mu-tr>
          </mu-tbody>
  
        </template>
  
      </mu-thead>
    </mu-table>
  
  </div>
</template>

<script>
import axios from 'axios'
export default {
  data: function () {
    return {
      height: '500px',
      items: [],
      time: {},
      cash: {},

    }
  },
  methods: {
    query_positions() {
      axios.get('http://localhost:5000/trade/query/assets')
        .then(response => {
          var data = response.data;
          this.cash = data['cash'];
          var stock = data['stock'];
          this.time = data['time'];
          this.items = stock;
          //console.log(this.cash['account_id'])
          //this.items = cash;
          this.query_positions()
        })
        .catch(function (error) {
          console.log(error);
        });
    }

  },
  mounted() {
    this.$nextTick(function () {
      //this.scroller = this.$el
      this.query_positions();
    })

  },
}

</script>
<style lang="css">
.mu-item {
  font-size: 10px;
}

.mu-tr {
  width: 100px;
}

th.mu-th {
  padding-left: 10px;
  padding-right: 10px;
  text-align: left;
}

.mu-td {
  width: 100px;

  text-align: left;
}
</style>