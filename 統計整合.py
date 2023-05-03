# coding: utf-8
#v1.2  FST 靜止時間計算，計算兩角移動速度來判定

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

#####################################
#將讀取與計算寫在一起，不過現在是計算單點
#####################################

def calculate_still_time(data, distance_threshold, ids_per_second=60):
    data = data.sort_values(by=['id'])
    still_time = 0
    ids_still = 0

    for animal_id in data['id'].unique():
        animal_data = data[data['id'] == animal_id]
        for i in range(1, len(animal_data)):
            prev_point = animal_data.iloc[i - 1]
            curr_point = animal_data.iloc[i]

            distance = ((curr_point['x'] - prev_point['x'])**2 + (curr_point['y'] - prev_point['y'])**2)**0.5
            if distance <= distance_threshold:
                ids_still += 1

    still_time = ids_still / ids_per_second
    return still_time

# 讀取 CSV 文件
file_path = 'path/to/your/data.csv'
data = pd.read_csv(file_path)

# 設置靜止閾值，例如 0.5
distance_threshold = 0.5

# 計算動物靜止不動的總時間（單位：秒）
total_still_time = calculate_still_time(data, distance_threshold)
print(f"動物靜止不動的總時間：{total_still_time} 秒")
