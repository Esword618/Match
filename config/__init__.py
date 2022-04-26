# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:33
# File : __init__.py
# Author : Esword


# 串口名字
import os.path

portName = "COM3"
# 波特率
BaudRate = 57600
# N 秒写一次csv
NSeconds = 1
# 默认路径
BasePath = "D:\pyproject\Match\save"
# 专注度路径
AttentionPath = f'{BasePath}/attention.txt'
# csv保存路径
CsvPath = f"{BasePath}/csv"
# 生成图片保存路径
ImgPath = f"{BasePath}/img"
# backpath
BaseBackPath = f"{BasePath}/backup"
# 备份csv数据
BackupCsvPath = f"{BaseBackPath}/csv"
# 备份图片路径
BackupImgPath = f"{BaseBackPath}/img"
# 日志路径
LogPath = f"{BasePath}/logs"


def Init():
    PathList = [BasePath,CsvPath,ImgPath,BaseBackPath,BackupCsvPath,BackupImgPath,LogPath]
    for iPath in PathList:
        b = os.path.exists(iPath)
        if not b:
            os.mkdir(iPath)

