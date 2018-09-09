#coding:utf-8
from __future__ import division
import pandas as pd
import csv
import numpy as np
import time
print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))

# 统计中国和国外的港口
# port = pd.read_csv('beg_port.csv')
# port_list = []
# port_list.extend(port['beg_port'])
# print port_list
china_port_1 = ['qingdao', 'tianjin', 'rizhao', 'yingkou', 'fangcheng', 'zhuhai', 'tangshan', 'qinzhou', 'xiamen',
              'yantai', 'ningbo', 'lianyungang', 'shanghai', 'zhanjiang', 'zhangjiagang', 'dandong', 'dalian',
              'guangzhou', 'qinhuangdao', 'quanzhou', 'zhenjiang', 'tianjian', 'longkou']
# print len(china_port_1)  # 24

# foreign_port = ['nouadhibou', 'lamma island', 'saldanha bay',  'rotterdam',  'kaohsiung', 'ashkelon','jubail',
#                 'mobile', 'gwangyang', 'muroran', 'oita', 'hamburg', 'mormugao', 'ka shima', 'roberts bank',
#                 'port hedland', 'eregli', 'kokura', 'iskenderun','safaga', 'piraeus', 'pohang', 'redcar',
#                 'kimitsu', 'ljmuiden', 'constantza', 'takehara', 'kure','singapre', 'taichung', 'hadera',
#                 'brisbane', 'kakogawa', 'ilychevsk', 'novorossiysk']
# print len(foreign_port)  #35

def port_country():
    port = np.array(pd.read_csv(u'D:\\1.王晓敏\\韩军老师\\数据\\港口信息csv格式.csv'))
    japan_port = []
    taiwan_port = []
    korea_port = []
    china_port = []
    for i in range(len(port)):
        if port[i,5].lower() == 'japan':
            japan_port.append(port[i,0].lower())
        elif port[i,5].lower() == 'taiwan':
            taiwan_port.append(port[i, 0].lower())
        elif port[i,5].lower() == 'korea':
            korea_port.append(port[i, 0].lower())
        elif port[i,5].lower() == 'china':
            china_port.append(port[i,0].lower())
    japan_port = list(set(japan_port))
    taiwan_port = list(set(taiwan_port))
    korea_port = list(set(korea_port))
    china_port = list(set(china_port))
    print len(japan_port),japan_port
    print len(taiwan_port),taiwan_port
    print len(korea_port),korea_port
    print len(china_port),china_port
    return
japan_port = ['kimitsu', 'matsushima', 'kakogawa', 'noshiro', 'misumi', 'oita', 'yokohama', 'kobe', 'yokkaichi', 'wakayama', 'ka shima', 'nagoya', 'takehara', 'chiba', 'haramichi', 'kokura', 'sakata', 'fukuyama', 'reihoku', 'kurasaki', 'ube', 'niihama', 'kochi', 'muroran', 'kinuura', 'tsuruga', 'hitachinaka', 'kure', 'toyama', 'nanao', 'kitakyushu', 'matsuzaka', 'hibikinada', 'tomakoma', 'ishikawa']
taiwan_port = ['taichung', 'keelung', 'hualien', 'kaohsiung']
korea_port = ['kunsan', 'samchok', 'pohang', 'gwangyang', 'busan', 'incheon']
china_port_2 = ['rizhao', 'dalian', 'sanya ', 'yingkou', 'beilun', 'zhenjiang', 'lamma island', 'dandong', 'shanghai', 'lianyungang', 'fangcheng', 'zhangjiagang', 'qinhuangdao', 'yantai', 'guangzhou', 'zhanjiang', 'xiamen', 'qingdao', 'haimen', 'yangzhou', 'shekou', 'tianjin', 'fuzhou', 'tangshan', 'ningbo']
china_port = list(set(china_port_1).union(china_port_2))  #并集
# a = list(set(china_port_1).intersection(china_port_2))  #交集
# b = list(set(china_port_1).difference(china_port_2))  #差集
#中国、日本、台湾、韩国的港口合并
china_port = japan_port + taiwan_port + korea_port + china_port
print len(china_port)

