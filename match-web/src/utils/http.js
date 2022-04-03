import request from "./httpConfig";
// 如果是post请求需要qs进行一个处理
// import qs from "qs";

// 获取图片
const Start = () => {
  return request.get("/api/start");
};

const Stop = () => {
  return request.get("/api/stop");
};

const Test = () => {
  return request.get("/api/test");
};

export default {
  Start,
  Stop,
  Test,
};
