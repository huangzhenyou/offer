############################################################################################

library(data.table)
# data = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\VLOC_AIS_201509_11_withGroup2.csv")#VLOC��AIS�켣
# data = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\VLOC_AIS_201409_11_withGroup2.csv")#VLOC��AIS�켣
data = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\paintData.csv") #cape�ۿڶԼ�켣
# data = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\R_clean_AIS_cape_all.csv")#cape��AIS�켣

library(ggplot2)
library ("ggmap")
library ("png")
mark = data.frame(lon = as.numeric(data$lon),la =  as.numeric(data$lat), group = data$num)
# mark = data.frame(lon = as.numeric(data$lon),la =  as.numeric(data$lat), group = data$pair)
#mapWorld <- borders("china", colour="gray50", fill="gray50") # create a layer of borders
#mp <- ggplot() +   mapWorld

#412406910, 412407040, 412414370, 41389400, 414033000
#res <- mp + geom_path(aes(x = mark$lon, y = mark$la, group=mark$group_pair), color = "red4", alpha = 1, size = 20)

mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() +   mapWorld

mp + geom_path(data = mark, aes(x = lon, y = la, group = group), color = "red4", alpha = 0.1, size = 1)