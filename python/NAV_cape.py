#coding:utf-8
#从停泊事件中挑选属于cape船的事件

from __future__ import division
import pandas as pd
import numpy as np
import csv
PREISION = 1000000
import time
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
#写
# writer = csv.writer(file('NAV_cape_201511.csv','wb'))
# writer.writerow(['unique_id','beg_time','end_time','beg_lon','beg_lat','end_lon','end_lat','point_num'])
#读cape_static文件
cape_static = pd.read_csv('cape_static.csv')
cape_arr = np.array(cape_static)
mmsi = cape_arr[:,19]
mmsi = set(list(mmsi))
print len(mmsi)   #1582条数据

#读停泊事件    [注意]：停泊事件中的经纬度是乘以100万后的结果，码头信息中的经纬度是正常的，所有要注意把停泊事件的经纬度除以100万
nav = pd.read_csv(u'D:\\1.王晓敏\\数据\\全球201509-201511的70类型船的停泊事件\\nav_event_more_201511_pre.csv')
nav = nav.append(pd.read_csv(u'D:\\1.王晓敏\\数据\\全球201509-201511的70类型船的停泊事件\\nav_event_more_201511_aft.csv'))
nav_array = np.array(nav)
print len(nav_array)
# 把停泊事件中的经纬度除以100万
for nav_line in range(len(nav)):
    for i in range(3, 7):
        nav_array[nav_line][i] = nav_array[nav_line][i] / PREISION
###
count = 0
for line in range(len(nav)):
    count += 1
    if count % 10000 == 0: print count
    unique_id = nav_array[line][0]
    if unique_id in mmsi:
        writer.writerow(nav_array[line])

print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))