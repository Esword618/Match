import request from "./httpConfig";
// 如果是post请求需要qs进行一个处理
// import qs from "qs";

// 开始
const Start = () => {
  return request.get("/api/start");
};

// 结束
const Stop = () => {
  return request.get("/api/stop");
};

// 测试
const Test = () => {
  return request.get("/api/test");
};

// 请求图片
const ShowImg = (filename) => {
  return request.get("/api/showImg", { params: { filename } });
};

// 获取图片名字
const GetImgName = () => {
  return request.get("/api/getImgName");
};

// 获取数据
const GetData = () => {
  return request.get("/api/data");
};

export default {
  Start,
  Stop,
  Test,
  ShowImg,
  GetData,
  GetImgName,
};
