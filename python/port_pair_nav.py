# coding:utf-8
# 根据每条船划分的停泊事件
import pandas as pd
import csv
import numpy as np

# 写数据
writer = csv.writer(file('port_pair_nav.csv', 'wb'))
writer.writerow(['mmsi', 'begin_time', 'end_time', 'beg_port', 'end_port'])

#读数据
cape_nav = pd.read_csv('cape_nav_201509_201511.csv')
print len(cape_nav)
group_cape_nav = cape_nav.groupby('mmsi')
for group in group_cape_nav:
    each_ship = np.array(group[1])  # 一条船的多条停泊事件
    for i in range(len(each_ship) - 1):
        # port_name = each_ship[i][27]
        if each_ship[i][27].lower() == each_ship[i + 1][27].lower():  #如果两次停泊事件停的港口一样，就跳过
            continue
        else:  #出现港口对
            write_line = []
            write_line.append(each_ship[i][19]) #mmsi
            write_line.append(each_ship[i][22]) #end_time,这一行港口结束停泊的时间
            write_line.append(each_ship[i+1][21]) #beg_time 下一行港口结束停泊的时间
            write_line.append(each_ship[i][27].lower()) #beg_port
            write_line.append(each_ship[i+1][27].lower())  # end_port
            writer.writerow(write_line)





