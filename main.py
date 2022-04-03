# -*- coding: utf-8 -*-
import os

from log import logger
from fastapi import FastAPI,File
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from model import MyThread
app = FastAPI()

# 跨域处理
origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 实例化
myThread = MyThread()


# 根目录
@logger.catch
@app.get("/")
async def root():
    return {"message": "Hello World"}


# 开始
@logger.catch
@app.get("/api/start")
async def Start():
    myThread.Start()
    return {"code": 200,"data": None,"msg":True}


# 结束
@logger.catch
@app.get("/api/stop")
async def Stop():
    myThread.Stop()
    return {"code": 200,"data":None,"msg":True}


# 获取图片名字
@logger.catch
@app.get("/api/getImgName")
async def GetImgName():
    imgList = os.listdir('./save/img')
    print(imgList)
    imgList = [i.replace(".jpg","") for i in imgList if ".jpg" in i]

    filename = f"{min(imgList)}.jpg"
    return {"code":200,"data":{"filename":filename},"msg":True}

# 测试后端连接
@logger.catch
@app.get("/api/test")
async def Test():
    return {"code":200,"data":{},"msg":True}

# 图片展示api
# 请求加个时间戳就可以 例如 http://127.0.0.1:8000/api/showImg?t=111111 这里不会对?t=timestamp进行验证
@logger.catch
@app.get("/api/showImg")
async def showImg():
    path = './save/img'
    imgList = os.listdir(path)
    imgList = [i.replace(".jpg", "") for i in imgList if ".jpg" in i]
    filename = f"{min(imgList)}.jpg"
    pathB = os.path.exists("./save/img/1.jpg")
    if pathB:
        return FileResponse(path=f'./save/img/{filename}')
    return FileResponse(path='./static/404.jpg')