def real_distri_china():  #提出2015年11月1日的船，并判断是否是从中国的港口驶出
    writer = csv.writer(file('real_distri_china.csv','wb'))
    writer.writerow(['mmsi', 'acqui_time', 'lon', 'lat','beg_port','end_port','frequency','from_China'])
    #实时分布的时间段
    beg_utc = 1446307200   #2015/11/1 0点
    end_utc = 1446393600   #2015/11/2 0点
    AIS_between_port = pd.read_csv('port_pair_nav_AIS.csv')
    ship_AIS_between_port = AIS_between_port.groupby('mmsi')

    count = 0
    for group in ship_AIS_between_port:
        each_ship = np.array(group[1]) #每条船
        write_line = []
        from_china = False
        find = False
        for i in range(len(each_ship)): #一条船的每一行
            if each_ship[i,1] in range(beg_utc,end_utc): #如果在实时分布的时间段内
                find = True
                count += 1
                write_line.extend(each_ship[i]) #写入经纬度
                if each_ship[i,4] in china_port: #判断港口是否属于中国
                    from_china = True
                write_line.append(from_china) #写入判断结果
                break
        if find is True:
            print count
            print write_line
            writer.writerow(write_line)
        print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))

    print "总共有",len(ship_AIS_between_port),"条船"   #396
    print "2015年11月1日有",count,"条船"  #178
    print time.strftime('%Y/%m/%d %H:%M:%S',time.localtime(time.time()))
    return

def AIS_nav_port():
    count_ship = 0
    count_find = 0
    writer = csv.writer(file('distribution.csv','wb'))
    writer.writerow(['mmsi','acq_time','lon','lat','from_China'])
    nav = pd.read_csv('cape_nav_201509_201511.csv')
    nav = np.array(nav)
    ais = pd.read_csv(r'\\DESKTOP-AH1EE5F\2015-09-11csv\201511\ships_20151130.csv')  #
    ais_group = ais.groupby('unique_ID')
    for group in ais_group:
        count_ship += 1
        # print time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time()))
        # print count_ship
        write_line = []
        each_ship = np.array(group[1])
        id = each_ship[0][0]   #取每条船的第一条数据
        aqu_time = each_ship[0][1]
        lon = each_ship[0][5] / 1000000
        lat = each_ship[0][6] / 1000000
        max_time = 0
        max_time_index = 0
        for i in range(len(nav)):  #找这条船这个AIS数据点上次停泊过的最近的港口   #由于nav中的船只都是cape型船，所以a匹配后的船也属于cape型船
            if id == nav[i,19] and aqu_time > nav[i,21]: # nav[i,21] : beg_time
                if max_time < nav[i,21]:
                    max_time = nav[i,21]
                    max_time_index = i
        if max_time != 0:  #找到这条船的港口了
            count_find += 1
            print count_find
            print "find!"
            write_line.extend([id,aqu_time,lon,lat])
            port = nav[max_time_index,27]  #停泊事件的停泊港口
            if port.lower() in china_port:  #判断港口是否属于中国
                write_line.append(True)
            else:
                write_line.append(False)
            writer.writerow(write_line)
    print "在",count_ship,"条船中找到了",count_find,"条船上次停泊的港口"  #1150
    return

def china_or_not():   #把上面的结果分开，为了用R画图
    writer1 = csv.writer(file('China_real_distri.csv','wb'))
    writer2 = csv.writer(file('foreign_real_distri.csv','wb'))
    writer1.writerow(['mmsi', 'acqui_time', 'lon', 'lat','from_China'])
    writer2.writerow(['mmsi', 'acqui_time', 'lon', 'lat','from_China'])
    distri = np.array(pd.read_csv('distribution.csv'))   #改
    for i in range(len(distri)):
        # print distri[i,7],type(distri[i,7])
        # raw_input('=============')
        if distri[i,4] is True:   #如果是驶于中国的船   #改
            # raw_input('===================')
            writer1.writerow(distri[i])  #写入中国的文件  139
        else:
            writer2.writerow(distri[i]) # 39
    return

if __name__ == '__main__':
    #real_distri_china()
    AIS_nav_port()   #2015/11/30的港口
    china_or_not()