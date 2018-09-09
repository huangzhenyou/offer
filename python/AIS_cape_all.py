# coding:utf-8
import pandas as pd
import os
import csv
import numpy as np
fileNameList = []
for fileName in os.listdir(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\data'):
    fileNameList.append(fileName)

# writer = csv.writer(file('AIS_cape_ALL.csv','wb'))
# writer.writerow(['unique_id','acu_time','lon','lat','speed','conversion','cog','true_header'])
# writer.close()

ais_cape_all = pd.DataFrame(data=None,columns=['unique_id','acqusition_time','lon','lat','speed','conversion','cog','true_header'],index=None)
print len(fileNameList)
for day in range(len(fileNameList)):  #对每个文件操作
    print "计算第", day, "的数据"
    each_day = pd.read_csv(u'D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\AIS_cape\\data\\' + fileNameList[day])
    ais_cape_all = ais_cape_all.append(each_day)
    # print ais_cape_all.head()
    # raw_input('===')
print ais_cape_all.head()
raw_input('=====')
ais_cape_all.to_csv('AIS_cape_ALL.csv',index=None)