# 在孙璟的程序基础上进行如下修改：
# 1.以D_DST为距离阈值对船的轨迹进行分段，大于D_DST不进行连接。D_DST对不用区域需要进行调整
# 2.最后画图时对value字段进行变换,变换公式请看D:\Rworkspace\data\heat_calc_main_qiu的改动说明.docx


setwd("D:/Rworkspace")
library(ggplot2)
library(ggmap)
library(Imap)
library(data.table)
source("intersect_func.R")
source("heat_calc.R")

#设置给定中心点周围范围
map = get_googlemap(c(103.766667,1.233333), zoom = 9, maptype = "satellite")  #改图层
ggmap(map)

range = c(0, 2.5, 102.5, 105)
###################################################################################################

#数据排序
data = fread("E:\\转换好的船讯网数据\\2014-09转换\\ships_20140901.csv")

data = data[data$latitude > range[1] & data$latitude < range[2] &           #去掉
              data$longitude > range[3] & data$longitude < range[4],]       #去掉
data = data.frame(unique_ID = data$unique_ID, acquisition_time = data$acquisition_time, 
                  longitude = data$longitude, latitude = data$latitude)
data = data[order(data$unique_ID, data$acquisition_time),]

a = read.csv("./data/t41_ship_id_imo_type700_name.csv")  #去掉
b = read.csv("./data/t41_ship_id_imo_type800.csv")  #去掉
ship700 = a$mmsi[!is.na(a$mmsi)]   #去掉
ship800 = b$mmsi[!is.na(b$mmsi)]   

id700 = match(data$unique_ID, ship700)
id700 = !is.na(id700)

id800 = match(data$unique_ID, ship800)
id800 = !is.na(id800)          #去掉

#设置各个船舶类型参数
ship_coef = numeric(dim(data)[1]) + 1
ship_coef[id700] = 10
ship_coef[id800] = 10
data = data.frame(data, ship_coef)


###################################################################################################
#设置精度
grade = 1000
D_DST = 1000

data$longitude = data$longitude * grade
data$latitude = data$latitude * grade

#计算格子中心点坐标
la_range = seq(range[1], range[2], by = 1/grade) # 生成等差数列
lon_range = seq(range[3], range[4], by = 1/grade)

la_center = sapply(1:(length(la_range) - 1), function(x){ return ((la_range[x] + la_range[x + 1]) / 2)},
                   simplify = T)
lon_center = sapply(1:(length(lon_range) - 1), function(x){ return ((lon_range[x] + lon_range[x + 1]) / 2)},
                    simplify = T)

#获得给定精度下范围数据以及坐标分割线
range =range * grade
la_range = as.integer(range[1]:range[2])
lon_range = as.integer(range[3]:range[4])

#创建点矩阵
points = matrix(0, ncol = length(la_center), nrow = length(lon_center))
rownames(points) = lon_center
colnames(points) = la_center

###################################################################################################
#排除采样点为1的船舶
t = as.matrix(table(data$unique_ID)) # t代表一条船有几条数据
name = as.numeric(rownames(t)[which(t == 1)])
idx = match(data$unique_ID, name)
data = data[is.na(idx),]

# 用D_DST对船舶轨迹进行分段
n = dim(data)[1]
i = 1
#找航行中的数据
start = 1  #去掉
end = 0
run_range = NULL
for(i in 1:(n - 1)){
  if(data$unique_ID[i] != data$unique_ID[i + 1]){
    end = i
    temp_range = c(data$unique_ID[start], data$acquisition_time[start], data$acquisition_time[end])
    run_range = rbind(run_range, temp_range)
  }
  start = end + 1
  cat(paste(round(i/n, 3), "\n"))
}
end = n
temp_range = c(data$unique_ID[start], data$acquisition_time[start], data$acquisition_time[end])
run_range = rbind(run_range, temp_range)

