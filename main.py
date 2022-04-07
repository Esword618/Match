# -*- coding: utf-8 -*-
import os
import time

from log import logger
from fastapi import FastAPI,Query
from typing import Optional
from config import Init,CsvPath
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from model import MyThread
import pandas as pd
import numpy as np

app = FastAPI()
# 初始化
Init()
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

IsOk = False

# 根目录
@logger.catch
@app.get("/")
async def root():
    return {"message": "Hello World"}


# 开始
@logger.catch
@app.get("/api/start")
async def Start():
    global IsOk
    IsOk = True
    myThread.Start()
    resData = {"code": 200,"data": {"info": None},"msg":True}
    return resData


# 结束
@logger.catch
@app.get("/api/stop")
async def Stop():
    global IsOk
    IsOk = False
    myThread.Stop()
    resData = {"code": 200,"data":{"info": None},"msg":True}
    return resData


# 获取图片名字
@logger.catch
@app.get("/api/getImgName")
async def GetImgName():
    imgList = os.listdir('./save/img')
    print(imgList)
    imgList = [i.replace(".jpg","") for i in imgList if ".jpg" in i]
    filename = f"{min(imgList)}.jpg"
    resData = {"code":200,"data":{"info":filename},"msg":True}
    return resData

# 测试后端连接
@logger.catch
@app.get("/api/test")
async def Test():
    TestErr = myThread.Test()
    if TestErr:
        resData = {"code": 200, "data": {"info":"请检查端口"}, "msg": False}
        logger.info(resData)
        return resData
    global IsOk
    IsOk = True
    resData = {"code":200,"data":{"info":None},"msg":True}
    logger.info(resData)
    return resData

# 图片展示api
# 请求加个时间戳就可以 例如 http://127.0.0.1:8000/api/showImg?imgType=number&t=111111 这里不会对?t=timestamp进行验证
@logger.catch
@app.get("/api/showImg")
async def showImg(
        imgType: Optional[int] = Query(...,title="图片类型"),
        t:Optional[str] = Query(...,title="时间戳",regex="\d+")
    ):
    logger.info(len(t))
    logger.info(f"t:{t},imgType:{imgType}")
    path = './save/img'
    imgList = os.listdir(path)
    imgList = [i.replace(".jpg", "") for i in imgList if ".jpg" in i]
    filename = f"{min(imgList)}.jpg"
    pathB = os.path.exists("./save/img/1.jpg")
    if pathB:
        return FileResponse(path=f'./save/img/{filename}')
    return FileResponse(path='./static/404.jpg',filename=f"{t}.jpg")

# 获取画图数据
@logger.catch
@app.get("/api/data")
async def Data():
    global IsOk
    # IsOk = True
    if not IsOk:
        resData = {"code": 200, "data": {"info": []}, "msg": False}
        logger.info(resData)
        return resData
    # csvFileLis = os.listdir(CsvPath)
    # csvFileLis = [int(i.replace(".csv", "")) for i in csvFileLis]
    # timestamp = min(csvFileLis)
    # path = f"{CsvPath}\\{timestamp}.csv"
    # df = pd.read_csv(path)
    # data = df._get_column_array(0).tolist()
    data2 = np.random.normal(0, 1, size=(1, 512))
    data = data2.tolist()[0]
    resData = {"code":200,"data":{"info":data},"msg":True}
    logger.info(resData)
    print(time.time())
    return resData
