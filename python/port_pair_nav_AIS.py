# coding:utf-8
# 根据每条船划分的停泊事件
import pandas as pd
import csv
import numpy as np
import time
import os

print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))

# 写数据
writer = csv.writer(file('port_pair_nav_AIS.csv', 'wb'))
writer.writerow(['mmsi', 'acqui_time', 'lon', 'lat','beg_port','end_port','frequency'])
#读AIS数据
fileNameList = []
for fileName in os.listdir(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape'): #改
    fileNameList.append(fileName)

#读数据
cape_nav = np.array(pd.read_csv('port_pair_nav.csv'))
print len(cape_nav)
count = 0
for line in range(len(cape_nav)):
    count += 1
    print count
    unique_id = cape_nav[line][0]
    beg_time = int(cape_nav[line][1])
    end_time = int(cape_nav[line][2])

    begin_time_beijing = time.strftime('%Y%m%d',time.localtime(beg_time))
    end_time_beijing = time.strftime('%Y%m%d',time.localtime(end_time))

    for fileName in fileNameList:
        if begin_time_beijing in fileName.encode('utf-8'):
            start_day = fileNameList.index(fileName)
        if end_time_beijing in fileName.encode('utf-8'):
            end_day = fileNameList.index(fileName)
    #根据停泊的开始结束时间，
    for day in range(start_day, end_day + 1):
        ais_arr = np.array(pd.read_csv(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\' + fileNameList[day])) #改
        for i in range(len(ais_arr)):
            if int((ais_arr[i][0]) == int(unique_id)) and (int(ais_arr[i][1]) in range(beg_time,end_time+1)): # 找在停泊时间之间的AIS数据
                # print 'find!!!!!!!!!!!!!!!!!!!!!'   #为什么找不到？？
                # raw_input('=========')
                nav_line = []
                nav_line.extend(ais_arr[i][0:4]) #mmsi,acq_time,lon,lat
                nav_line.extend(cape_nav[line][3:5]) #beg_port,end_port
                #连接频次统计，把频次加上                #这里的频次表示的是这个文件中的这个港口对会出现的频次
                port_pair_fre = np.array(pd.read_csv('port_pair_frequency.csv'))
                find = False
                for j in range(len(port_pair_fre)):
                    if cape_nav[line][3] == port_pair_fre[j][0] and cape_nav[line][4] == port_pair_fre[j][1]:
                        find = True
                        fre = port_pair_fre[j][2]
                        break
                if find is True:
                    nav_line.append(fre)
                # print nav_line
                # raw_input('=======================================')
                writer.writerow(nav_line)
    print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))