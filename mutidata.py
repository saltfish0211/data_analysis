import csv
import pandas as pd
import numpy as np
import math
import glob,os

def muti_data(filepath):

    path = filepath
    file = glob.glob(os.path.join(path,"*.csv"))
    print(file)
    dl = []
    for f in file:
        dl.append(pd.read_csv(f))
    
    for i in range(dl):
        print(i)

muti_data(filepath=r'C:\Users\USER\Desktop\JKN')

