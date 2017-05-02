<template>
        <div class="container">
                <div class="demo-infinite-container">

                        <mu-list>
                                <template v-for="item in list">
                                        <mu-list-item :title="item[0]" v-on:click='ready(item);get_info(item)' />
                                        <mu-divider/>
                                </template>
                        </mu-list>
                        <mu-infinite-scroll :scroller="scroller" :loading="loading" @load="querys()" />


                </div>
                <div id='table'>
                        <mu-table :height='height' :selectable="selectable" :showCheckbox="showCheckbox">
                                <mu-thead>
                                        <mu-tr>
                                                <th>回测概览</th>
                                        </mu-tr>
                                </mu-thead>

                                <mu-tbody>
                                        <mu-tr>
                                                <mu-td>{{ itemss['start_time']}}</mu-td>
                                                <mu-td>{{ itemss['end_time']}}</mu-td>
                                                <mu-td>{{ itemss['profit']}}</mu-td>


                                        </mu-tr>

                                </mu-tbody>
                                <mu-thead>
                                        <mu-tr>
                                                <th>交易历史</th>
                                        </mu-tr>
                                </mu-thead>
                                <template v-for="item in items">
                                        <mu-tbody>
                                                <mu-tr>
                                                        <mu-td>{{item[0]}}</mu-td>
                                                        <mu-td>{{item[1]}}</mu-td>
                                                        <mu-td>{{item[2]}}</mu-td>
                                                        <mu-td>{{item[3]}}</mu-td>
                                                        <mu-td>{{item[4]}}</mu-td>

                                                </mu-tr>
                                        </mu-tbody>
                                </template>

                        </mu-table>
                </div>
                <div id='main'></div>
        </div>
