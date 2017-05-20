<template>

    <div>
        <h1>实盘监控</h1>
        <li><input  v-on:keyup.enter="querybyname($event.currentTarget.value)" placeholder="需要监控的股票代码:" lazy></li>
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
                data0:'monitor'
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
                    grid: {
                        x: '5%',
                        y: '15%',
                        // x2:300,
                        // y2:400,
                        borderWidth: 1
                    },
                    toolbox: {
                        show: true,
                        feature: {
                            dataZoom: {
                                yAxisIndex: 'none'
                            },
                            dataView: { readOnly: false },
                            restore: {},
                            saveAsImage: {}
                        }
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
                    }, ],
                    yAxis: [{
                        name: 'price',
                        max: 'dataMax',
                        min: 'dataMin'

                    }],
                    legend: {
                        data: [
                            {
                                name: 'market'
                            }
                        ],
                        //data:['k_line'],
                        x: 'left',
                        top: '5%'
                    },
                    dataZoom: [{
                        show: true,
                        realtime: true,
                        start: 0,
                        end: 100
                    },
                    {
                        type: 'inside',
                        realtime: true,
                        start: 0,
                        end: 100
                    }
                    ],
                    series: [
                    {
                        name: 'market',
                        type: 'candlestick',
                        data: []
                    }]
                })
            },
            querybyname(code) {
                let val = 'http://localhost:3000/monitor/code?name=' + code
                axios.get(val)
                    .then( response => {
                        this.chart.hideLoading();
                        //console.log(response.data['record'][0]);
                        var data1 = response.data['record'];
                        var kline=[]
                        var k_time=[]
                        for (var i=0;i<data1.length;i++){
                            var temp_day=[]
                            temp_day.push(parseFloat(data1[i][1]))
                            temp_day.push(parseFloat(data1[i][3]))
                            temp_day.push(parseFloat(data1[i][4]))
                            temp_day.push(parseFloat(data1[i][2]))
                            kline.push(temp_day)
                            k_time.push(data1[i][0])
                        }

                        
                        console.log(kline)


                        this.chart.setOption({
                            
                        series:{
                            name: 'market',
                            type: 'candlestick',
                            data: kline,
                            

                        },
                        xAxis: {
                            data: k_time
                        }
                    })
                    })
                    .catch(function (error) {
                        console.log(error);
                    });
            }
        },
        mounted() {
        this.$nextTick(function () {
            this.drawline('main');
            
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