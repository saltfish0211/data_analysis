import csv
import pandas as pd
import numpy as np
import math
# import cv2


data1 = pd.read_csv("data2.csv" ,header=2,usecols=["coords","x", "y"])
data1.head()





#計算兩點坐標距離
def picdata(p1x,p1y,p2x,p2y):
    picp1 = np.array([p1x,p1y])
    picp2 = np.array([p2x,p2y])
    picp3 = picp1 - picp2
    picp4 = math.hypot(picp3[0],picp3[1])
    # picp5=round(picp4)
    picdis = str(picp4)
    print("兩點坐標的距離為"+picdis)

#計算總移動距離和中心進出次數
def data_dis(filename,picp4,x1,x2,y1,y2):
    data1 = pd.read_csv(filename,header=2,usecols=["coords","x", "y"])
    data2 = data1[data1['x'].between(x1,x2)&data1['y'].between(y1,y2)]
    id = data1['coords']
    x = data1['x']
    y = data1['y']
    id2 = data2['coords']
    id2l = len(id2)
    idc = len(id)
    p4 = 0
    p5 = 0
    id2count = 0
    #計算距離
    for i in range(idc-1):
        p1 = np.array([x[i],y[i]])
        p2 = np.array([x[i+1],y[i+1]])
        p3 = p2-p1
        p4= math.hypot(p3[0],p3[1])
        p5 = p4 + p5
    data_distance = (p5/picp4)*8
    # dis=round(data_distance)
    datadistance = str(data_distance)
    print("總移動距離為"+datadistance+"cm")
    #計算進出次數
    for i2 in range(id2l-1):
        idx1 = (id2.iloc[i2])
        idx2 = (id2.iloc[i2+1])
        if idx1+1 != idx2:
            id2count += 1
    print("中心區域進入次數為"+str(id2count)+"次")



# 使用下面兩行程式碼就好


picdata(p1x=180,
        p1y=202,
        p2x=190,
        p2y=254)#輸入圖片2點坐標，如果啥都沒有就不用動


