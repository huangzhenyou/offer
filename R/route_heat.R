library(ggplot2)
library(ggmap)
library(Imap)
library(data.table)
library(png)

#画图层
mp <- NULL
mapWorld <- borders("world", colour="gray50", fill="gray50") # create a layer of borders
mp <- ggplot() + mapWorld
mp

range = c(-90,90,-180,180)   #设置纬度和经度范围

#数据读取,一个num代表一段轨迹
# data = fread("D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\paintData.csv")#cape港口对间的AIS轨迹
data = fread("D:\\1.王晓敏\\python_project\\停泊事件\\Python代码\\韩军\\R_clean_AIS_cape_all.csv")#cape的AIS轨迹
data = data.frame(unique_ID = data$unique_id, acquisition_time = data$acqusition_time, 
                  longitude = data$lon, latitude = data$lat, num = data$num)


#设置各个船舶类型参数
ship_coef = numeric(dim(data)[1]) + 1
ship_coef = 10
data = data.frame(data, ship_coef)

###################################################################################################
#设置精度
grade = 10   #精度值应该调一点
D_DST = 1000

data$longitude = data$longitude * grade   #乘精度的作用是？？
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

n = dim(data)[1]
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


mp + 
  geom_point(data = pp, aes(x = lon, y = la, colour = (log(value + 1) ^ 2 + log(value + 1))/2),alpha = 0.1, size = 2, shape = 16) +
  scale_colour_gradientn(colours = rev(color))
mp
