<template>
  <div class="main_content">
    <div class="container">
      <router-link :to="{name:'history',params: {id:this.data0}}">
        <mu-raised-button v-on:click='query()' label="成交明细" class="demo-raised-button" primary/>
      </router-link>
      <mu-raised-button v-on:click='ready()' label="行情数据" class="demo-raised-button" secondary/>
      <mu-raised-button v-on:click='query_market();query()' label="刷新图像" class="demo-raised-button" />
      <mu-divider />
    </div>
    <div>
      <mu-table>
        <mu-th>code</mu-th>
        <mu-th>alpha</mu-th>
        <mu-th>beta</mu-th>
        <mu-th>sharpe</mu-th>
        <mu-th>最大回撤</mu-th> 
        <mu-th>持续期</mu-th>
        <mu-tbody>
          <mu-td>{{info['code']}}</mu-td>
          <mu-td>{{info['alpha']}}</mu-td>
          <mu-td>{{info['beta']}}</mu-td>
          <mu-td>{{info['sharpe']}}</mu-td>
          <mu-td>{{info['max_drop']}}</mu-td>
          <mu-td>{{info['exist']}}</mu-td>
        </mu-tbody>
      </mu-table>
      <mu-table>
        <mu-th>年化收益</mu-th>
        <mu-th>波动率</mu-th>
        <mu-th>Benchmark年化收益</mu-th>
        <mu-th>Benchmark波动率</mu-th>
        <mu-th>总收益</mu-th>
        <mu-tbody>
          <mu-td>{{info['annualized_returns']}}</mu-td>
          <mu-td>{{info['vol']}}</mu-td>
          <mu-td>{{info['benchmark_annualized_returns']}}</mu-td>
          <mu-td>{{info['benchmark_vol']}}</mu-td>
          <mu-td>{{info['total_returns']}}</mu-td>

        </mu-tbody>
        
      </mu-table>
      
    </div>
    <div id="main"></div>
  </div>
