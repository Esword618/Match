# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:15
# File : __init__.py.py
# Author : Esword

import threading
import time
from time import sleep
import re
from config import NSeconds,CsvPath
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

    # 生成图片位置
    def Eeg(self):
        while True:
            logger.warning("This is Eeg")
            if self.stop_threads:
                break

            data_path = CsvPath

            data1 = []
            for j in range(1, 23):
                data = pd.read_csv(data_path, usecols=[str(j)])
                list1 = data.values.tolist()
                final_list = list(chain.from_iterable(list1))
                data1.append(final_list)

            ch_names = ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1',
                        'CPz',
                        'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
            ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                        'eeg', 'eeg',
                        'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
            sfreq = 100  # Hz
            info = mne.create_info(ch_names, sfreq, ch_types)
            montage = mne.channels.make_standard_montage("standard_1020")

            # 事件 根据事件生成
            evoked = mne.EvokedArray(data1, info)
            evoked.set_montage(montage)
            evoked_csd = mne.preprocessing.compute_current_source_density(evoked)
            evoked.plot_joint(title='Average Reference', show=False)
            evoked_csd.plot_joint(title='Current Source Density')
            plt.show()

    # 接收数据
    def Sensor(self):
        portName = "COM7"
        BaudRate = 57600
        port = serial.Serial(port=portName, baudrate=BaudRate)
        if port.isOpen():
            rawdataList = []
            logger.info("串口打开成功！")
            sleep(1)
            print(50 * '-')
            info = ''
            # 判断是否是第一包，一开始为真，判断是第一个就设为False
            IsNSeconds = 0
            while True:
                if self.stop_threads:
                    return
                logger.warning("Sensor")
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
                            IsNSeconds += 1
                            # if len(rawdataList)==20:
                            #     # 做图片什么的操作
                            #     rawdataList.clear()
                            # rawdataList.append(rawdata)
                            # logger.info(f'---->rawdata:{rawdata}')
                            # print(SmallList)
                            # print(len(SmallList))
                            # print("----------")

                        # if isNext:
                        #     print(rawdataList)

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
                        if NSeconds == IsNSeconds:
                            IsNSeconds = 0
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
                            df.to_csv(f"{CsvPath}/{int(time.time() * 10)}.csv", index=False)
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
            return True
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
