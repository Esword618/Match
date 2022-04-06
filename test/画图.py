# -*- coding: utf-8 -*-
# Time : 2022/4/3 20:49
# File : 画图.py
# Author : Esword

import mne
import numpy as np
import pandas as pd
from itertools import chain
import matplotlib.pyplot as plt

data_path = "csv/data.csv"

data1 = []
for j in range(1, 23):
    data = pd.read_csv(data_path, usecols=[str(j)])
    list1 = data.values.tolist()
    final_list = list(chain.from_iterable(list1))
    data1.append(final_list)


ch_names = ['Fz', 'FC3', 'FC1', 'FCz', 'FC2', 'FC4', 'C5', 'C3', 'C1', 'Cz', 'C2', 'C4', 'C6', 'CP3', 'CP1', 'CPz',
                'CP2', 'CP4', 'P1', 'Pz', 'P2', 'POz']
ch_types = ['eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg',
                'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg', 'eeg']
sfreq = 100  # Hz
info = mne.create_info(ch_names, sfreq, ch_types)
montage = mne.channels.make_standard_montage("standard_1020")

#事件 根据事件生成
evoked = mne.EvokedArray(data1, info)
evoked.set_montage(montage)
evoked_csd = mne.preprocessing.compute_current_source_density(evoked)
evoked.plot_joint(title='Average Reference', show=False)
evoked_csd.plot_joint(title='Current Source Density')
plt.show()


#脑电图
# mne.viz.plot_topomap(evoked.data[:, 0], evoked.info,show=False)
# plt.show()
# for i in range(6):
#     mne.viz.plot_topomap(evoked.data[:, i], evoked.info,show=False)
#     plt.savefig(str(i))
#     plt.clf()


#生成脑电地形图 根据事件
# mne.viz.plot_topomap(evoked.data[:, 3], evoked.info,show=False)
# plt.show()
# report = mne.Report(title='脑电图')
# report.add_evokeds(
#     evokeds=evoked,
# )
# report.save('report_evoked.html', overwrite=True)


#时间 根据时间生成
# epoch = mne.EpochsArray(data1,info)
# epoch.set_montage(montage)
# report = mne.Report
# report.add_epochs(
#      epoch=epoch,
# )
# report.save('report_epoch.html', overwrite=True)
