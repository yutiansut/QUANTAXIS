<template>
  <div id="index">
    <div id="logo">
      <mu-list>
        <h2 align='left'>> Hi! {{itemd.user}}</h2>
      </mu-list>
    </div>

    <div id="personal-content">
      <ul>
        <h3>回测概览</h3>
        <mu-table :height="height">


            <mu-thead  slot="header">
              <mu-tr>
                <mu-th>strategy</mu-th>
                <mu-th>start</mu-th>
                <mu-th>end</mu-th>
                <mu-th>annualized_returns</mu-th>
              </mu-tr>
            </mu-thead>
            <template v-for="item in items">
            <mu-tbody>

              <mu-tr>

                  <mu-td><router-link :to="{ name:'history',params: {id:item['account_cookie']}}">{{ item['strategy']}}</router-link></mu-td>
                  <mu-td>{{ item['start_time']}}</mu-td>
                  <mu-td>{{ item['end_time']}}</mu-td>
                  <mu-td>{{ item['annualized_returns']}}</mu-td>

              </mu-tr>
            </mu-tbody>

          </template>

        </mu-table>
        <h3>NOTEBOOK</h3>
        <mu-table multiSelectable enableSelectAll ref="table">
          <mu-thead>
            <mu-tr>
              <mu-th>title</mu-th>
              <mu-th>content</mu-th>
            </mu-tr>
          </mu-thead>
          <template v-for="item in itema">
            <mu-tbody style="vertical-align:left">
              <mu-tr>
                <!--<router-link :to="{ name:'markdown',params: {id:item['_id']}}"></router-link>-->
                  <mu-td><router-link :to="{ name:'markdown',params: {id:item['_id']}}">{{item['title']}}</router-link></mu-td>
                  <mu-td>{{item['content'].substr(0,60)}}</mu-td>
               <!-- </router-link>-->
              </mu-tr>

            </mu-tbody>
          </template>
        </mu-table>

      </ul>
    </div>
  </div>
</template>
<script>
  import axios from 'axios'
  export default {
    data() {
      return {
        itemd: {
          user: sessionStorage.user
        },
        items: [''],
        itema: ['']

      }
    },
    methods: {
      query() {

        axios.get('http://localhost:3000/notebook/queryall')
          .then(response => {
            this.itema = response.data;
          })
          .catch(function (error) {

          });
      },

      ready() {

        axios.get('http://localhost:3000/backtest/info?name=' + sessionStorage.user)
          .then(response => {
            this.items = response.data;

            this.length = this.items.length;
            var performance = response.data[0]['performance'];

          })
          .catch(function (error) {

          });
      }
    },

    mounted() {
      this.$nextTick(function () {
        this.ready();
        this.query();

      })
    }
  }

</script>
<style lang="css">
  #logo {
    width: 20%;
    height: 20%;
  }

  .mu-item {
    font-size: 2em;
  }

  #personal-content {
    margin-top: 2%;
  }

  li {
    float: left;
  }

  h3 {
    float: left;
  }

  tbody {
    vertical-align: left;
  }

  a {
    text-align: left;
  }

  .demo-table-settings{
  width: 200px;
  overflow: hidden;
  margin: 20px auto 0px;
}
</style>
