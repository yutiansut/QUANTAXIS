<template>
  <div class="main_content">
    <button id='but' v-on:click='query()'>refresh</button>
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
          yAxis: {
           
          },
          series: [{
              name: 'acc',
              type: 'line',
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
                        console.log(code)
                        //console.log(this.acc)
                        this.length = this.acc.length;
                        var time =[]
                        for (var i=1;i<this.items.length;i++){
                          //console.log(this.items[i][0])
                          time.push(this.items[i][0])
                          //this.chart.setOption
                        }
                        //console.log(time)
                        this.chart.setOption({
                          title:{text:code},
                          series:[{data:this.acc}],
                          xAxis: {
                            data:time
                          }
                        })
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
                  

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
</style>