<template>
  <div class="chart-box">
    <div
      id="rawdatachart-id"
      style="width: 900px; height: 500px"
      ref="main"
    ></div>
    <div
      id="concentrationdatachart-id"
      style="width: 600px; height: 500px"
      ref="main"
    ></div>
  </div>
</template>
<script>
import { onMounted, ref, reactive } from "vue";
import { message } from "ant-design-vue";
import * as echarts from "echarts";
import http from "@/utils/http";
export default {
  name: "RawDtaChart",
  props: ["isok"],
  setup(props) {
    let RawData = ref();
    const ConcentrationData = reactive({
      on: 1,
      off: 99,
    });
    const MYDATA = () => {
      http
        .GetData()
        .then((response) => {
          let mydata = response.data.data.rawdata;
          let concentrationData = response.data.data.concentrationdata;
          console.log(concentrationData);
          ConcentrationData.on = concentrationData[0];
          ConcentrationData.off = concentrationData[1];
          console.log(ConcentrationData);
          // console.log("-------->", response.data);
          RawData.value = mydata;
          // console.log("数据", data);
        })
        .catch((error) => {
          message.error(error.message);
          // Sleep(1000);
          console.log(error.message);
        });
    };
    const Chart = () => {
      const ConcentrationDataChart = echarts.init(
        document.getElementById("concentrationdatachart-id")
      );
      const RawDataChart = echarts.init(
        document.getElementById("rawdatachart-id")
      );
      const time = (function () {
        // 立即执行函数
        let now = new Date(); // 获得当前的时间
        let res = []; // 存放时间的数组
        let len = 1024; // 要存几个时间？
        while (len--) {
          res.unshift(now.toLocaleTimeString().replace(/^\D*/, "")); // 转换时间，大家可以打印出来看一下
          now = new Date(+now - 2000); // 延迟几秒存储一次？
        }
        return res;
      })();
      //配置项，可以去查一下官方文档
      let ConcentrationDataoptions = {
        title: {
          text: "专注度",
          x: "center",
        },
        series: [
          {
            type: "pie",
            data: [
              {
                value: 1,
                name: "专注度",
              },
              {
                value: 99,
                name: "放松度",
              },
            ],
            radius: "50%",
          },
        ],
      };
      let RawDataoptions = {
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
            data: RawData.value,
            type: "line",
            name: "RawData数据展示",
            smooth: true,
            markLine: {
              data: [{ type: "average", name: "平均值" }],
            },
          },
        ],
      };
      setInterval(() => {
        console.log("------------->>>", props);
        let nowTime = new Date().toLocaleTimeString().replace(/^\D*/, "");
        time.shift();
        time.push(nowTime);
        let IsOk = props.isok;
        if (IsOk) {
          MYDATA();
          console.log("数据：", RawData.value);
        } else {
          RawData.value = [];
          ConcentrationData.on = 1;
          ConcentrationData.off = 99;
        }
        ConcentrationDataChart.setOption({
          series: [
            {
              data: [
                {
                  value: ConcentrationData.on,
                  name: "专注度",
                },
                {
                  value: ConcentrationData.off,
                  name: "放松度",
                },
              ],
            },
          ],
        });
        RawDataChart.setOption({
          xAxis: [
            {
              data: time,
            },
          ],
          series: [
            {
              data: RawData.value,
            },
          ],
        });
      }, 3000);
      ConcentrationDataChart.setOption(ConcentrationDataoptions);
      RawDataChart.setOption(RawDataoptions);
    };
    onMounted(() => {
      Chart();
    });
    return {
      MYDATA,
      RawData,
      ConcentrationData,
      Chart,
    };
  },
};
</script>
<style scoped lang="scss">
.chart-box {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
}
</style>
