<template>
  <div>
      <h2 align="left">>TrainGame</h2>
      
        <div class="container">
        <div id="main">
          </div>
        </div>
      <div>

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
      title:'000001',
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
          // x2:300,
          // y2:400,
          borderWidth: 1
        },
        toolbox: {
          show: true,
          feature: {
            dataZoom: {
              yAxisIndex: "none"
            },
            dataView: {
              readOnly: false
            },
            magicType: {
              type: ["line", "bar"]
            },
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
          },
          {
            data: [],
            scale: true

            //boundaryGap : false,
            //axisLine: {onZero: true}
          }
        ],
        yAxis: [
          {},
          {
            name: "account",
            max: "dataMax",
            min: "dataMin"
          }
        ],
        legend: {
          data: [
            {
              name: "assets"
            },
            {
              name: "benchmark"
            }
          ],
          //data:['k_line'],
          x: "left",
          top: "5%"
        },
        dataZoom: [
          {
            show: true,
            realtime: true,
            start: 0,
            end: 100
          }
        ],
        series: [
          {
            name: "assets",
            type: "line",
            data: [],
            lineStyle: {
              normal: {
                color: "#c23531"
              }
            },
            areaStyle: {
              normal: {
                color: "#c23531",
                opacity: 0.3
              }
            },
            yAxisIndex: 1
          },
          {
            name: "benchmark",
            type: "line",
            data: [],
            lineStyle: {
              normal: {
                color: "#2f4554"
              }
            },
            areaStyle: {
              normal: {
                color: "#2f4554",
                opacity: 0.3
              }
            },
            yAxisIndex: 1
          }
        ]
      });
    }
  },
    get_data(code,start,end){
      data=axios.get()

    },

  mounted() {
    this.$nextTick(function() {
      this.drawline("main");
    });
  }
};
</script>