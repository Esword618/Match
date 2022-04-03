# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:15
# File : __init__.py.py
# Author : Esword

import threading
from log import logger


class MyThread():
    def __init__(self):
        self.stop_threads = False
        self.threadEeg = None
        self.threadSensor = None

    # 生成图片位置
    def Eeg(self):
        while True:
            logger.warning("This is Eeg")
            if self.stop_threads:
                break
    # 接收数据
    def Sensor(self):
        while True:
            logger.info("This is Sensor")
            if self.stop_threads:
                break

    def Start(self):
        self.threadSensor = threading.Thread(target=self.Sensor)
        self.threadEeg = threading.Thread(target=self.Eeg)
        self.threadSensor.start()
        self.threadEeg.start()

    def Stop(self):
        self.stop_threads = True
        self.threadSensor.join()
        self.threadEeg.join()
