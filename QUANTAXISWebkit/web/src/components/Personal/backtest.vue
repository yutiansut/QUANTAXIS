<template>
    <div id="index">

    <li><input v-model="message" v-on:keyup.enter="info($event.currentTarget.value)" placeholder="edit me" lazy></li>
        <li>
          <p>owner is: {{ message }}</p>
        </li>
        <mu-table :height="height" :enableSelectAll="enableSelectAll">
          <mu-thead>
            <mu-tr>
              <mu-th>user</mu-th>
              <mu-th>strategy</mu-th>
              <mu-th>cookie</mu-th>
              <mu-th>start_time</mu-th>
              <mu-th>end_time</mu-th>
              <mu-th>profit</mu-th>
            </mu-tr>
          </mu-thead>
          <template v-for="item in items">

            <mu-tbody>
              <mu-tr>
                <mu-td>{{ item['user']}}</mu-td>
                <mu-td>{{ item['strategy']}}</mu-td>
                <mu-td>{{ item['account_cookie']}}</mu-td>
                <mu-td>{{ item['start_time']}}</mu-td>
                <mu-td>{{ item['end_time']}}</mu-td>
                <mu-td>{{ item['profit']}}</mu-td>
                
              </mu-tr>
            </mu-tbody>
          </template>

        </mu-table>
    </div>
</template>
<script>
import myron from '../assets/QUANTAXIS.jpg'
import axios from 'axios'
export default {
  data:function () {
    return {
        height: '300px',
        multiSelectable: true,
        enableSelectAll: false,
        message: 1,
        items: ['1', '2'],
        total: 130,
        current: 1,
        showSizeChanger: true,
        pageSizeOption: [10, 20, 30, 40]
    }
  },
  methods:{
        info(message) {
        let val = message
        console.log(val)
        axios.get('http://localhost:3000/backtest/info?name=' + val)
          .then(response => {
            this.items = response.data;
            this.length = this.items.length;
            console.log(response.data[0]['start_time'])
          })
          .catch(function (error) {
            console.log(error);
          });
      }
  }
}
</script>
<style lang="css">
    
    .mu-item{
        font-size:10px;
    }
    #personal-content{
        margin-top: 2%;
    }
</style>