import axios from "axios";

// 创建 axios 对象
const request = axios.create({
  baseURL: "http://127.0.0.1:8000",
  timeout: 5 * 1000,
});

export default request;
