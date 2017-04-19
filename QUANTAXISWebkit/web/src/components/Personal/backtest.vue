<template>
    <div id="index">

    <li><input v-model="message" v-on:keyup.enter="info($event.currentTarget.value)" placeholder="edit me" lazy></li>
        <mu-table :height="height" >
          <mu-thead>
            <mu-tr>
              <mu-th>user</mu-th>
              <mu-th>strategy</mu-th>
              <mu-th>code</mu-th>
              <mu-th>start</mu-th>
              <mu-th>end</mu-th>
              <mu-th>profit</mu-th>
              <mu-th>per</mu-th>
              <mu-th>cookie</mu-th>
            </mu-tr>
          </mu-thead>
          <template v-for="item in items">

            <mu-tbody>
              <mu-tr>
                <router-link :to="{ name:'history',params: {id:item['account_cookie']}}"><mu-td>{{ item['user']}}</mu-td>
                <mu-td >{{ item['strategy']}}</mu-td>
                <mu-td>{{ item['stock_list']}}</mu-td>
                <mu-td >{{ item['start_time']}}</mu-td>
                <mu-td>{{ item['end_time']}}</mu-td>
                <mu-td>{{ item['profit']}}</mu-td>
                <mu-td>{{ item['performace']}}</mu-td>
                
                <mu-td >{{ item['account_cookie']}}</mu-td></router-link>
              </mu-tr>
            </mu-tbody>
           
          </template>

        </mu-table>
    </div>
</template>
<script>

import axios from 'axios'
export default {
  data:function () {
    return {
        height: '450px',
        multiSelectable: true,
        enableSelectAll: false,
        message: 'yutiansut',
        items: [''],
        total: 180,
        current: 1,
        showSizeChanger: true
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
      },
      history(cookie){
         let val = cookie
         console.log(val)
        axios.get('http://localhost:3000/backtest/history?cookie=' + val)
          .then(response => {
            this.items = response.data;
            this.length = this.items.length;
            
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