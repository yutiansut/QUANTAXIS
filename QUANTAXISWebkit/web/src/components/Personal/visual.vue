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
            data0:this.$route.params.id
        }
    },
    methods:{
      drawline(id){
        this.chart = echarts.init(document.getElementById(id))
        this.chart.setOption({
          title: { text: this.data0},
          tooltip: {},
          xAxis: {
            data:[]
          },
          yAxis: [{
            name:'account',
            max:'dataMax',
            min:'dataMin'

          },{
            name:'market',
            max:'dataMax',
            min:'dataMin'
          }],
          legend: {
              data:['account','market'],
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
          }]
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
                        var time =[]
                        for (var i=1;i<this.items.length;i++){
                          //console.log(this.items[i][0])
                          time.push(this.items[i][0])
                          //this.chart.setOption
                        }
                        //console.log(time)
                        this.chart.setOption({
                          title:{text:code+'--'+strategy_name},
                          series:[{name:'account',data:this.acc,yAxisIndex:0}],
                          xAxis: {
                            data:time
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
                      for (var i=0;i<market.length;i++){
                        //console.log(this.items[i][0])
                        value.push([market[i]['market']['open'],market[i]['market']['high'],market[i]['market']['low'],market[i]['market']['close']])

                        }
                      //console.log(open)
                      this.chart.setOption({
                        series:{
                          name:'market',
                          type:'candlestick',
                          data:value,
                          yAxisIndex:1
                      }
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