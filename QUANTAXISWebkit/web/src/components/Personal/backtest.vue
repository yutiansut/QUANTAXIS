<template>
  <div id="index">

    <li><input v-model="message" v-on:keyup.enter="info($event.currentTarget.value)" placeholder="edit me" lazy>
      <input v-model="messages" v-on:keyup.enter="code($event.currentTarget.value)" placeholder="edit me" lazy></li>
    <mu-table :height="height">
      <mu-thead>
        <mu-tr>
          <mu-th>user</mu-th>
          <mu-th>strategy</mu-th>
          <mu-th>code</mu-th>
          <mu-th>start</mu-th>
          <mu-th>end</mu-th>
          <mu-th>profit</mu-th>
          <mu-th>alpha</mu-th>
          <mu-th>annualized_returns</mu-th>
        </mu-tr>
      </mu-thead>
      <template v-for="item in items">

        <mu-tbody>
          <mu-tr>
            <router-link :to="{ name:'history',params: {id:item['account_cookie']}}">
              <mu-td>{{ item['user']}}</mu-td>
              <mu-td>{{ item['strategy']}}</mu-td>
              <mu-td>{{ item['stock_list']}}</mu-td>
              <mu-td>{{ item['start_time']}}</mu-td>
              <mu-td>{{ item['end_time']}}</mu-td>
              <mu-td>{{ item['profit']}}</mu-td>
              <mu-td>{{ item['alpha']}}</mu-td>
              <mu-td>{{ item['annualized_returns']}}</mu-td>
            </router-link>
          </mu-tr>
        </mu-tbody>

      </template>

    </mu-table>
  </div>
</template>
<script>
  import axios from 'axios'
  export default {
    data: function () {
      return {
        height: '500px',
        multiSelectable: true,
        enableSelectAll: false,
        message: 'yutiansut',
        messages: 'code',
        items: [''],
        total: 180,
        current: 1,
        showSizeChanger: true
      }
    },
    methods: {
      info(message) {
        let val = message
        console.log(val)
        axios.get('http://localhost:3000/backtest/info?name=' + val)
          .then(response => {
            this.items = response.data;
            console.log(this.items)
            this.length = this.items.length;
            var performance = response.data[0]['performance'];
            console.log(performance)
          })
          .catch(function (error) {
            console.log(error);
          });
      },
      code(message) {
        let val = message
        console.log(val)
        axios.get('http://localhost:3000/backtest/info_code?code=' + val)
          .then(response => {
            this.items = response.data;
            console.log(this.items)
            this.length = this.items.length;
            var performance = response.data[0]['performance'];
            console.log(performance)
          })
          .catch(function (error) {
            console.log(error);
          });
      }

    }
  }
</script>
<style lang="css">
  .mu-item {
    font-size: 10px;
  }

  #personal-content {
    margin-top: 2%;
  }
</style>