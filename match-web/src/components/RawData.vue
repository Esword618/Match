<template>
  <div id="main" style="width: 600px; height: 500px" ref="main"></div>
</template>
<script>
import { onMounted, ref } from "vue";
import { message } from "ant-design-vue";
import * as echarts from "echarts";
import http from "@/utils/http";
export default {
  name: "RawDtaChart",
  setup() {
    let DATA = ref();
    const MYDATA = () => {
      http
        .GetData()
        .then((response) => {
          let mydata = response.data.data.info;
          // console.log("-------->", response.data);
          DATA.value = mydata;
          // console.log("数据", data);
        })
        .catch((error) => {
          message.error(error.message);
          Sleep(1000);
          console.log(error.message);
        });
    };
    function Sleep(time) {
      return new Promise((resolve) => setTimeout(resolve, time));
    }
    const Chart = () => {
      const myChart = echarts.init(document.getElementById("main"));
      //
      const time = (function () {
        // 立即执行函数
        let now = new Date(); // 获得当前的时间
        let res = []; // 存放时间的数组
        let len = 512; // 要存几个时间？
        while (len--) {
          res.unshift(now.toLocaleTimeString().replace(/^\D*/, "")); // 转换时间，大家可以打印出来看一下
          now = new Date(+now - 2000); // 延迟几秒存储一次？
        }
        return res;
      })();
      //配置项，可以去查一下官方文档
      let options = {
        title: {
          text: "rawdata",
          textStyle: {
            color: "black",
          },
        },
        tooltip: {
          trigger: "axis",
          axisPointer: {
            type: "cross",
            label: {
              backgroundColor: "#283b56",
            },
          },
        },
        legend: {},
        xAxis: {
          type: "category",
          data: time, // 把时间组成的数组接过来，放在x轴上
          boundaryGap: true,
        },
        yAxis: {
          type: "value",
        },
        series: [
          {
            data: DATA.value,
            type: "line",
            name: "RawData数据展示",
            smooth: true,
            markLine: {
              data: [{ type: "average", name: "平均值" }],
            },
          },
        ],
      };
      setInterval(function () {
        let nowTime = new Date().toLocaleTimeString().replace(/^\D*/, "");
        time.shift();
        time.push(nowTime);
        MYDATA();
        console.log("数据：", DATA.value);
        myChart.setOption({
          xAxis: [
            {
              data: time,
            },
          ],
          series: [
            {
              data: DATA.value,
            },
          ],
        });
      }, 3000);
      myChart.setOption(options);
    };
    onMounted(() => {
      Chart();
    });
    return {
      MYDATA,
      DATA,
      Sleep,
      Chart,
    };
  },
};
</script>
<style></style>
