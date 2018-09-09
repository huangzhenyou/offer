#REFERENCE���жϵ��Ƿ��ڶ�����ڵķ����μ�
#           http://www.cnblogs.com/xiaozhi_5638/p/4165353.html

#���ڸ������㣨x��y)�����㾭������ķ���ax+by+c=0
#�����a��b��c��
#cor1,cor2�� ����
linePara = function(cor1, cor2){
  if(all(cor1 == cor2)){
    print("not a line, but a point")

  }
  else{
    if(cor2[1] != cor1[1]){
      a = (cor2[2] - cor1[2]) / (cor2[1] - cor1[1])
      b = -1
      c = (cor1[2] * cor2[1] - cor2[2] * cor1[1]) / (cor2[1] - cor1[1])
    }
    else{
      a = 1
      b = 0
      c = -cor1[1]
    }
    return (c(a,b,c))
  }
}

#���ڸ����� (x,y) �Լ�(a,b,c)
#���ɺ��� f(x,y) = ax + by + c�� ����f����ֵ
#cor�� �������
#para�� ��a,b,c)
linefunc = function(cor, para){
  return (para[1] * cor[1] + para[2] * cor[2] + para[3])
}

#���ڸ���yֵ,��a��Ϊ0ʱ������ax+by+c=0��x��ֵ
get_x = function(y, para){
  x = -(para[2] * y + para[3])/para[1] 
  return (x)
}

#���ڸ���xֵ,��b��Ϊ0ʱ������ax+by+c=0��y��ֵ
get_y = function(x, para){
  y = -(para[1] * x + para[3])/ para[2]
  return(y)
}

#�жϸ�����ֵx�Ƿ�����ֵx1��x2�м�
between = function(x, x1, x2){
  if(x <= max(x1, x2) && x >= min(x1, x2)){
    return (TRUE)
  }
  else{
    return (FALSE)
  }
}

#�ж��������Ƿ��غ�
point_point = function(cor1, cor2){
  if(all(cor1 == cor2)){
    return (TRUE)
  }
  else{
    return (FALSE)
  }
}

#�жϵ��������cor1 �Ƿ������� line_cor1, line_cor2 �����ӳɵ��߶���
point_line = function(cor1, line_cor1, line_cor2){
  if(all(line_cor1 == line_cor2)){
    return(point_point(cor1, line_cor1))
  }
  else{
    if(between(cor1[1], line_cor1[1], line_cor2[1]) && 
       between(cor1[2], line_cor1[2], line_cor2[2])){
      if(linefunc(cor1, linePara(line_cor1,line_cor2)) == 0){
        return (TRUE)
      }
    }
    return (FALSE)
  }
}

#�ж�line1_cor1,line1_cor2���ӳɵ��߶��Ƿ���line2_cor1,line2_cor2�����߶��ཻ
line_line = function(line1_cor1,line1_cor2, line2_cor1, line2_cor2){
  if(point_point(line1_cor1,line1_cor2)){
    return(point_line(line1_cor1, line2_cor1, line2_cor2))
  }
  para1 = linePara(line1_cor1,line1_cor2)
  para2 = linePara(line2_cor1,line2_cor2)
  if(all(para1 == para2)){
    return (TRUE)
  }
  else{
    if(all(para1[1:2] == para2[1:2])){
      return (FALSE)
    }
    else{
      if(para1[2] == para2[2]){
        x = (para2[3] - para1[3]) / (para1[1] - para2[1])
        y = get_y(x, para1)
      }
      else{
        if(para1[2] == 0){
          x = -para1[3]
          y = get_y(x, para2)
        }
        else{
          x = -para2[3]
          y = get_y(x, para1)
        }
        
      }
      if(between(x, line1_cor1[1], line1_cor2[1]) &
         between(x, line2_cor1[1], line2_cor2[1]) &
         between(y, line1_cor1[2], line1_cor2[2]) &
         between(y, line2_cor1[2], line2_cor2[2])){
        return (TRUE)
      }
      else{
        return (FALSE)
      }
    }
  }
}

