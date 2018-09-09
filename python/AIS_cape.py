#coding:utf-8
#在AIS数据中挑出cape船的AIS数据
from __future__ import division
import pandas as pd
import csv
import numpy as np
PREISION = 1000000
import os
import time
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))

fileNameList = []
for fileName in os.listdir(r'\\DESKTOP-AH1EE5F\2015-09-11csv\201511'):
    fileNameList.append(fileName)

#读取cape_static
cape_static = pd.read_csv('cape_static.csv')
cape_arr = np.array(cape_static)
mmsi = cape_arr[:,19]

#读取AIS数据
for day in range(31): #改，一个月30或31天
    ais = pd.read_csv(r'\\DESKTOP-AH1EE5F\2015-09-11csv\201511\\'+fileNameList[day])  #改
    writer = csv.writer(file('AIS_cape_'+fileNameList[day][6:], 'wb'))  # 改
    writer.writerow(['unique_id', 'acqusition_time', 'lon', 'lat', 'speed', 'conversion', 'cog', 'true_header'])
    print len(ais)
    ais_arr = np.array(ais)
    ais_arr[:,5:7] = ais_arr[:,5:7] / PREISION
    count = 0
    for line in range(len(ais)):
        count += 1
        if count % 1000000 == 0: print count
        unique_id = ais_arr[line][0] #ais的id
        if unique_id in mmsi:
            write_line = []
            write_line.extend(ais_arr[line, [0, 1, 5, 6, 8, 9, 10, 11]])
            writer.writerow(write_line)
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))