# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:15
# File : __init__.py.py
# Author : Esword
import os
import threading
import time
from time import sleep
import re

import matplotlib

from config import NSeconds,CsvPath,ImgPath,BackupCsvPath,BackupImgPath,AttentionPath
import serial
import numpy as np
import pandas as pd
import mne
from itertools import chain
import matplotlib.pyplot as plt
from log import logger


class MyThread():
    def __init__(self):
        self.stop_threads = False
        self.threadEeg = None
        self.threadSensor = None
        self.SensorErr = False
        self.IsNSeconds = 0

    # 生成图片位置
    def Eeg(self):
        while True:
            logger.warning("This is Eeg")
            if self.stop_threads:
                break
            CsvPathList = os.listdir(CsvPath)
            CsvPathList = [int(i.replace(".csv", "")) for i in CsvPathList]
            timestamp = min(CsvPathList)
            data_path = f"save/csv/{timestamp}.csv"
            data1 = []
            matplotlib.use('Agg')
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
                figure.savefig(f'{ImgPath}/{timestamp}.png')
                figure.savefig(f'{BackupImgPath}/{timestamp}.png')

    # 接收数据
    def Sensor(self):
        portName = "COM3"
        BaudRate = 57600
        port = serial.Serial(port=portName, baudrate=BaudRate)
        if port.isOpen():
            rawdataList = []
            logger.info("串口打开成功！")
            sleep(1)
            print(50 * '-')
            info = ''
            # 判断是否是第一包，一开始为真，判断是第一个就设为False
            while True:
                if self.stop_threads:
                    return
                # logger.warning("Sensor")
                info += port.read(size=72).hex().upper()
                S = re.findall('AAAA2002[A-Za-z0-9]{64}(.*?)(AAAA2002[A-Za-z0-9]{64})', info)
                if S:
                    # print(S)
                    SmallList = re.findall('AAAA048002[A-Za-z0-9]{6}', S[0][0])
                    # print(len(SmallList))
                    # print(SmallList)
                    if len(SmallList) == 512:
                        isNext = True
                        # rawdataList = []
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
                            self.IsNSeconds += 1
                            # if len(rawdataList)==20:
                            #     # 做图片什么的操作
                            #     rawdataList.clear()
                            # rawdataList.append(rawdata)
                            # logger.info(f'---->rawdata:{rawdata}')
                            # print(SmallList)
                            # print(len(SmallList))
                            # print("----------")

                        # if isNext:
                            # print(rawdataList)

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
                        # logger.info(Info)
                        logger.warning(self.IsNSeconds)
                        #
                        # if NSeconds == self.IsNSeconds:
                            # 数据情况
                        info=''
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
                        # 清空 rawdataList
                        rawdataList.clear()
                        timestamp = int(time.time() * 10)
                        with open(AttentionPath,"w") as f:
                            f.write(f"{Attention}")
                        df.to_csv(f"{CsvPath}/{timestamp}.csv", index=False)
                        df.to_csv(f"{BackupCsvPath}/{timestamp}.csv", index=False)
                        self.IsNSeconds = 0
                            # with open(f"data_file/{int(time.time()*10)}.txt","w") as f:
                            #     f.write(json.dumps(Info))

        else:
            logger.info("串口打开失败或串口名字有误！")
            self.SensorErr = True

    def Test(self):
        self.threadSensor = threading.Thread(target=self.Sensor)
        self.threadEeg = threading.Thread(target=self.Eeg)
        self.threadSensor.start()
        self.threadEeg.start()
        if self.SensorErr:
            self.Stop()
            self.threadEeg.join()
            return False
        self.Stop()
        return True

    def Start(self):
        self.threadSensor = threading.Thread(target=self.Sensor)
        self.threadEeg = threading.Thread(target=self.Eeg)
        self.threadSensor.start()
        self.threadEeg.start()

    def Stop(self):
        self.stop_threads = True
        self.threadSensor.join()
        self.threadEeg.join()
