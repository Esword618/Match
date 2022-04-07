<template>
  <div id="main" style="width: 100%; height: 600px" ref="main"></div>
</template>

<script>
import * as echarts from "echarts";
import http from "@/utils/http";
// import axios from "axios";
export default {
  name: "ConTest",
  mounted() {
    this.MyChart();
  },
  methods: {
    async Data(){
      http.GetData().then((response) => {
          let mydata = response.data.data.info;
          return mydata
          // console.log("数据", data);
        });
    },
    MyChart() {
      // 官方示例 var myChart = echarts.init(document.getElementById('main'));
      const myChart = echarts.init(this.$refs.main); // 我们可以这样写
      //
      const time = (function () {
        // 立即执行函数
        let now = new Date(); // 获得当前的时间
        let res = []; // 存放时间的数组
        let len = 5; // 要存几个时间？
        while (len--) {
          res.unshift(now.toLocaleTimeString().replace(/^\D*/, "")); // 转换时间，大家可以打印出来看一下
          now = new Date(+now - 2000); // 延迟几秒存储一次？
        }
        return res;
      })();
      // const dataOne = (function () {
      //   // 5个随机数，大家可随意定义
      //   let res = [];
      //   let len = 5;
      //   while (len--) {
      //     res.push(Math.round(Math.random() * 1000));
      //   }
      //   return res;
      // })();
      const RawData = (function () {
        let data = [];
        let len = 512;
        http.GetData().then((response) => {
          let mydata = response.data.data.info;
          console.log("-------->", response.data);
          while (len--) {
            data.push(mydata[511 - len]);
          }
          return data;
          // console.log("数据", data);
        });
        // console.log(":______data", data);
        return data;
      })();
      //配置项，可以去查一下官方文档
      let options = {
        title: {
          text: "动态",
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
            data: RawData,
            type: "line",
            name: "测试一",
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
        // dataOne.shift();
        // dataOne.push(Math.round(Math.random() * 1000));
        // console.log(dataOne);
        //很多朋友可能要接后端接口,把数据替换下来既可以了
        // axios.get('你的url').then(res => {
        //   console.log(res)
        // })
        console.log(RawData);
        myChart.setOption({
          xAxis: [
            {
              data: time,
            },
          ],
          series: [
            {
              data: RawData,
              smooth: true,
            },
          ],
        });
      }, 2000);
      myChart.setOption(options);
    },
  },
};
</script>

<style scoped lang="scss"></style>
