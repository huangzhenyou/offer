library(data.table)
library(ggplot2)
library ("ggmap")
library ("png")

ships_china = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\China_real_distri.csv")
ships_foreign = fread("D:\\1.������\\python_project\\ͣ���¼�\\Python����\\����\\foreign_real_distri.csv")

mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() +   mapWorld

#Now Layer the cities on top
mp <- mp+ geom_point(aes(x=ships_china$lon, y=ships_china$lat) ,color="green", size=3) 
mp <- mp+ geom_point(aes(x=ships_foreign$lon, y=ships_foreign$lat) ,color="red", size=3) 
mp