# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 22:49:07 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
from collections import Counter


with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_with_series.txt',"rb") as fp :
        vod = pickle.load(fp)   
        
series = vod[vod['시리즈']==1]


## creat matrix for 구매횟수 ( row : 상품명2, col : 회원번호) ##
        
# 회원번호        
member_count = series['아이디+회원번호'].value_counts()
member = member_count[member_count>150].index.tolist()

# 상품명2
title = np.unique(series['상품명2'])

# 회원번호 당 상품명2
trsc = [series['상품명2'][series['아이디+회원번호'] == i].values.tolist() for i in member]
trsc_counter = [Counter(trsc[i]) for i in range(len(trsc))] # unique title + counts
trsc2 = [[list(i.keys()), list(i.values())] for i in trsc_counter]

# create matrix
trsc_matrix = pd.DataFrame(index = title, columns= member)
trsc_matrix = trsc_matrix.reset_index()

# input value to matrix
for i in range(len(trsc2)) :
    trsc_matrix.iloc[:,(i+1)] = trsc_matrix['index'].apply(lambda x : trsc2[i][1][trsc2[i][0].index(x)] if x in trsc2[i][0] else 0)

