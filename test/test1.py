# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:10
# File : test1.py
# Author : Esword
import os

dirList = os.listdir('../save/img')
print(dirList)
d = [1,4,32,43]
d = min(d)
print(d)
d = os.path.exists("../save/img/1.jpg")
print(d)
