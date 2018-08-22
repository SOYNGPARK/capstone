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
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final.txt',"rb") as fp :
        vod = pickle.load(fp)  
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_unique.txt',"rb") as fp :
        vu = pickle.load(fp)     
        
        
# unique vod    
def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique 


## series 칼럼 추가 - series(1), non-series(0) ##
non_series = vod[vod['회차']=='']
non_series_vu = unique_vod(non_series)

series = vod[vod['회차']!='']
series_vu = unique_vod(series)

non_series_real = set(non_series_vu['title'].tolist()) -set(series_vu['title'].tolist())
non_series_real = list(non_series_real)

non_series = vod[vod['상품명2'].isin(non_series_real)]
series = vod.drop(non_series.index)

non_series_vu = unique_vod(non_series)
series_vu = unique_vod(series)

non_series['시리즈'] = [0]*len(non_series)
series['시리즈'] = [1]*len(series)

vod = pd.concat([non_series, series])

#save
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_with_series.txt',"wb") as fp :
#        pickle.dump(vod,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_with_series.txt',"rb") as fp :
        vod_test = pickle.load(fp)   


## creat matrix for 구매횟수 ( row : 상품명2, col : 회원번호) ##
        
## example ##

# 회원번호        
member = np.unique(series['아이디+회원번호'])

# 상품명2
title = np.unique(series['상품명2'])

# 회원번호 당 상품명2
trsc = [series['상품명2'][series['아이디+회원번호'] == i].values.tolist() for i in member[:10]]
trsc_counter = [Counter(trsc[i]) for i in range(len(trsc))] # unique title + counts
trsc2 = [[list(i.keys()), list(i.values())] for i in trsc_counter]

# create matrix
trsc_matrix = pd.DataFrame(index = title, columns= member[:10])
trsc_matrix = trsc_matrix.reset_index()

# input value to matrix
for i in range(len(trsc2)) :
    trsc_matrix.iloc[:,(i+1)] = trsc_matrix['index'].apply(lambda x : trsc2[i][1][trsc2[i][0].index(x)] if x in trsc2[i][0] else 0)









