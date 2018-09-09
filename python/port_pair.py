#coding:utf-8
#根据每条船划分的停泊事件，统计港口对的频数
import pandas as pd
import csv
import numpy as np

#写数据
writer = csv.writer(file('port_pair_frequency.csv','wb'))
writer.writerow(['beg_port','end_port','frequency'])
dict = {}
cape_nav = pd.read_csv('cape_nav_201509_201511.csv')
print len(cape_nav)  #2978
group_cape_nav = cape_nav.groupby('mmsi')
count = 0
for group in group_cape_nav:
    each_ship = np.array(group[1])   #一条船的多条停泊事件
    for i in range(len(each_ship) - 1):
                                                #port_name = each_ship[i][27]
        if each_ship[i][27].lower() == each_ship[i+1][27].lower():
            continue
        else:
            count += 1   #记录每条船的港口对的数量
            port_pair = (each_ship[i][27].lower(),each_ship[i+1][27].lower())
            if dict.has_key(port_pair):
                dict[port_pair] += 1
            else:
                dict[port_pair] = 1
print len(dict)  #186
for port in dict.keys():
    writer.writerow([port[0],port[1],dict[port]])




