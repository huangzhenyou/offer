#coding:utf-8

from __future__ import division
import pandas as pd
import numpy as np
import time
import csv
import os
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))

writer = csv.writer(file('VLOC_AIS_201409_11_2.csv','wb'))
writer.writerow(['mmsi','acu_time','lon','lat'])

vloc_mmsi = np.array(pd.read_csv('VLOC_mmsi.csv'))
mmsi_all = vloc_mmsi[:,1]
print mmsi_all


fileNameList = []
# for fileName in os.listdir(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape'):
for fileName in os.listdir(u'D:\\1.王晓敏\\数据\\AIS原始数据\\201409_11'):
    fileNameList.append(fileName)

for day in range(len(fileNameList)):
    print day
    each_day = np.array(pd.read_csv(u'D:\\1.王晓敏\\数据\\AIS原始数据\\201409_11\\' + fileNameList[day]))
    for i in range(len(each_day)):
        uni_id = each_day[i][0]
        if uni_id in mmsi_all:
            writer.writerow(each_day[i,0:4])
print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))