# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:33
# File : __init__.py
# Author : Esword


# 串口名字
import os.path

portName = "COM4"
# 波特率
BaudRate = 57600
# N 秒写一次csv
NSeconds = 4
# csv保存路径
CsvPath = "./save/csv"
# 生成图片保存路径
ImgPath = "./save/img"
# 日志路径
LogPath = "./save/logs"


def Init():
    b = os.path.exists("./save")
    if not b:
        os.mkdir("./save")
    b = os.path.exists(CsvPath)
    if not b:
        os.mkdir(CsvPath)
    b = os.path.exists(ImgPath)
    if not b:
        os.mkdir(ImgPath)
    b = os.path.exists(LogPath)
    if not b:
        os.mkdir(LogPath)
