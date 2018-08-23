# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 18:00:26 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
from collections import Counter


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add.txt',"rb") as fp :
        vod = pickle.load(fp)  
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add_unique.txt',"rb") as fp :
        vu = pickle.load(fp)     
        
        
# unique vod    
def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique 


## series 칼럼 추가 - series(1), non-series(0) ##
vod.index = list(range(len(vod)))

non_series = vod[vod['회차']=='']
non_series_vu = unique_vod(non_series)

series = vod[vod['회차']!='']
series_vu = unique_vod(series)

non_series_vu_real = set(non_series_vu['title'].tolist()) -set(series_vu['title'].tolist())
non_series_vu_real = list(non_series_vu_real)

non_series = vod[vod['상품명2'].isin(non_series_vu_real)]
series = vod.drop(non_series.index)

len(series) + len(non_series) == len(vod)
len(unique_vod(non_series)) + len(unique_vod(series)) == len(vu)

non_series['시리즈'] = [0]*len(non_series)
series['시리즈'] = [1]*len(series)

vod_series = pd.concat([non_series, series])

#save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"wb") as fp :
        pickle.dump(vod_series,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod_series_test = pickle.load(fp)   

