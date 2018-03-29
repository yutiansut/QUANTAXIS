<template>
  <div>
      <h2 align="left">>TrainGame</h2>
      
      <mu-raised-button v-on:click='new_data()' label="BUY" class="demo-raised-button" secondary/>
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
      toast: false,
      market_data: [],
      show_data: [],
      show_time: [],
      splited_data: [],
      splited_date: []
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
            start: 90,
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
          var market_data = response.data;
          var kline = [];
          var k_time = [];
          var n = 50;
          for (var i = 0; i < market_data.length - n; i++) {
            var temp_day = [];
            temp_day.push(parseFloat(market_data[i]["open"]));
            temp_day.push(parseFloat(market_data[i]["close"]));
            temp_day.push(parseFloat(market_data[i]["low"]));
            temp_day.push(parseFloat(market_data[i]["high"]));

            this.show_data.push(temp_day);
            this.show_time.push(market_data[i]["date"]);
          }
          for (var i = market_data.length - n; i < market_data.length; i++) {
            var temp_day = [];
            temp_day.push(parseFloat(market_data[i]["open"]));
            temp_day.push(parseFloat(market_data[i]["close"]));
            temp_day.push(parseFloat(market_data[i]["low"]));
            temp_day.push(parseFloat(market_data[i]["high"]));

            this.splited_data.push(temp_day);
            this.splited_date.push(market_data[i]["date"]);
          }
          this.chart.setOption({
            title: {
              text: "data"
            },

            series: {
              name: "market",
              type: "candlestick",
              data: this.show_data
            },
            xAxis: {
              data: this.show_time
            }
          });
        });
    },
    new_data() {
      var l1 = this.splited_data.shift();
      var l1_date = this.splited_date.shift();
      this.show_data.push(l1);
      this.show_time.push(l1_date);
      this.chart.setOption({
        title: {
          text: "data"
        },

        series: {
          name: "market",
          type: "candlestick",
          data: this.show_data
        },
        xAxis: {
          data: this.show_time
        }
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
