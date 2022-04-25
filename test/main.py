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
from fastapi.responses import StreamingResponse
# -*- encoding: utf-8 -*-
import json
import logging
import binascii
import re
import sys
import time
from time import sleep
import os
import numpy as np
import serial
from loguru import logger
import pandas as pd
import matplotlib
from itertools import chain
import mne


def img_gne():
    portName = "COM7"
    BaudRate = 57600
    port = serial.Serial(port=portName, baudrate=BaudRate)
    if port.isOpen():
        rawdataList = []
        logging.info("串口打开成功！")
        sleep(1)
        print(50 * '-')
        info = ''
        # 判断是否是第一包，一开始为真，判断是第一个就设为False
        IsFirst = True
        N=0
        while(N==0):
            info += port.read(size=72).hex().upper()
            S = re.findall('AAAA2002[A-Za-z0-9]{64}(.*?)(AAAA2002[A-Za-z0-9]{64})', info)
            if S:
                # print(S)
                SmallList = re.findall('AAAA048002[A-Za-z0-9]{6}', S[0][0])
                # print(len(SmallList))
                if len(SmallList) == 512:
                    isNext = True
                    rawdataList = []
                    # 小包数据处理
                    for i in SmallList:
                        xxHigh, xxLow, xxCheckSum = int(i[-6:-4], 16), int(i[-4:-2], 16), int(i[-2:], 16)
                        # sum = ((0x80 + 0x02 + xxHigh + xxLow)^ 0xFFFFFFFF) & 0xFF
                        sum = ((128 + 2 + xxHigh + xxLow) ^ 4294967295) & 255
                        if sum != xxCheckSum:
                            logger.error("-------》丢包")
                            isNext = False
                            break
                        rawdata = (xxHigh << 8) | xxLow
                        rawdata = (rawdata * (1.8 / 4096)) / 2000
                        rawdataList.append(rawdata)
                        # if len(rawdataList)==20:
                        #     # 做图片什么的操作
                        #     rawdataList.clear()
                        # rawdataList.append(rawdata)
                        # logger.info(f'---->rawdata:{rawdata}')
                        # print(SmallList)
                        # print(len(SmallList))
                        # print("----------")

                    # if isNext:
                    #     print()

                    # 打包数据处理
                    # AA 同步
                    # AA 同步
                    # 20 是十进制的32，即有32个字节的payload，除掉20本身+两个AA同步+最后校验和
                    # 02 代表信号值Signal
                    # C8 信号的值
                    # 83 代表EEG Power开始了
                    # 18 是十进制的24，说明EEG Power是由24个字节组成的，以下每三个字节为一组
                    # 18 Delta 1/3
                    # D4 Delta 2/3
                    # 8B Delta 3/3
                    # 13 Theta 1/3
                    # D1 Theta 2/3
                    # 69 Theta 3/3
                    # 02 LowAlpha 1/3
                    # 58 LowAlpha 2/3
                    # C1 LowAlpha 3/3
                    # 17 HighAlpha 1/3
                    # 3B HighAlpha 2/3
                    # DC HighAlpha 3/3
                    # 02 LowBeta 1/3
                    # 50 LowBeta 2/3
                    # 00 LowBeta 3/3
                    # 03 HighBeta 1/3
                    # CB HighBeta 2/3
                    # 9D HighBeta 3/3
                    # 03 LowGamma 1/3
                    # 6D LowGamma 2/3
                    # 3B LowGamma 3/3
                    # 03 MiddleGamma 1/3
                    # 7E MiddleGamma 2/3
                    # 89 MiddleGamma 3/3
                    # 04 代表专注度Attention
                    # 00 Attention的值(0到100之间)
                    # 05 代表放松度Meditation
                    # 00 Meditation的值(0到100之间)
                    # D5 校验和
                    BigBagStr = S[0][1]
                    Signal = int(BigBagStr[6:8], 16)
                    AttentionMeditation = BigBagStr[-10:]
                    Attention = int(AttentionMeditation[2:4], 16)
                    Meditation = int(AttentionMeditation[-4:-2], 16)
                    logger.info(f"---->Signal:{Signal}")
                    logger.info(f"---->Attention:{Attention}")
                    logger.info(f"---->Meditation:{Meditation}")
                    logger.warning("<---------------------------->")
                    Info = {
                        "RawList": rawdataList,
                        "Attention": Attention,
                        "Meditation": Meditation
                    }
                    df = pd.DataFrame({
                        '0': np.array(rawdataList),
                        '1': 0,
                        '2': 0,
                        '3': 0,
                        '4': 0,
                        '5': 0,
                        '6': 0,
                        '7': 0,
                        '8': 0,
                        '9': 0,
                        '10': 0,
                        '11': 0,
                        '12': 0,
                        '13': 0,
                        '14': 0,
                        '15': 0,
                        '16': 0,
                        '17': 0,
                        '18': 0,
                        '19': 0,
                        '20': 0,
                        '21': 0
                    })
                    a= int(time.time() * 10)
                    df.to_csv(f"save/csv/{a}.csv", index=False)
                    df.to_csv(f"save1/csv/{a}.csv",index=False)
                    # with open(f"data_file/{int(time.time()*10)}.txt","w") as f:
                    #     f.write(json.dumps(Info))
                    matplotlib.use('Agg')
                    csv_name = os.listdir("save/csv/")
                    for i in csv_name:
                        data_path = 'save/csv/' + i
                        data1 = []
                        st = time.time()
                        for j in range(0, 22):
                            data = pd.read_csv(data_path, usecols=[str(j)])
                            list1 = data.values.tolist()
                            final_list = list(chain.from_iterable(list1))
                            data1.append(final_list)

                        ch_names = ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6',
                                    'CP3', 'CP1', 'CPz',
                                    'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
                        ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                                    'eeg', 'eeg', 'eeg',
                                    'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
                        sfreq = 512  # Hz
                        info = mne.create_info(ch_names, sfreq, ch_types)
                        raw = mne.io.RawArray(data1, info)
                        montage = mne.channels.make_standard_montage("standard_1020")
                        raw.set_montage(montage)

                        # 需要滤波
                        raw = raw.filter(l_freq=0.1, h_freq=30)
                        # components太高runtime_error
                        ica = mne.preprocessing.ICA(n_components=8, random_state=97, max_iter=800)
                        ica.fit(raw)
                        for k, figure in enumerate(ica.plot_components()):
                            figure.savefig('save/img/figure0.png')
                            figure.savefig(f'save1/img/{a}.png')
                        os.remove(data_path)
                info = ''
                N= 1
                # time.sleep(5)

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

@logger.catch
@app.get("/api/img_gne")
async def gne():
    img_gne()
    resData = {"code":200}
    return resData


@logger.catch
@app.get("/api/img_wat")
async def watch():
    img = open(f'./save/img/figure0.png',mode="rb")
    return StreamingResponse(img,media_type='image/png')

