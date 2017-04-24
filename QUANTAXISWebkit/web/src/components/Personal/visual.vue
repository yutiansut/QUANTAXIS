<template>
  <div class="main_content">
    <div class="container">
    <router-link :to="{ name:'history',params: {id:this.data0}}"><mu-raised-button v-on:click='query()' label="成交明细" class="demo-raised-button" primary/></router-link>
    <mu-raised-button v-on:click='query_market()' label="行情数据" class="demo-raised-button"secondary/>
    <mu-raised-button v-on:click='query()' label="刷新图像" class="demo-raised-button"/>
     <mu-divider />
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
    data(){
        return{
            chart:null,
            data0:this.$route.params.id,
            time:[]
        }
    },
    methods:{
      drawline(id){
        this.chart = echarts.init(document.getElementById(id))
        this.chart.setOption({
          title: { text: this.data0},
          tooltip: {
              trigger: 'axis',
              axisPointer: {
                  type: 'cross'
              }
          },
          xAxis: [{
            data:this.time,
            scale:true
          },{
            data:[],
            scale:true
          }],
          yAxis: [{
              name:'account',
              max:'dataMax',
              min:'dataMin'

            },{
              name:'market',

            },{
              name:'bid_buy',

            },{
              name:'bid_sell',

            }
          ],
          legend: {
              data:['account','market','bid_sell','bid_buy'],
              x: 'right'
          },
          dataZoom: [
              {
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
              data:[]
          },{
            name:'market',
            type:'candlestick',
            data:[]
          },{
            name:'bid_buy',
            type:'scatter',
            data:[]
          },{
            name:'bid_sell',
            type:'scatter',
            data:[]
          }
          ]
        })
      },
      query() {
            console.log(this.data0)
            let val =this.data0
            console.log(val)
            axios.get('http://localhost:3000/backtest/history?cookie='+val)
                    .then(response => {
                        this.items = response.data['history'];
                        this.acc=response.data['assest_history'];
                        var code=response.data['bid']['code'];
                        var strategy_name=response.data['strategy']
                        //console.log(code)
                       // console.log(this.acc)
                        this.length = this.acc.length;
                        var market_time=[];
                        for (var i=1;i<this.items.length;i++){
                          //console.log(this.items[i][0])
                          market_time.push(this.items[i][0])
                          //this.chart.setOption
                        }
                        //console.log(time)
                        this.chart.setOption({
                          title:{text:code+'--'+strategy_name},
                          series:[{name:'account',data:this.acc,yAxisIndex:0}],
                          xAxis: {
                            data:market_time,
                            zlevel:1,
                            type:'category'
                          }
                        })
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                  

        },
        query_market(){
            //console.log(this.data0)
            let val =this.data0
            //console.log(val)
            axios.get('http://localhost:3000/backtest/market?cookie='+val)
                    .then(response => {
                      var market = response.data;
                      //console.log(market)
                      var value=[];
                      var bid_buy=[];
                      var bid_sell=[];
                      var bid_buy_date=[];
                      var bid_sell_date=[];
                      /**var kline=[];
                      var kline_date=[];
                      var start_time=market[0]['bid']['time'];
                      var end_time=market[market.length-1]['bid']['time']
                      var val=market[0]['bid']['code']+'&start='+start_time+'&end='+end_time
                      console.log(val)
                      //http://localhost:3000/stock/history/time?code=600010&feq=day&start=2015-01-05&end=2015-01-29
                      axios.get('http://localhost:3000/stock/history/time?code='+val)
                          .then(response => {
                            var history_data = response.data;
                             for (var i=0;i<history_data.length-1;i++){
                                kline_date.push(history_data[i]['date']);
                                var temp=[];
                                temp.push(history_data[i]['open'])
                                temp.push(history_data[i]['high'])
                                temp.push(history_data[i]['low'])
                                temp.push(history_data[i]['close'])
                                
                                kline.push(temp);
                             }
                             this.time=kline_date
                             console.log(kline_date)
                              console.log(kline)
                               this.chart.setOption({
                                    series:{
                                      name:'kline',
                                      type:'candlestick',
                                      data:kline,
                                      xAxis:{
                                        name:'xxx',
                                        data:kline_date,
                                        zlevel:0,
                                        type:'time'
                                        
                                      },
                                      xAxisIndex:0,
                                      yAxisIndex:4
                                  }
                          })
                           }) 
                      */
                      for (var i=0;i<market.length-1;i++){
                        //console.log(this.items[i][0])
                        value.push([market[i]['market']['open'],market[i]['market']['high'],market[i]['market']['low'],market[i]['market']['close']])
                        if (market[i]['bid']['towards']==1){
                          bid_buy.push(market[i]['bid']['price']);
                          bid_buy_date.push(market[i]['bid']['time']);
                          bid_sell.push('');
                          bid_sell_date.push('');
                          }
                        else{
                          bid_buy.push('');
                          bid_buy_date.push('');
                          bid_sell.push(market[i]['bid']['price']);
                          bid_sell_date.push(market[i]['bid']['time']);
                        }
                        
                        }
                      //console.log(bid_buy_date)
                      this.chart.setOption({
                        series:[{
                          name:'market',
                          type:'candlestick',
                          data:value,
                          yAxisIndex:4
                      },{
                          name:'bid_buy',
                          type:'scatter',
                          data:bid_buy,
                          xAxis:{data:bid_buy_date,zlevel:2, type:'category'},
                          yAxisIndex:2

                      },{
                          name:'bid_sell',
                          type:'scatter',
                          data:bid_sell,
                          xAxis:{data:bid_sell_date,zlevel:2, type:'category'},
                          yAxisIndex:2
                      }
                      ]
                      })
                          //this.chart.setOption
                    })
        }
        
    },
        mounted() {
      this.$nextTick(function() {
          this.drawline('main')
        
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
#but{
    width:100px;
    height:50px;
}
.container{
  display: flex;
  flex-wrap: wrap;
}
</style>