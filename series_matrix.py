# -*- coding: utf-8 -*-
"""
Created on Wed Aug 22 22:49:07 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
from collections import Counter


with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod = pickle.load(fp)   
        
series = vod[vod['시리즈']==1]

member_total_count = vod['아이디+회원번호'].value_counts()
vod_total_count = vod['상품명2'].value_counts()

## creat matrix for 구매횟수 ( row : 상품명2, col : 회원번호) ##
        
# 회원번호        
member_count = series['아이디+회원번호'].value_counts()
member_count.describe()

member = member_count[member_count>=300].index.tolist()

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






#
  
import matplotlib.pyplot as plt

series['성별코드'].value_counts()
series['생년'].value_counts().sort_index()
series['생년'][series['성별코드']==1].plot.hist(range= tuple([1926, 2004]), bins=20, alpha=0.3, color ='r')
series['생년'][series['성별코드']==0].plot.hist(range= tuple([1926, 2004]), bins=20, alpha=0.3)

series['생년'][series['생년'].isnull() == True] = 0
series['생년'] = series['생년'].astype(int)


    
    
1978 - 1959
    
customers = vod[['아이디+회원번호', '생년', '성별코드']]
customers = customers.drop_duplicates()

member_total_count = member_total_count.reset_index()
member_total_count.columns = ['아이디+회원번호', '구매횟수']

customers = pd.merge(customers, member_total_count, on='아이디+회원번호')
    
customers['구매횟수'][customers['성별코드']==1].plot.hist(range = (0, 200), bins=30, alpha=0.3, color ='r')
customers['구매횟수'][customers['성별코드']==0].plot.hist(range = (0, 200), bins=30, alpha=0.3)


customers['구매횟수'][(customers['생년']<=1978) & (customers['생년']>1958)].plot.hist(range = (0, 200), bins=30, alpha=0.3, color ='r')
customers['구매횟수'][(customers['생년']<=1998) & (customers['생년']>1978)].plot.hist(range = (0, 200), bins=30, alpha=0.3)
    
customers['구매횟수'].describe()
customers['구매횟수'].plot.box()
    






