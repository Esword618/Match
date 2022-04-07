<template>
  <div class="map">
    <div id="mychartid" style="width: 300px; height: 400px"></div>
  </div>
</template>

<script>
// import http from "@/utils/http";
import { onMounted } from "vue";
import * as echarts from "echarts";
export default {
  name: "MyEchart",
  setup() {
    const echartInit = () => {
      var myChart = echarts.init(document.getElementById("mychartid"));
      // 指定图表的配置项和数据
      var option = {
        title: {
          text: "rawdata",
        },
        tooltip: {},
        legend: {
          data: ["销量"],
        },
        xAxis: {
          data: ["衬衫", "羊毛衫", "雪纺衫", "裤子", "高跟鞋", "袜子"],
        },
        yAxis: {},
        series: [
          {
            name: "销量",
            type: "bar",
            data: [5, 20, 36, 10, 10, 20],
          },
        ],
      };
      // 使用刚指定的配置项和数据显示图表。
      myChart.setOption(option);
    };

    onMounted(() => {
      echartInit();
    });

    // 开始
    const Data = () => {
      // http
      //   .Start()
      //   .then((response) => {
      //     console.log(response.data);
      //   })
      //   .catch((error) => {
      //     console.log(error);
      //   });
    };
    return {
      Data,
      echartInit,
    };
  },
};
</script>

<style></style>
