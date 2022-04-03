<template>
  <a-layout class="layout">
    <!-- 头部 -->
    <a-layout-header class="layout-header">
      <div class="title">智能设备可视化界面</div>
    </a-layout-header>
    <!-- 主体 -->
    <a-layout-content class="layout-content" :style="{ height: contentHeight }">
      <img
        class="eeg"
        src="https://zos.alipayobjects.com/rmsportal/jkjgkEfvpUPVyRjUImniVslZfWPnJuuZ.png"
      />
      <div class="data">后端数据实时展示</div>
      <!-- 这里是开关 -->
      <a-switch
        class="switch"
        @click="Test"
        v-model:checked="checked1"
        checked-children="开"
        un-checked-children="关"
      />
    </a-layout-content>
    <!-- 脚部 -->
    <a-layout-footer class="layout-footer">XXX by XXX</a-layout-footer>
  </a-layout>
</template>

<script>
import http from "@/utils/http";
import { ref, computed, toRefs, reactive } from "vue";
// import { message } from 'ant-design-vue';
export default {
  name: "HomeView",
  setup() {
    let closeBool = ref(false);
    // 计算主体高度
    const contentHeight = computed(() => {
      const height = document.body.scrollHeight;
      return height - 64 - 70 + "px";
    });

    const state = reactive({
      checked1: false,
    });

    const Test = () => {
      http
        .Test()
        .then((response) => {
          console.log(response.data);
        })
        .catch((error) => {
          console.log(error);
        });
    };

    

    return {
      ...toRefs(state),
      closeBool,
      contentHeight,
      Test,
    };
  },
};
</script>

<style scoped lang="scss">
.layout {
  .layout-header {
    //  :style="{ position: 'fixed', zIndex: 1, width: '100%' }"
    position: fixed;
    z-index: 1;
    width: 100%;
    .title {
      font-weight: bold;
      color: #10aabe;
      // font-background:rgb(192, 82, 82);
      // background: rgb(54, 71, 224);
      float: left;
    }
  }
  .layout-content {
    // :style="{ padding: '0 50px', marginTop: '64px',height:'100vh',overflow: 'auto' }"
    padding: 0 50px;
    margin-top: 64px;
    // height: 100vh;
    // overflow: auto;
    .eeg {
      margin-top: 20px;
      float: left;
      width: 450px;
      height: 450px;
    }
    .data {
      margin-top: 20px;
      float: auto;
      // width: 100px;
      height: 50px;
      // background: #10aabe;
      font-size: 40px;
    }
    .switch {
      margin-top: 20px;
      float: right;
    }
  }
  .layout-footer {
    text-align: center;
  }
}
</style>
