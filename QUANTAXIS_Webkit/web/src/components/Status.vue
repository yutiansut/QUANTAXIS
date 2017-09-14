<template>
  <div id="status">
    <h1>状态中心</h1>
    <div id="check_box">
      <mu-table :showCheckbox=false>
        <mu-thead>
          <mu-tr>
            <mu-th>插件名称</mu-th>
            <mu-th>插件端口</mu-th>
            <mu-th>插件状态</mu-th>
            <mu-th>插件地址</mu-th>
          </mu-tr>

        </mu-thead>
        <template v-for="item in items">
          <mu-tbody>
            <tr>
              <mu-td>{{ item['name']}}</mu-td>
              <mu-td>{{ item['port']}}</mu-td>
              <mu-td>{{ item['status']}}</mu-td>
              <mu-td>{{ item['web_link']}}</mu-td>
            </tr>
          </mu-tbody>
        </template>
      </mu-table>
    </div>

  </div>
</template>
<script>
  import axios from 'axios'
  export default {
    name: "home",
    data: function () {
      return {
        items: [{
          'name': 'Nodejs 后端',
          'port': 3000,
          'status':'检测中...',
          'web_link':'https://github.com/yutiansut/QUANTAXIS/tree/master/QUANTAXIS_Webkit/backend'

        }, {
          'name': 'QUANTAXIS Trade 端',
          'port': 5000,
          'status':'检测中...',
          'web_link':'https://github.com/yutiansut/QUANTAXIS/blob/master/QUANTAXIS_Trade'
        }, {
          'name': 'QUANTAXISD 后台',
          'port': 5050,
          'status': '检测中...',
          'web_link':'https://github.com/yutiansut/QUANTAXIS/tree/master/QUANTAXIS/QAWeb'
        }, {
          'name': '实盘易插件',
          'port': 8888,
          'status':'检测中...',
          'web_link':'https://github.com/sinall/ShiPanE-Python-SDK'
        },{
          'name': 'Rainx/Tdx_trade插件',
          'port': 19820,
          'status':'检测中...',
          'web_link':'https://github.com/rainx/TdxTradeServer'
        }],
        item_status: []
      }
    },
    methods: {

      status(i) {
        axios.get('http://localhost:' + this.items[i]['port'] + '/status')
          .then((response) => {
            var data = response.data;
            this.items[i]['status'] = 'ready';
          })
          .catch((error) => {
            this.items[i]['status'] = 'stopped';
          })
      },
      ready() {
        for (var i = 0; i <= this.items.length; i++) {
          this.status(i)

        }


      }
    },

    mounted() {
      this.$nextTick(function () {
         this.ready();

      })
    }
  }

</script>
<style>
  #title {
    position: relative;
    width: 60%;
    height: 100%;
    float: left;
    display: inline-block;
    margin: 10% 0%;
  }

  #check_box {
    position: relative;
    width: 80%;
    height: 100%;
    float: left;

    display: inline-block;
    margin: 10% 0%;
  }

  #title h1 {
    color: darkgrey;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 60px;
  }

  #title h2 {
    color: darkgrey;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    font-size: 20px;
  }

  .demo-raised-button {
    position: relative;
    float: left;
  }

.mu-raised-button-label{
  position: relative;
  float: left;
}

.mu-td{
  white-space: nowrap;
}

.mu-table{
  table-layout:auto;
}
</style>
