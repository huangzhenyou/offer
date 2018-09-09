#coding:utf-8
#船型和静态数据匹配的结果cape_static与停泊事件匹配 imo
#根据停泊位置判断停在哪个港口
from __future__ import division
import pandas as pd
import numpy as np
import csv
import math
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

PREISION = 1000000
RADIUS = 20 #公里
EARTH_RADIUS = 6378.137  # 地球半径，单位千米

print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
# 判断点是否在给定多边形内，返回T或F
def point_poly(pointLon, pointLat, polygon):
    cor = len(polygon)
    i = 0
    j = cor - 1
    inside = False
    while (i < cor):
        if ((((polygon[i, 1] < pointLat) & (polygon[j, 1] >= pointLat))
                 | ((polygon[j, 1] < pointLat) & (polygon[i, 1] >= pointLat)))
                & ((polygon[i, 0] <= pointLon) | (polygon[j, 0] <= pointLon))):
            a = (polygon[i, 0] +
                 (pointLat - polygon[i, 1]) / (polygon[j, 1] - polygon[i, 1]) *
                 (polygon[j, 0] - polygon[i, 0]))

            if (a < pointLon):
                inside = not inside
        j = i
        i = i + 1

    return inside

#取码头合并信息中的区域，存为list
def get_area(str_area):
    result = []
    list_area = str_area.split('*')
    for i in range(len(list_area)):
        pair = list_area[i].split(';')
        for j in range(len(pair)):
            pair[j] = float(pair[j])
        result.append(pair)
    return np.array(result)

#########################################################
# 获得地球两点间距离
def getRadian(x):
    return x * math.pi / 180.0

def getDist(lon1, lat1, lon2, lat2):  # 得到地球两点距离，单位千米
    radLat1 = getRadian(lat1)
    radLat2 = getRadian(lat2)

    a = radLat1 - radLat2
    b = getRadian(lon1) - getRadian(lon2)

    dst = 2 * math.asin(math.sqrt(math.pow(math.sin(a / 2), 2) +
                                  math.cos(radLat1) * math.cos(radLat2) * math.pow(math.sin(b / 2), 2)))
    dst = dst * EARTH_RADIUS
    dst = round(dst * 100000000) / 100000000

    return dst
#######################################################

#把结果写入文件
# write_file = file('cape_nav_201509_201511.csv','wb')
# writer = csv.writer(write_file)
# writer.writerow(['Type', 'Name', 'Size', 'Unit', 'Dwt', 'GT', 'Flag', 'Built', 'Month', 'Builder', 'Owner Group', 'Status', 'chuanjishe', 'LOA', 'Draught', 'Beam', 'Speed', 'Call Sign', 'IMO Number',
#                  'mmsi', 'name',  #cape+静态字段
#                  'beg_time','end_time','beg_lon','beg_lat','end_lon','end_lat',  #停泊事件字段
#                  'port/dock name','port_lon','port_lat',
#                  'load_type','unload_type',])  #港口/码头信息字段
#读cape_static文件
cape_static = pd.read_csv('cape_static.csv')
len_cape_static = len(cape_static)
print len_cape_static,"条cape船"
cape_array = np.array(cape_static)

#读停泊事件    [注意]：停泊事件中的经纬度是乘以100万后的结果，码头信息中的经纬度是正常的，所有要注意把停泊事件的经纬度除以100万
nav = pd.read_csv('NAV_cape_201509.csv')  #NAV_cape_201509.csv 本来就是cape船的停泊事件，因此只需要识别停泊的港口即可
print len(nav)
nav = nav.append(pd.read_csv('NAV_cape_201510.csv'))
print len(nav)
nav = nav.append(pd.read_csv('NAV_cape_201511.csv'))
nav.sort_index(by=['unique_id','beg_time'])
nav_array = np.array(nav)  #64766行
print len(nav)
raw_input('=============')
#把停泊事件中的时间转换为北京时间
beijing_time = [[time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(x)) for x in line] for line in nav_array[:,1:3]]

#读港口/码头的范围
port_1 = np.array(pd.read_csv(u'D:\\1.王晓敏\\韩军老师\\数据\\码头信息合并.csv')) #先拿码头信息，因为港口信息的标定可能有错  #共33个port
port_2 = np.array(pd.read_csv(u'D:\\1.王晓敏\\韩军老师\\数据\\港口信息csv格式.csv'))  #韩军的港口信息  #共280个港口
port_3 = np.array(pd.read_csv(u'D:\\1.王晓敏\\韩军老师\\数据\\port_corrige.csv'))

