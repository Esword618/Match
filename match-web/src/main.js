import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";

// 导入 anted
import Antd from "ant-design-vue";
import "ant-design-vue/dist/antd.css";

// 导入axios
import axios from "axios";
import VueAxios from "vue-axios";

const app = createApp(App);
app.use(store).use(router);
app.use(Antd);
app.use(VueAxios, axios);
app.mount("#app");
