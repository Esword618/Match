
## 注释仅仅些部分，后面再加。

##豆瓣源下载
pip install xxx -i https://pypi.douban.com/simple/

## 框架说明
    后端 fastapi
    前端 vue3 + Ant Design of Vue(框架)
    Ant Design of Vue 地址 https://next.antdv.com/docs/vue/introduce-cn/

## 启动命令
后端启动命令(热更新命令)

    uvicorn main:app --reload
非热更新命令

    uvicorn main:app
命令含义如下:

    main：main.py 文件（一个 Python「模块」）。

    app：在 main.py 文件中通过 app = FastAPI() 创建的对象。

    --reload：让服务器在更新代码后重新启动。仅在开发时使用该选项。

## 说明
`test`文件夹是测试文件

`match-web`是前端框架
    启动命令 yarn run serve

`剩下的为后端框架`



