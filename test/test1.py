# -*- coding: utf-8 -*-
# Time : 2022/4/3 11:10
# File : test1.py
# Author : Esword
import os

dirList = os.listdir('../save/csv')
print(dirList)
dirList = [int(i.replace(".csv","")) for i in dirList]
print(dirList)
print(min(dirList))
# print(dirList)
# d = [1,4,32,43]
# d = min(d)
# print(d)
# d = os.path.exists("../save/img/1.jpg")
# print(d)
# import pandas as pd
# import numpy as np
# rawdataList = [1,323,32,32433565567,766,2,665,43222,245]
# df = pd.DataFrame({
#     '0': np.array(rawdataList),
#     '1': 0,
#     '2': 0,
#     '3': 0,
#     '4': 0,
#     '5': 0,
#     '6': 0,
#     '7': 0,
#     '8': 0,
#     '9': 0,
#     '10': 0,
#     '11': 0,
#     '12': 0,
#     '13': 0,
#     '14': 0,
#     '15': 0,
#     '16': 0,
#     '17': 0,
#     '18': 0,
#     '19': 0,
#     '20': 0,
#     '21': 0
# })
# # 清空 rawdataList
# rawdataList.clear()
# df.to_csv(f"16854151251.csv", index=False)
