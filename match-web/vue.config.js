const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  transpileDependencies: true,
});
// export default defineConfig({
//   // 本地运行配置，及反向代理配置
//   server: {
//     host: "localhost", // 指定服务器主机名
//     port: 8080, // 指定服务器端口
//     open: true, // 在服务器启动时自动在浏览器中打开应用程序
//     strictPort: false, // 设为 false 时，若端口已被占用则会尝试下一个可用端口,而不是直接退出
//     https: false, // 是否开启 https
//     cors: true, // 为开发服务器配置 CORS。默认启用并允许任何源
//     proxy: {
//       // 为开发服务器配置自定义代理规则
//       "/api": {
//         target: "http://127.0.0.1:8000", //代理接口
//         changeOrigin: true,
//         rewrite: (path) => path.replace(/^\/api/, ""),
//       },
//     },
//   },
// });