#�жϵ��Ƿ��ڶ���Σ������飩��
point_polygon = function(cor, polygon){
  n = dim(polygon)[1]
  if(n > 2){
    count = 0
    i = 1
    while(i <= n){
      line_cor1 = polygon[i,]
      i = i + 1
      if(i > n){
        line_cor2 = polygon[1,]
      }
      else{
        line_cor2 = polygon[i,]
      }
      if(point_line(cor, line_cor1, line_cor2)){
        return (TRUE)
      }
      else{
        if(!point_point(line_cor1, line_cor2) && 
           line_cor1[2] != line_cor2[2]){
          if(between(cor[2], line_cor1[2], line_cor2[2])){
            if(cor[1] <= max(line_cor1[1], line_cor2[1])){
              if(get_x(cor[2], linePara(line_cor1, line_cor2)) >= cor[1]){
                count = count + 1
              }
            }
          }
        }
      }
    }
    if(count %% 2 == 1){
      return (TRUE)
    }
    else{
      return (FALSE)
    }
  }
  if(n == 0){
    return (FALSE)
  }
  if(n == 1){
    return (point_point(cor, polygon[1]))
  }
  if(n == 2){
    return (point_line(cor, ploygon[1], polygon[2]))
  }
}

point_point_q = function(ship, polygon){
  cor = dim(polygon)[1]
  i = 1
  j = cor
  inside = FALSE
  for(i in 1:cor){
    if(((polygon[i,2] < ship$latitude & polygon[j,2] >= ship$latitude)
        | (polygon[j,2] < ship$latitude & polygon[i,2] >= ship$latitude))
       & (polygon[i,1] <= ship$longitude | polygon[j,1] <= ship$longitude)){
      a = (polygon[i,1] + 
             (ship$latitude - polygon[i,2])/(polygon[j,2] - polygon[i,2]) * 
             (polygon[j,1] - polygon[i,1]))
      if(a < ship$longitude){
        inside = !inside
      }
    }
    j = i
  }
  return(inside)
}

#�ж� ���������߶� �Ƿ��ڶ������
#polygon����������Σ���ά����
line_polygon = function(cor1, cor2, polygon){
  n = dim(polygon)[1]
  for(i in 1 : n){
    line_cor1 = polygon[i,]
    if(i != n){
      line_cor2 = polygon[i + 1,]
    }
    else{
      line_cor2 = polygon[1, ]
    }
    if(line_line(cor1,cor2,line_cor1, line_cor2)){
      return (TRUE)
    }
  }
  if(point_polygon(cor1, polygon) || point_polygon(cor2, polygon)){
    return (TRUE)
  }
  return (FALSE)
}

#�жϵ��Ƿ��ڸ���Բ��
#center: Բ������
#radius�� �뾶 ����λkm��
point_circle = function(cor, center, radius){
  library(Imap)
  if(gdist(cor[1],cor[2],center[1],center[2],unit = "km") <= radius){
      return (TRUE)
  }
  else{
    return (FALSE)
  }
}
 
#�ж��߶��Ƿ��ڸ���Բ��
#center: Բ������
#radius�� �뾶 ����λkm��
line_circle = function(line_cor1, line_cor2, center, radius){
  if(point_circle(line_cor1,center,radius) || 
      point_circle(line_cor2, center, radius)){
    return (TRUE)
  }
  else{
    return (FALSE)
  }
}

#�жϵ��Ƿ���������,Ĭ��Ϊ����
contain_area = function(lon, lat, lon_right = 174.77618055555556, lon_left = 29.91921388888889, lat_bot = -16.933333333333334,
                        lat_top = 59.326008333333334){
#   lon_right = 174.77618055555556 #�����
#   lon_left = 29.91921388888889 #����ɽ���
#   lat_bot = -16.933333333333334 #����˹
#   lat_up = 59.326008333333334 #Ĭ�¸��Ħ
  if((lon < lon_right)&(lon > lon_left)&(lat > lat_bot)&(lat < lat_top)){
    return (1)
  }
  else{
    return (0)
  }
}