</template>
<script>
import echarts from 'echarts'
// 基于准备好的dom，初始化echarts实例
import axios from 'axios'
export default {
        data() {
                return {
                        height: '300px',

                        $el: '.demo-infinite-container',
                        chart: null,
                        data0: this.$route.params.id,
                        time: [],
                        list: [
                                ['Strategy_List', 'cookie']
                        ],
                        showCheckbox: false,
                        selectable: false,
                        items: [],
                        itemss: [],
                        num: 10,
                        loading: false,
                        scroller: null
                }
        },

        methods: {
                querys() {
                        axios.get('http://localhost:3000/backtest/info_all')
                                .then(response => {
                                        var info = response.data;

                                        for (var i = 0; i < info.length; i++) {
                                                this.list.push([info[i]['stock_list'][0] + '-' + info[i]
                                                        ['strategy'], info[i][
                                                                'account_cookie'
                                                        ]
                                                ])
                                        }


                                })
                                .catch(function (error) {
                                        console.log(error);
                                });
                },
                drawline(id) {
                        this.chart = echarts.init(document.getElementById(id))
                        this.chart.showLoading();
                        this.chart.setOption({
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

                                color: '#2f4554'
                        })
                },
                ready(message) {
                        //先从ready拿到信息数据
                        let val = message[1]
                        
                                
                        var legend = {
                                data: ['k_line'+val, 'account'+val, 'market'+val, 'bid_sell'+val,
                                        'bid_buy'+val
                                ],
                                //data:['k_line'],
                                x: 'right'
                        }
                        var legend_data=legend['data'].push(['k_line'+val, 'account'+val, 'market'+val, 'bid_sell'+val,'bid_buy'+val])
                        var legend = {
                                data: legend_data,
                                //data:['k_line'],
                                x: 'right'
                        }
                        var xAxis=[]
                        axios.get('http://localhost:3000/backtest/info_cookie?cookie=' + val)
                                .then(response => {
                                        var data = response.data;

                                        var start_time = data['start_time']
                                        var end_time = data['end_time']
                                        
                                        
                                        var code = data['stock_list'][0]
                                        var vals = code + '&start=' + start_time + '&end=' + end_time
                                        //console.log(val)
                                        var kline = [];
                                        var kline_date = [];

                                        
                                        this.chart.setOption({
                                                legend:this.legend,
                                                series: [{
                                                name: 'account'+val,
                                                type: 'line',
                                                data: []
                                        }, {
                                                name: 'market'+val,
                                                type: 'candlestick',
                                                data: []
                                        }, {
                                                name: 'bid_buy'+val,
                                                type: 'scatter',
                                                data: [],
                                                itemStyle: {
                                                        normal: {
                                                                color: "#980000"
                                                        }
                                                }
                                        }, {
                                                name: 'bid_sell'+val,
                                                type: 'scatter',
                                                data: [],
                                                itemStyle: {
                                                        normal: {
                                                                color: "#2f4554"
                                                        }
                                                }
                                        }, {
                                                name: 'k_line'+val,
                                                type: 'candlestick',
                                                data: []
                                        }]
                                        },{notMerge:false, lazyUpdate:true})
                                        //http://localhost:3000/stock/history/time?code=600010&feq=day&start=2015-01-05&end=2015-01-29
                                        axios.get('http://localhost:3000/stock/history/time?code=' +vals)
                                                .then(response => {
                                                        console.log(val)
                                                        var history_data = response.data;
                                                        for (var i = 0; i < history_data.length -
                                                                1; i++) {
                                                                kline_date.push(history_data[i]
                                                                        ['date']);
                                                                var temp = [];
                                                                temp.push(history_data[i][
                                                                        'open'
                                                                ])
                                                                temp.push(history_data[i][
                                                                        'close'
                                                                ])
                                                                temp.push(history_data[i]['low'])
                                                                temp.push(history_data[i][
                                                                        'high'
                                                                ])

                                                                kline.push(temp);
                                                        }
                                                        this.time = kline_date
                                                        //console.log(kline_date)
                                                        //console.log(kline)



                                                        this.chart.setOption({
                                                                legend: legend,
                                                                series: {
                                                                        name: 'k_line'+val,
                                                                        type: 'candlestick',
                                                                        data: kline,

                                                                },
                                                                xAxis:{
                                                                        name: 'k_line'+val,
                                                                        data: kline_date,
                                                                },
                                                                yAxisIndex: 0
                                                        })
                                                })
                                        axios.get('http://localhost:3000/backtest/history?cookie=' +val)
                                                .then(response => {
                                                        this.items = response.data['history'];
                                                        this.acc = response.data[
                                                                'assest_history'].slice(
                                                                1);
                                                        var code = response.data['bid']['code'];
                                                        var strategy_name = response.data[
                                                                'strategy']
                                                        //console.log(code)
                                                        // console.log(this.acc)
                                                        this.length = this.acc.length;
                                                        var market_time = [];
                                                        for (var i = 1; i < this.items.length; i++) {
                                                                //console.log(this.items[i][0])
                                                                market_time.push(this.items[i][
                                                                        0
                                                                ])
                                                                //this.chart.setOption
                                                        }

                                                        //console.log(this.time)
                                                        for (var i = 0; i < this.time.length; i++) {
                                                                if (market_time.indexOf(this.time[
                                                                                i]) == -1) {
                                                                        market_time.splice(i, 0,
                                                                                this.time[
                                                                                        i
                                                                                ])
                                                                        this.acc.splice(i, 0,
                                                                                this.acc[
                                                                                        i -
                                                                                        1
                                                                                ])
                                                                        //console.log()
                                                                }

                                                        }
                                                        //console.log(this.acc)
                                                        //console.log(market_time)
                                                        this.chart.setOption({
                                                                title: {
                                                                        text: code +
                                                                                '--' +
                                                                                strategy_name
                                                                },
                                                                series: [{
                                                                        name: 'account'+val,
                                                                        type: 'line',
                                                                        data: this
                                                                                .acc,
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
                                                                value.push([market[i]['market']['open'],
                                                                        market[i]['market']['high'],
                                                                        market[i]['market']['low'],
                                                                        market[i]['market']['close']
                                                                ])
                                                                if (market[i]['bid']['towards'] ==1) {
                                                                        bid_buy.push(market[i]['bid']['price']);
                                                                        bid_buy_date.push(market[i]['bid']['time']);
                                                                        bid_sell.push('');
                                                                        bid_sell_date.push('');
                                                                } else {
                                                                        bid_buy.push('');
                                                                        bid_buy_date.push('');
                                                                        bid_sell.push(market[i]['bid']['price']);
                                                                        bid_sell_date.push(
                                                                                market[i]['bid']['time']
                                                                        );
                                                                }

                                                        }
                                                        for (var i = 0; i < this.time.length; i++) {
                                                                if (bid_buy_date.indexOf(this.time[
                                                                                i]) == -1 &&
                                                                        bid_sell_date.indexOf(
                                                                                this.time[i]) ==
                                                                        -1) {
                                                                        bid_buy_date.splice(i,0, '')
                                                                        bid_buy.splice(i, 0, '')
                                                                        bid_sell_date.splice(i,0, '')
                                                                        bid_sell.splice(i, 0,'')
                                                                        value.splice(i, 0, '')
                                                                        //console.log()
                                                                }

                                                        }
                                                        //console.log(value)
                                                        
                                                        this.chart.setOption({
                                                               
                                                                series:[{
                                                                                name: 'market'+val,
                                                                                type: 'candlestick',
                                                                                data: value,
                                                                                yAxisIndex: 0,
                                                                                gridIndex: 0
                                                                        },
                                                                        {
                                                                                name: 'bid_buy'+val,
                                                                                type: 'scatter',
                                                                                data: bid_buy,
                                                                                xAxis: {
                                                                                        data: bid_buy_date,
                                                                                        zlevel: 2,
                                                                                        type: 'category'
                                                                                },
                                                                                yAxisIndex: 0,
                                                                                gridIndex: 0

                                                                        },
                                                                        {
                                                                                name: 'bid_sell'+val,
                                                                                type: 'scatter',
                                                                                data: bid_sell,
                                                                                xAxis: {
                                                                                        data: bid_sell_date,
                                                                                        zlevel: 2,
                                                                                        type: 'category'
                                                                                },
                                                                                yAxisIndex: 0,
                                                                                gridIndex: 0,

                                                                        }
                                                                ] 
                                                        })
                                                        //this.chart.setOption
                                                })
                                })



                },
                get_info(message) {
                        let val = message[1]
                        axios.get('http://localhost:3000/backtest/info_cookie?cookie=' + val)
                                .then(response => {
                                        this.itemss = response.data;
                                        //console.log(this.itemss)

                                })

                }


        },
        mounted() {
                this.$nextTick(function () {
                        //this.scroller = this.$el
                        this.querys();

                        this.drawline('main');
                })

        },
}
</script>

<style lang="css">
        .demo-infinite-container {
                width: 20%;
                height: 300px;
                overflow: auto;
                -webkit-overflow-scrolling: touch;
                border: 1px solid #d9d9d9;
        }

        #table {
                width: 80%;
        }

        .container {
                display: flex;
                flex-wrap: wrap;
        }
</style>