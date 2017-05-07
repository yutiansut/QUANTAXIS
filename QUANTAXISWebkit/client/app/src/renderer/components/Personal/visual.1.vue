<template>
    <div class="main_content">
        <h1></h1>
        <li><input v-on:keyup.enter="query($event.currentTarget.value)"></li>
        <div id="main"></div>
        
    </div>
</template>
<script>
import axios from 'axios'
var data0={};
import echarts from 'echarts'

export default {
    data(){
        return{
            chart:null,
            data0:data0,
            titled:'上证指数'
        }
    },
    methods:{
        drawKline(id){
            console.log(this.data0)
                this.chart = echarts.init(document.getElementById(id))
                this.chart.setOption({
                    title: {
                        text: this.titled,
                        left: 0
                    },
                    tooltip: {
                        trigger: 'axis',
                        axisPointer: {
                            type: 'line'
                        }
                    },
                    legend: {
                        data: ['日K', 'MA5', 'MA10', 'MA20', 'MA30']
                    },
                    grid: {
                        left: '10%',
                        right: '10%',
                        bottom: '15%'
                    },
                    xAxis: {
                        type: 'category',
                        data: this.data0.categoryData,
                        scale: true,
                        boundaryGap : false,
                        axisLine: {onZero: false},
                        splitLine: {show: false},
                        splitNumber: 20,
                        min: 'dataMin',
                        max: 'dataMax'
                    },
                    yAxis: {
                        scale: true,
                        splitArea: {
                            show: true
                        }
                    },
                    dataZoom: [
                        {
                            type: 'inside',
                            start: 50,
                            end: 100
                        },
                        {
                            show: true,
                            type: 'slider',
                            y: '90%',
                            start: 50,
                            end: 100
                        }
                    ],
                    series: [
            {
                name: '日K',
                type: 'candlestick',
                data: this.data0.values,
                markPoint: {
                    label: {
                        normal: {
                            formatter: function (param) {
                                return param != null ? Math.round(param.value) : '';
                            }
                        }
                    },
                    data: [
                        {
                            name: 'XX标点',
                            coord: ['2013/5/31', 2300],
                            value: 2300,
                            itemStyle: {
                                normal: {color: 'rgb(41,60,85)'}
                            }
                        },
                        {
                            name: 'highest value',
                            type: 'max',
                            valueDim: 'highest'
                        },
                        {
                            name: 'lowest value',
                            type: 'min',
                            valueDim: 'lowest'
                        },
                        {
                            name: 'average value on close',
                            type: 'average',
                            valueDim: 'close'
                        }
                        ],
                        tooltip: {
                            formatter: function (param) {
                                return param.name + '<br>' + (param.data.coord || '');
                            }
                        }
                        },
                        markLine: {
                            symbol: ['none', 'none'],
                            data: [
                                [
                                    {
                                        name: 'from lowest to highest',
                                        type: 'min',
                                        valueDim: 'lowest',
                                        symbol: 'circle',
                                        symbolSize: 10,
                                        label: {
                                            normal: {show: false},
                                            emphasis: {show: false}
                                        }
                                    },
                                    {
                                        type: 'max',
                                        valueDim: 'highest',
                                        symbol: 'circle',
                                        symbolSize: 10,
                                        label: {
                                            normal: {show: false},
                                            emphasis: {show: false}
                                        }
                                    }
                                ],
                                {
                                    name: 'min line on close',
                                    type: 'min',
                                    valueDim: 'close'
                                },
                                {
                                    name: 'max line on close',
                                    type: 'max',
                                    valueDim: 'close'
                                }
                                ]
                            }
                        },
                        {
                            name: 'MA5',
                            type: 'line',
                            data: this.calculateMA(5),
                            smooth: true,
                            lineStyle: {
                                normal: {opacity: 0.5}
                            }
                        },
                        {
                            name: 'MA10',
                            type: 'line',
                            data: this.calculateMA(10),
                            smooth: true,
                            lineStyle: {
                                normal: {opacity: 0.5}
                            }
                        },
                        {
                            name: 'MA20',
                            type: 'line',
                            data: this.calculateMA(20),
                            smooth: true,
                            lineStyle: {
                                normal: {opacity: 0.5}
                            }
                        },
                        {
                            name: 'MA30',
                            type: 'line',
                            data: this.calculateMA(30),
                            smooth: true,
                            lineStyle: {
                                normal: {opacity: 0.5}
                            }
                        },

                        ]
                    })
                    

        },
        splitData(rawData) {
            var categoryData = [];
            var values = []
            
            for (var i = 0; i < rawData.length; i++) {

                categoryData.push(rawData[i].splice(0, 1)[0]);
                values.push(rawData[i])

            }
            return {
                categoryData: categoryData,
                values: values
                
            };
        },
        calculateMA(dayCount) {
            var result = [];
            for (var i = 0, len = this.data0.values.length; i < len; i++) {
                if (i < dayCount) {
                    result.push('-');
                    continue;
                }
                var sum = 0;
                for (var j = 0; j < dayCount; j++) {
                    sum += this.data0.values[i - j][1];
                }
                result.push(sum / dayCount);
            }
            return result;
        },
        query(code){

            var queryline='http://localhost:3000/stock/history/all?code='+code+'&feq=day'
            axios.get(queryline)
                .then(function (response) {

                    var dt=response.data;
                    
                    var rawData=[];
                    for (var j=0; j<dt.length;j++){
                        rawData.push(dt[j].slice(0,5));
                    }
                    
                    var categoryData = [];
                    var values = [];
                    for (var i = 0; i < rawData.length; i++) {

                        categoryData.push(rawData[i].splice(0, 1)[0]);
                        var temp=new Array()
                        
                        temp[0]=Number(rawData[i][0]);
                        temp[1]=Number(rawData[i][1]);
                        temp[2]=Number(rawData[i][2]);
                        temp[3]=Number(rawData[i][3]);


                        values.push(temp)

                    }

                    console.log(data0)

                    data0.values=values;
                    data0.categoryData=categoryData;
                    console.log(data0)
                    
                    })
                .catch(function (error) {
                    console.log(error);
                    });
            this.drawKline('main')
        }
    },
    mounted() {
      this.$nextTick(function() {
          this.drawKline('main')
        
      })
    }
}
/**
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
   */
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