find_count = 0
#cape_static与停泊事件匹配
for cape_line in range(len_cape_static): #静态数据中的每条cape船
    find = False
    for nav_line in range(len(nav)): #每条cape船的停泊事件
        if cape_array[cape_line][19] == nav_array[nav_line][0]: #cape船的mmsi==停泊事件的unique_id
            #找到船的停泊事件，取出开始和结束的经纬度，判断属于哪个港口
            # print cape_array[cape_line][19],nav_array[nav_line][0]
            #取港口区域位置
            for port_line in range(len(port_1)): # 先判断是否在“码头信息合并”的文件内
                if port_1[port_line][8][-1] == '*':
                    #删掉最后一个元素
                    port_1[port_line][8] = port_1[port_line][8][:-1]
                # try:
                area = get_area(port_1[port_line][8]) #码头区域坐标，str->list
                # except ValueError,e:
                #     print 'error',e,port_line,port_1[port_line][8]
                if apply(point_poly, (nav_array[nav_line][3],nav_array[nav_line][4],area)) or \
                    apply(point_poly,(nav_array[nav_line][5],nav_array[nav_line][6],area)):   #如果该船停泊事件的开始结束经纬度在港口内
                    find = True
                    write_line = []
                    write_line.extend(cape_array[cape_line]) #把cape船的静态信息写入
                    #写停泊事件的开始结束时间
                    write_line.extend(nav_array[nav_line][1:3])  #utc时间
                    # write_line.extend(beijing_time[nav_line][0:2]) #把该船对应的停泊事件的开始和结束北京时间字段写入
                    write_line.extend(nav_array[nav_line][3:7])  # 把该船对应的停泊事件的开始和结束经纬度字段写入
                    write_line.extend([port_1[port_line][0],area[0][0],area[0][1]]) #把船停泊的港口名字写入 dock/terminal  #改                       #这个文件中的港口，没有对应的装卸货类型，有些港口的装卸货类型可在《港口信息》中找到，所以需要把这个文件和港口信息合并
                    print 'writing'
                    writer.writerow(write_line)
                    break
                    # raw_input('=====================1===================')
            # print(find)
            # raw_input('=====================1===================')

            if find is False:  #如果在码头信息合并的文件内没找到，再在港口信息文件内找
                min_port_line = 0
                min_dist = 0
                for port_line in range(len(port_2)): #再判断是否在 “港口信息”的文件内
                    begin_dist = getDist(nav_array[nav_line][3],nav_array[nav_line][4], port_2[port_line][7], port_2[port_line][8]) #停泊开始位置与港口的距离
                    end_dist = getDist(nav_array[nav_line][5], nav_array[nav_line][6], port_2[port_line][7], port_2[port_line][8])  #停泊结束位置与港口的距离
                    if begin_dist < RADIUS or end_dist < RADIUS:  #停泊开始位置或结束位置与港口位置距离小于20公里
                        #考虑两个港口比较近的情况，将其分到较近的港口
                        mean_dist = np.mean([begin_dist,end_dist])
                        if min_dist == 0:
                            min_dist = mean_dist
                            min_port_line = port_line
                        elif mean_dist < min_dist:
                            min_dist = mean_dist
                            min_port_line = port_line
                        #把min_port_line写入文件，也就是距离停泊位置最近的港口
                        find = True
                if find is True:
                    write_line = []
                    write_line.extend(cape_array[cape_line])  # 把cape船的静态信息写入
                    #写停泊事件的开始结束时间
                    write_line.extend(nav_array[nav_line][1:3])  # utc时间
                    # write_line.extend(beijing_time[nav_line][0:2]) #把该船对应的停泊事件的开始和结束北京时间字段写入
                    write_line.extend(nav_array[nav_line][3:7])  # 把该船对应的停泊事件的开始和结束经纬度字段写入
                    write_line.extend(port_2[min_port_line,[0,7,8,1,2]])  #把港口信息的港口名称、港口位置、装载货物类型、卸货类型写入
                    print 'writing'
                    writer.writerow(write_line)
            # print find
            # raw_input('=====================2===================')
            if find is False: #如果在前两个文件内都没有找到，在port_corrige文件内找
                # print '在port_corrige中查找'
                min_port_line = 0
                min_dist = 0
                for port_line in range(len(port_3)):
                    begin_dist = getDist(nav_array[nav_line][3],nav_array[nav_line][4], port_3[port_line][13],port_3[port_line][14]) #停泊开始位置与港口的距离
                    end_dist = getDist(nav_array[nav_line][5], nav_array[nav_line][6], port_3[port_line][13], port_3[port_line][14]) #停泊结束位置与港口的距离
                    if begin_dist < RADIUS or end_dist < RADIUS:  #停泊开始位置或结束位置与港口位置距离小于20公里
                        #考虑两个港口比较近的情况，将其分到较近的港口
                        mean_dist = np.mean([begin_dist, end_dist])
                        if min_dist == 0:
                            min_dist = mean_dist
                            min_port_line = port_line
                        elif mean_dist < min_dist:
                            min_dist = mean_dist
                            min_port_line = port_line
                        #把min_port_line写入文件，也就是距离停泊位置最近的港口
                        find = True
                if find is True:
                    print '在port_corrige中找到了'
                    write_line = []
                    write_line.extend(cape_array[cape_line])  # 把cape船的静态信息写入
                    #写停泊事件的开始结束时间
                    write_line.extend(nav_array[nav_line][1:3])  # utc时间
                    # write_line.extend(beijing_time[nav_line][0:2]) #把该船对应的停泊事件的开始和结束北京时间字段写入
                    write_line.extend(nav_array[nav_line][3:7])  # 把该船对应的停泊事件的开始和结束经纬度字段写入
                    write_line.extend(port_3[min_port_line,[3,13,14]])  #把port_corrige的port字段写入
                    print 'writing'
                    writer.writerow(write_line)
            # print find
            # raw_input('=====================3===================')
    if find is True:
        find_count += 1
    print cape_line, find

print find_count,len_cape_static,find_count / len_cape_static    #750 2728 0.274926686217
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
