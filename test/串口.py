# -*- coding: utf-8 -*-
# Time : 2022/4/3 20:49
# File : 串口.py
# Author : Esword

# -*- encoding: utf-8 -*-
import json
import logging
import binascii
import re
import sys
import time
from time import sleep

import numpy as np
import serial
from loguru import logger
import pandas as pd
portName = "COM7"
BaudRate = 57600
port = serial.Serial(port=portName, baudrate=BaudRate)


if port.isOpen():
    rawdataList = []
    logging.info("串口打开成功！")
    sleep(1)
    print(50*'-')
    info = ''
    # 判断是否是第一包，一开始为真，判断是第一个就设为False
    IsFirst = True
    while True:
        info += port.read(size=72).hex().upper()
        S = re.findall('AAAA2002[A-Za-z0-9]{64}(.*?)(AAAA2002[A-Za-z0-9]{64})',info)
        if S:
            # print(S)
            SmallList = re.findall('AAAA048002[A-Za-z0-9]{6}', S[0][0])
            # print(len(SmallList))
            # print(SmallList)
            if len(SmallList)==512:
                isNext = True
                rawdataList = []
                # 小包数据处理
                for i in SmallList:
                    xxHigh,xxLow,xxCheckSum = int(i[-6:-4],16),int(i[-4:-2],16),int(i[-2:],16)
                    # sum = ((0x80 + 0x02 + xxHigh + xxLow)^ 0xFFFFFFFF) & 0xFF
                    sum = ((128 + 2 + xxHigh + xxLow) ^ 4294967295) & 255
                    if sum != xxCheckSum:
                        logger.error("-------》丢包")
                        isNext = False
                        break
                    rawdata = (xxHigh << 8) | xxLow
                    rawdata = (rawdata*(1.8/4096))/2000
                    rawdataList.append(rawdata)
                    # if len(rawdataList)==20:
                    #     # 做图片什么的操作
                    #     rawdataList.clear()
                    # rawdataList.append(rawdata)
                    # logger.info(f'---->rawdata:{rawdata}')
                    # print(SmallList)
                    # print(len(SmallList))
                    # print("----------")

                if isNext:
                    print(rawdataList)

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
                Signal = int(BigBagStr[6:8],16)
                AttentionMeditation = BigBagStr[-10:]
                Attention = int(AttentionMeditation[2:4], 16)
                Meditation = int(AttentionMeditation[-4:-2], 16)
                logger.info(f"---->Signal:{Signal}")
                logger.info(f"---->Attention:{Attention}")
                logger.info(f"---->Meditation:{Meditation}")
                logger.warning("<---------------------------->")
                Info = {
                    "RawList":rawdataList,
                    "Attention":Attention,
                    "Meditation":Meditation
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
                df.to_csv(f"data_file/{int(time.time()*10)}.csv",index=False)
                # with open(f"data_file/{int(time.time()*10)}.txt","w") as f:
                #     f.write(json.dumps(Info))



else:
    logging.info("串口打开失败或串口名字有误！")
