<template>
    <div class="main_content">
        <h1>Visual</h1>
        <div id="main"></div>
        
    </div>
</template>
<script>
import axios from 'axios'

import echarts from 'echarts'
  export default {
    data() {
      return {
        chart: null,
        opinion: ['学习氛围差', '学习氛围一般', '学习氛围很好'],
        opinionData: [
          {value:26, name:'学习氛围差'},
          {value:31, name:'学习氛围一般'},
          {value:8, name:'学习氛围很好'}
        ]
      }
    },
    methods: {
      drawPie (id) {
        this.chart = echarts.init(document.getElementById(id))
        this.chart.setOption({
          title: {
            text: 'id',
            left: 'center',
            top: 10,
            textStyle: {
              fontSize: 24,
              fontFamily: 'Helvetica',
              fontWeight: 400
            }
          },
          tooltip: {
            trigger: 'item',
            formatte: "{b}: {c} ({d}%)"
          },
          toolbox: {
            feature: {
              saveAsImage: {},
              dataView: {}
            },
            right: 15,
            top: 10
          },
          legend: {
              orient: 'vertical',
              left: 5,
              top: 10,
              data: this.opinion,
          },
          series: [
            {
              name: '寝室学习氛围',
              type: 'pie',
              radius: ['50%', '70%'],
              center: ['50%', '60%'],
              avoidLabelOverlap: false,
              label: {
                emphasis: {
                  show: true,
                  textStyle: {
                    fontSize: '24',
                    fontWeight: 'bold'
                  }
                }
              },
              labelLine: {
                normal: {
                  show: false
                }
              },
              data: this.opinionData,
              itemStyle: {
                emphasis: {
                  shadowBlur: 10,
                  shadowOffset: 0,
                  shadowColor: 'rgba(0, 0, 0, 0.5)'
                }
              }
            }
          ]
        })
      }
    },
    mounted() {
      this.$nextTick(function() {
          this.drawPie('main')
        
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
</style>
