import csv
from sys import dllhandle
import pandas as pd
import numpy as np
import math
import glob,os

def muti_data(filepath,picp4,x1,x2,y1,y2):
    i=0
    p4 = 0
    p5 = 0

    path = filepath
    file = glob.glob(os.path.join(path,"*.csv"))
    print(file)
    dl = []
    for f in file:
        dl.append(pd.read_csv(f,header=2,usecols=["coords","x", "y"]))
    
    for i in range(len(dl)):
        data1 = dl[i]
        id = data1['coords']
        x = data1['x']
        y = data1['y']

        #計算距離
        for d1 in range(len(id)-1):
            p1 = np.array([x[d1],y[d1]])
            p2 = np.array([x[d1+1],y[d1+1]])
            p3 = p2-p1
            p4= math.hypot(p3[0],p3[1])
            p5 = p4 + p5
        data_distance = (p5/picp4)*80
        datadistance = str(data_distance)
        p5 = 0
        print(file[i]+"的總移動距離為*"+datadistance+"mm")


        data2 = data1[data1['x'].between(x1,x2)&data1['y'].between(y1,y2)]
        id2 = data2['coords']
        id2l = len(id2)
        i2 = 0
        id2count = 0
        #計算進出次數
        for i2 in range(id2l-1):
            idx1 = (id2.iloc[i2])
            idx2 = (id2.iloc[i2+1])
            if idx1+1 != idx2:
                id2count += 1
        print(file[i]+"進出中心*"+str(id2count)+"次")
        midtime = id2l/14.57
        print(file[i]+"中心停留時間為*"+str(midtime)+"秒")



#下面紅色也就是filepath那邊改成data所在文件夾的絕對路徑，picp4改成你的距離比例請善用data.py進行計算,x1-y2改成你要標點的中心區域4個標記，如果不知道坐標請善用picdata
muti_data(filepath=r'C:\Users\USER\Desktop\JKN-L-and-N\analysis',
            picp4=65.03076195155643,
            x1=197,
            x2=421,
            y1=113,
            y2=338)
