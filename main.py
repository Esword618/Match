# -*- coding: utf-8 -*-
import os
import random
import shutil
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


# 根目录
@logger.catch
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 测试后端连接
@logger.catch
@app.get("/api/test")
async def Test():
    # 这里注释是为了便于调试，其实它是必须组件
    # TestErr = myThread.Test()
    # if TestErr:
    #     resData = {"code": 200, "data": {"info":"请检查端口"}, "msg": False}
    #     logger.info(resData)
    #     return resData
    resData = {"code":200,"data":{"info":None},"msg":True}
    logger.info(resData)
    return resData


# 开始
@logger.catch
@app.get("/api/start")
async def Start():
    # 这里注释是为了便于调试，其实它是必须组件
    # myThread.Start()
    resData = {"code": 200,"data": {"info": None},"msg":True}
    return resData


# 结束
@logger.catch
@app.get("/api/stop")
async def Stop():
    # 这里注释是为了便于调试，其实它是必须组件
    # myThread.Stop()
    resData = {"code": 200,"data":{"info": None},"msg":True}
    return resData



# 获取图片名字
@logger.catch
@app.get("/api/getImgName")
async def GetImgName():
    imgList = os.listdir('./save/img')
    # print(imgList)
    # imgList = [i.replace(".jpg","") for i in imgList if ".jpg" in i]
    # filename = f"{min(imgList)}.jpg"
    filename = random.choice(imgList)
    logger.info(filename)
    resData = {"code":200,"data":{"info":filename},"msg":True}
    return resData


# 图片展示api
# 请求加个时间戳就可以 例如 http://127.0.0.1:8000/api/showImg?imgType=number&t=111111 这里不会对?t=timestamp进行验证
@logger.catch
@app.get("/api/showImg")
async def showImg(
        filename: Optional[str] = Query(...,title="图片类型"),
    ):
    # logger.info(len(t))
    # logger.info(f"t:{t},imgType:{filename}")
    # path = './save/img'
    # imgList = os.listdir(path)
    # imgList = [i.replace(".jpg", "") for i in imgList if ".jpg" in i]
    # filename = f"{min(imgList)}.jpg"
    # filename = random.choice(imgList)
    pathB = os.path.exists(f"./save/img/{filename}")
    if pathB:
        return FileResponse(path=f'./save/img/{filename}')
    # return FileResponse(path='./static/404.jpg',filename=f"{t}.jpg")
    return FileResponse(path='./static/404.jpg')

# 获取画图数据
@logger.catch
@app.get("/api/data")
async def Data():
    # csvFileLis = os.listdir(CsvPath)
    # csvFileLis = [int(i.replace(".csv", "")) for i in csvFileLis]
    # timestamp = min(csvFileLis)
    # path = f"{CsvPath}\\{timestamp}.csv"
    # df = pd.read_csv(path)
    # data = df._get_column_array(0).tolist()
    data2 = np.random.normal(0, 1, size=(1, 1024))
    rawdata = data2.tolist()[0]
    Concentration = random.randint(1,100)
    Concentrationdata = [Concentration,100-Concentration]
    print(time.time())
    resData = {"code":200,"data":{"rawdata":rawdata,"concentrationdata":Concentrationdata},"msg":True}
    # logger.info(resData)
    return resData
