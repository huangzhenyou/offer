# coding:utf-8
from __future__ import division
import pandas as pd
import numpy as np
import time
import csv
import os
import math

#航速一节是1.852km/h,0.5144444（m/s）
SPEED = 0.5144444 #速度：m/s
ACCELERATION = 0.5144444 #加速度：m/s的平方
#########################################################
# 获得地球两点间距离
EARTH_RADIUS = 6378.137  # 地球半径，单位千米

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
##########################################################

def wash_data(data): #对一天中每条船的数据做清洗
    #去掉低速点和加速度高的点
    washed_data = pd.DataFrame(data=None,columns=['unique_id','acqusition_time','lon','lat','speed','conversion','cog','true_header'])
    # washed_data = data
    for i in range(len(data) - 1):
        #求速度
        s = getDist(data.iloc[i][2],data.iloc[i][3],data.iloc[i+1][2],data.iloc[i+1][3])  #经纬度间的距离，单位是千米
        t = abs(data.iloc[i,1] - data.iloc[i+1, 1])  #单位是秒
        v = s * 1000 / t #速度，单位是m/s
        # print "速度：", v,"m/s"
        #求加速度，AIS数据中speed的单位是0.1节
        d_speed = abs(data.iloc[i,4] - data.iloc[i+1,4]) #速度差，单位是0.001m/s，1节为0.5144444 m/s
        d_speed = d_speed * 0.001  #单位是m/s
        a = d_speed / t #加速度，单位是m/s的平方
        # print "加速度：",a,'m/s的平方'
        #比较
        if v < SPEED: #低速点data[i],航速小于一节
            # washed_data = washed_data.drop(i)
            continue
        elif a > ACCELERATION: #加速度高的点data[i]，加速度大于一节
            # washed_data = washed_data.drop(i)
            continue
        else:
            washed_data = washed_data.append(data.iloc[i],ignore_index=True)
    # print washed_data.head()
    # raw_input('============')
    return washed_data

def ave_speed(data): #data是dataframe类型
    all_speed = data.iloc[:,4] #speed字段
    ave = np.mean(all_speed)  #speed字段的平均值，单位是0.001m/s
    ave = ave * 0.001 / SPEED #转换为节
    return ave


fileNameList = []
for fileName in os.listdir(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\data'):
    fileNameList.append(fileName)

ave_speed_all = []
for day in range(len(fileNameList)):  #对每个文件操作
    print "计算",fileNameList[day], "的数据"
    print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
    washed_data_day = pd.DataFrame(data=None,columns=['unique_id','acqusition_time','lon','lat','speed','conversion','cog','true_header'])

    each_day = pd.read_csv(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\data\\' + fileNameList[day])
    grouped = each_day.groupby('unique_id')
    for group in grouped:  #对一天中的每条船操作
        each_ship = group[1] #每条船
        each_ship.sort_index(by='acqusition_time') #时间排序
        washed_data_ship = wash_data(each_ship) #清洗数据
        washed_data_day = washed_data_day.append(washed_data_ship,ignore_index=True) #加入每天的数据
    print fileNameList[day],"去掉",len(each_day) - len(washed_data_day),"行数据"
    # raw_input('====')
    washed_data_day.to_csv("speed_"+fileNameList[day],index=None)  #把处理后的每一天的数据保存下来

    ave_speed_by_day = ave_speed(washed_data_day) #每天的数据求一个平均值
    print "平均航速：",ave_speed_by_day
    ave_speed_all.append(ave_speed_by_day)

    print ave_speed_all
    #each_day是文件夹下每一天的数据
    #去掉数据中的低速点和加速度高的点


###############################################代运行
ave_speed_all = [11.42511773244269, 11.384388877998971, 11.411412338251729, 11.402440530219367, 11.425318222850716, 11.48227305376092, 11.430434924148429, 11.249983641613552, 11.339387014953047, 11.308333941011659, 11.212864044106567, 11.344897998841027, 11.400388769123731, 11.424408313372915, 11.272437349186255, 11.351770885729785, 11.229708307639214, 11.341816234551704, 11.478548062060819, 11.421042559351378, 11.324712264549554, 11.413260408708394, 11.2331547704472, 11.218028344957625, 11.272296534780072, 11.375595383903573, 11.289099755748323, 11.324330547992554, 11.358866985684598, 11.285267168120017, 11.310153628621428, 11.260816878885167, 11.367022686092092, 11.426851680244779, 11.275314645022693, 11.247955071813333, 11.323941830533231, 11.210142686211199, 11.360746664503873, 11.268734762508915, 11.240257538280821, 11.358735240260417, 11.650093220426076, 11.590373323488732, 11.581962767796661, 11.478958427752833, 11.496386446282781, 11.549958712648179, 11.451119630696871, 11.382526561509628, 11.430548648209406, 11.340383048220188, 11.425516297186739, 11.333277501568054, 11.371113100932137, 11.528338903625222, 11.442446070914601, 11.431480621617021, 11.29650097971809, 11.385140187566087, 11.238723319788773, 11.256758091709493, 11.290577778486133, 11.263768196878466, 11.365419895778215, 11.391640500973052, 11.258024648892436, 11.349216304959803, 11.363400349441457, 11.254709078634486, 11.403939704400296, 11.507297338948856, 11.442689381645261, 11.387662273462132, 11.322136234257558, 11.462816111054055, 11.347733678666176, 11.289666399408604, 11.271321891487119, 11.087644911452413, 10.984259881966711, 11.050626151548553, 11.255203637157809, 11.292528596326378, 11.419849195649196, 11.386325710028311, 11.000873742048441, 11.025743565389027, 11.290603409840386, 11.351283779576693, 11.251101401098555]
writer = csv.writer(file('ave_speed__day.csv','wb'))
fileNameList = []
for fileName in os.listdir(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\data'):
    fileNameList.append(fileName[9:17])
for i in range(len(fileNameList)):
    writer.writerow([fileNameList[i],ave_speed_all[i]])