</template>
<script>
  import echarts from 'echarts'
  // 基于准备好的dom，初始化echarts实例
  import axios from 'axios'
  // 绘制图表
  export default {
    data() {
      return {
        chart: null,
        data0: this.$route.params.id,
        time: [],
        info:{}
      }
    },
    methods: {
      drawline(id) {
        this.chart = echarts.init(document.getElementById(id))
        this.chart.showLoading();
        this.chart.setOption({
          title: {
            text: this.data0
          },
          tooltip: {
            trigger: 'axis',
            axisPointer: {
              type: 'cross'
            }
          },
          xAxis: [{

            data: [],
            scale: true
          }, {
            data: [],
            scale: true,


            //boundaryGap : false,
            //axisLine: {onZero: true}
          }],
          yAxis: [{
            name: 'price',
            max: 'dataMax',
            min: 'dataMin'
          }, {
            name: 'account',
            max: 'dataMax',
            min: 'dataMin'

          }],
          legend: {
            data: ['k_line', 'account', 'market', 'bid_sell', 'bid_buy'],
            //data:['k_line'],
            x: 'right'
          },
          dataZoom: [{
              show: true,
              realtime: true,
              start: 65,
              end: 85
            },
            {
              type: 'inside',
              realtime: true,
              start: 65,
              end: 85
            }
          ],
          series: [{
            name: 'account',
            type: 'line',
            data: []

          }, {
            name: 'market',
            type: 'candlestick',
            data: []
          }, {
            name: 'bid_buy',
            type: 'scatter',
            data: [],
            itemStyle: {
              normal: {
                color: "#980000"
              }
            }

          }, {
            name: 'bid_sell',
            type: 'scatter',
            data: [],
            itemStyle: {
              normal: {
                color: "#2f4554"
              }
            }

          }, {
            name: 'k_line',
            type: 'candlestick',
            data: []
          }],
          color: '#2f4554'
        })
      },
      ready() {
        //先从ready拿到信息数据
        let val = this.data0
        axios.get('http://localhost:3000/backtest/info_cookie?cookie=' + val)
          .then(response => {
            var data = response.data;
            var start_time = data['start_time']
            var end_time = data['end_time']
            var profit = data['total_returns']
            this.info['alpha']=data['alpha'].toFixed(3)
            this.info['beta']=data['beta'].toFixed(4)
            this.info['max_drop']=data['max_drop'].toFixed(3)
            this.info['code']=data['stock_list'][0]
            this.info['sharpe']=data['sharpe'].toFixed(3)
            this.info['vol']=data['vol'].toFixed(3)
            this.info['annualized_returns']=data['annualized_returns'].toFixed(3)
            this.info['benchmark_annualized_returns']=data['benchmark_annualized_returns'].toFixed(3)
            this.info['benchmark_vol']=data['benchmark_vol'].toFixed(3)
            this.info['exist']=data['exist']
            this.info['total_returns']=data['total_returns'].toFixed(2)
            console.log(this.info)
            var code = data['stock_list'][0]
            var val = code + '&start=' + start_time + '&end=' + end_time
            //console.log(val)
            var kline = [];
            var kline_date = [];
            //http://localhost:3000/stock/history/time?code=600010&feq=day&start=2015-01-05&end=2015-01-29
            axios.get('http://localhost:3000/stock/history/time?code=' + val)
              .then(response => {

                var history_data = response.data;
                for (var i = 0; i < history_data.length - 1; i++) {
                  kline_date.push(history_data[i]['date']);
                  var temp = [];
                  temp.push(history_data[i]['open'])
                  temp.push(history_data[i]['high'])
                  temp.push(history_data[i]['low'])
                  temp.push(history_data[i]['close'])

                  kline.push(temp);
                }
                this.time = kline_date
                //console.log(kline_date)
                //console.log(kline)
                this.chart.setOption({
                  title: {
                    text: code
                  },
                  series: {
                    name: 'k_line',
                    type: 'candlestick',
                    data: kline,

                  },
                  xAxis: {
                    name: 'k_line',
                    data: kline_date,
                  },
                  yAxisIndex: 0
                })
              })
          })
      },
      query() {
        //console.log(this.data0)
        let val = this.data0
        //console.log(val)
        axios.get('http://localhost:3000/backtest/history?cookie=' + val)
          .then(response => {

            this.items = response.data['history'];
            this.acc = response.data['assest_history'].slice(1);
            var code = response.data['bid']['code'];
            var strategy_name = response.data['strategy']
            //console.log(code)
            // console.log(this.acc)
            this.length = this.acc.length;
            var market_time = [];
            for (var i = 1; i < this.items.length; i++) {
              //console.log(this.items[i][0])
              market_time.push(this.items[i][0])
              //this.chart.setOption
            }

            //console.log(this.time)
            for (var i = 0; i < this.time.length; i++) {
              if (market_time.indexOf(this.time[i]) == -1) {
                market_time.splice(i, 0, this.time[i])
                this.acc.splice(i, 0, this.acc[i - 1])
                //console.log()
              }

            }
            //console.log(this.acc)
            //console.log(market_time)
            this.chart.setOption({
              title: {
                text: code + '--' + strategy_name
              },
              series: [{
                name: 'account',
                type: 'line',
                data: this.acc,
                yAxisIndex: 1
              }],
              xAxis: {
                data: market_time,
                zlevel: 1,
                gridIndex: 0,
              }
            })
          })
          .catch(function (error) {
            console.log(error);
          });


      },
      query_market() {
        //console.log(this.data0)
        let val = this.data0
        //console.log(val)
        axios.get('http://localhost:3000/backtest/market?cookie=' + val)
          .then(response => {
            this.chart.hideLoading();
            var market = response.data;
            //console.log(market)
            var value = [];
            var bid_buy = [];
            var bid_sell = [];
            var bid_buy_date = [];
            var bid_sell_date = [];

            var start_time = market[0]['bid']['time'];
            var end_time = market[market.length - 1]['bid']['time']


            for (var i = 0; i < market.length - 1; i++) {
              //console.log(this.items[i][0])
              value.push([market[i]['market']['open'], market[i]['market']['high'], market[i]['market']['low'],
                market[i]['market']['close']
              ])
              if (market[i]['bid']['towards'] == 1) {
                bid_buy.push(market[i]['bid']['price']);
                bid_buy_date.push(market[i]['bid']['time']);
                bid_sell.push('');
                bid_sell_date.push('');
              } else {
                bid_buy.push('');
                bid_buy_date.push('');
                bid_sell.push(market[i]['bid']['price']);
                bid_sell_date.push(market[i]['bid']['time']);
              }

            }
            for (var i = 0; i < this.time.length; i++) {
              if (bid_buy_date.indexOf(this.time[i]) == -1 && bid_sell_date.indexOf(this.time[i]) == -1) {
                bid_buy_date.splice(i, 0, '')
                bid_buy.splice(i, 0, '')
                bid_sell_date.splice(i, 0, '')
                bid_sell.splice(i, 0, '')
                value.splice(i, 0, '')
                //console.log()
              }

            }
            //console.log(value)
            this.chart.setOption({
              series: [{
                name: 'market',
                type: 'candlestick',
                data: value,
                yAxisIndex: 0,
                gridIndex: 0
              }, {
                name: 'bid_buy',
                type: 'scatter',
                data: bid_buy,
                xAxis: {
                  data: bid_buy_date,
                  zlevel: 2,
                  type: 'category'
                },
                yAxisIndex: 0,
                gridIndex: 0

              }, {
                name: 'bid_sell',
                type: 'scatter',
                data: bid_sell,
                xAxis: {
                  data: bid_sell_date,
                  zlevel: 2,
                  type: 'category'
                },
                yAxisIndex: 0,
                gridIndex: 0,

              }]
            })
            //this.chart.setOption
          })
      }

    },
    mounted() {
      this.$nextTick(function () {
        this.drawline('main');
        this.ready();
        this.query();
        this.query_market();
      })
    }
  }
</script>
<style>
  #main {
    position: relative;
    left: 0;
    margin-left: 0px;
    margin-bottom: 0px;
    width: 800px;
    height: 600px;
    border-radius: 10px;
  }

  #but {
    width: 100px;
    height: 50px;
  }

  .container {
    display: flex;
    flex-wrap: wrap;
  }
</style>