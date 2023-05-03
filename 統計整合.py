# coding: utf-8
#v1.1  FST 靜止時間計算，計算兩角移動速度來判定

import csv
from sys import dllhandle
import pandas as pd
import numpy as np
import math
import glob,os


#####################################
#讀取csv檔並篩選資料col
#####################################
def datapath(filepath):
    path = filepath
    file = glob.glob(os.path.join(path,"*.csv"))
    dl = []
    for f in file:
        dl.append(pd.read_csv(f,header=2,usecols=["coords","x", "y"]))



#