run_range = data.frame(mmsi = as.numeric(run_range[,1]),start =  as.numeric(run_range[,2]), end = as.numeric(run_range[,3])) #去掉
######
str = 1
edr = 1
ships_data = NULL
ship_len = dim(data)[1]
num_group = 0
temp_group = -1
n = dim(run_range)[1]

# # id = match(data$unique_ID, run_range$mmsi[i])
# # id = !is.na(id)
# # temp_ship = data[id,]
# # idx = which((temp_ship$acquisition_time >= run_range$start[i])&(temp_ship$acquisition_time <= run_range$end[i]))
# temp_ship = temp_ship[idx,]
# temp_num = dim(temp_ship)[1]
# temp_group = temp_group + 1
# group = NULL
# group = rbind(group, temp_group)
# #cat(paste(run_range$mmsi[i], "\n"))
# if(temp_num >= 2){
#   for(j in 1:(temp_num - 1)){
#     temp_dst = gdist(temp_ship$longitude[j], temp_ship$latitude[j], temp_ship$longitude[j + 1], temp_ship$latitude[j + 1])
#     if(temp_dst < D_DST){
#       temp_group = num_group
#       group = rbind(group, temp_group)
#       # temp_ship[j,] = c(temp_ship[j,], group)
#     }
#     else{
#       num_group = num_group + 1
#       temp_group = num_group
#       group = rbind(group, temp_group)
#       # temp_ship[j,] = c(temp_ship[j,], group)
#     }
#   }
#   temp_ship = cbind(temp_ship, group)
#   ships_data = rbind(ships_data, temp_ship)
#   num_group = num_group + 1
# }
# # group = rbind(group, temp_group)
# cat(paste(round(i/n, 3), "\n"))


#排除采样点为1的船舶
t1 = as.matrix(table(ships_data$group)) # t代表一条船有几条数据
name1 = as.numeric(rownames(t1)[which(t1 == 1)])
idx1 = match(ships_data$group, name1)
ships_data = ships_data[is.na(idx1),]

n = dim(ships_data)[1]
# 将group作为新的unique_ID
ships_data = data.frame(unique_id = ships_data$group, acquisition_time = ships_data$acquisition_time, longitude = ships_data$longitude,
                        latitude = ships_data$latitude, ship_coef = ships_data$ship_coef)
data = ships_data
i = 1

#对于给定所有数据计算每个格子值
while(i <= n){
  ship_id = data$unique_id[i]
  id = which(data$unique_id == ship_id)
  ship = as.matrix(data[id, ])
  if(dim(ship)[1] > 2){
    temp = lapply(1:(dim(ship)[1] - 1), function(i){
      return (convert_matrix(i, ship, lon_range, la_range, grade))})
    temp = do.call(rbind, temp)
  }
  else{
    temp = convert_matrix(1, ship, lon_range, la_range, grade)
  }
  if(!is.null(temp)){
    temp = aggregate(dist ~ m_lo + m_la, sum, data = temp)
    points[cbind(temp[,1], temp[,2])] = points[cbind(temp[,1], temp[,2])] + temp[,3]
  }
  cat(paste("ship id:", ship_id, "\n"))
  i = max(id) + 1
}
#转换矩阵
p = gen_points(points, lon_center, la_center)
###################################################################################################

#输出图像
p = data.frame( lon = p[,1], la = p[,2], value = p[,3])
pp = p[p$value > 0,]
pp$value = scale(pp$value)

theme_set(theme_bw(base_size = 8))

color = c(rgb(226, 17, 0, maxColorValue = 255),
          rgb(254,67,101, maxColorValue = 255), 
          rgb(252,157,154,maxColorValue = 255),
          rgb(249, 105, 173,maxColorValue = 255), 
          rgb(200,200,169,maxColorValue = 255),
          rgb(131,175,155,maxColorValue = 255))


ggmap(map) + 
  geom_point(data = pp, aes(x = lon, y = la, colour = (log(value + 1) ^ 2 + log(value + 1))/2, group=group),alpha = 0.1, size = 2, shape = 16) +
  scale_colour_gradientn(colours = rev(color))
