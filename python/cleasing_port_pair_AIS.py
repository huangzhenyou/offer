#coding:utf-8
from __future__ import division
import pandas as pd
import csv
import numpy as np
import math

RADIUS = 20 #公里
EARTH_RADIUS = 6378.137  # 地球半径，单位千米
SPEED = 12.85 #单位是m/s
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
def clean_data():
    #写数据
    # writer = csv.writer(file('clean_port_pair_nav_AIS.csv','wb'))
    # writer.writerow(['mmsi', 'acqui_time', 'lon', 'lat','beg_port','end_port','frequency'])
    writer = csv.writer(file('clean_AIS_cape_all.csv','wb'))
    writer.writerow(['unique_id','acqusition_time','lon','lat','speed','conversion','cog','true_header'])
    #读数据
    count = 0
    # data = pd.read_csv('port_pair_nav_AIS.csv')
    # grouped = data.groupby('mmsi')
    data = pd.read_csv(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\AIS_cape_ALL.csv')
    grouped = data.groupby('unique_id')
    for group in grouped:
        each_ship = np.array(group[1])
        for i in range(len(each_ship) - 1):   #对每个船只的每一行数据
            # print each_ship[i][2],each_ship[i][3]
            # raw_input('===============')
            dis = getDist(each_ship[i][2],each_ship[i][3],each_ship[i+1][2],each_ship[i+1][3])  #经纬度间的距离，单位是千米
            d = abs(each_ship[i+1][1] - each_ship[i][1]) * SPEED / 1000  #单位是千米
            if dis > d:   #如果经纬度的距离>速度*时间,就删除数据，也就是不写入文件
                print group[0],"不合理数据存在第",i,"行"
                i = i+2  #跳到下两条比较
                if i >= len(each_ship) - 1:
                    break
            else:
                writer.writerow(each_ship[i])
                count +=1
    print count,len(data)
    return

def remove_line():
    data = pd.read_csv("clean_AIS_cape_all.csv") #3098条轨迹
    data['num'] = [0] * len(data['unique_id'])
    groupedData = data.groupby(data['unique_id'])
    # print data.head()
    paintData = pd.DataFrame(data=None,columns=['unique_id','acqusition_time','lon','lat','speed','conversion','cog','true_header','num'])
    count = 1
    for group in groupedData:  #每个group是一条轨迹
        a_route = group[1]
        last_index = 0
        for line in range(len(a_route) - 1):
            if a_route.iloc[line, 2] * a_route.iloc[line+1, 2] < 0.0: #地图上左右两边的横线
                a_route.iloc[last_index:line+1, 8] = count  #'num',改
                count += 1
                last_index = line+1
        a_route.iloc[last_index:, 8] = count
        count += 1
        print count
        # print a_route.head()
        paintData = paintData.append(a_route, ignore_index=True)
        #print paintData.head()
        #raw_input('============================')
    paintData.to_csv('R_clean_AIS_cape_all.csv',index=None)
    return

if __name__ == "__main__":
    # clean_data()
    remove_line()