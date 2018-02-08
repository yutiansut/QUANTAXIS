<template>
  <div>
      <h2 align="left">>TrainGame</h2>
      

      <div id="main">
        </div>


  </div>
</template>
<script>
import echarts from "echarts";

import axios from "axios";
// 绘制图表
export default {
  data() {
    return {
      title: "000001",
      chart: null,
      time: [],
      toast: false
    };
  },
  methods: {
    drawline(id) {
      this.chart = echarts.init(document.getElementById(id));

      this.chart.setOption({
        title: {
          text: this.title
        },
        grid: {
          x: "5%",
          y: "15%",
          borderWidth: 1
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: "none"
            },
            // dataView: { readOnly: false },
            restore: {},
            saveAsImage: {}
          }
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross"
          }
        },
        xAxis: [
          {
            data: [],
            scale: true
          }
        ],
        yAxis: [
          {
            name: "price",
            max: "dataMax",
            min: "dataMin"
          }
        ],
        legend: {
          data: [
            {
              name: "market"
            }
          ],
          x: "left",
          top: "5%"
        },
        dataZoom: [
          {
            show: true,
            realtime: true,
            start:90,
            end: 100
          },
          {
            type: "inside",
            realtime: true,
            start: 90,
            end: 100
          }
        ],
        series: [
          {
            name: "market",
            type: "candlestick",
            data: []
          }
        ]
      });
    },
    get_data(code, start, end) {
      axios
        .get(
          "http://localhost:3000/stock/history/time?code=000001&start=2017-01-01&end=2018-02-08"
        )
        .then(response => {
          var date = new Date()
          console.log(string(date))
          var market_data = response.data;
          var kline = [];
          var k_time = [];
          for (var i = 0; i < market_data.length; i++) {
            var temp_day = [];
            temp_day.push(parseFloat(market_data[i]["open"]));
            temp_day.push(parseFloat(market_data[i]["close"]));
            temp_day.push(parseFloat(market_data[i]["low"]));
            temp_day.push(parseFloat(market_data[i]["high"]));
            kline.push(temp_day);
            k_time.push(market_data[i]['date']);
          }
          this.chart.setOption({
            title: {
              text: "data"
            },

            series: {
              name: "market",
              type: "candlestick",
              data: kline
            },
            xAxis: {
              data: k_time
            }
          });
        });
    }
  },

  mounted() {
    this.$nextTick(function() {
      this.drawline("main");
      this.get_data("000001", "2018-01-01", "2018-02-02");
    });
  }
};
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
