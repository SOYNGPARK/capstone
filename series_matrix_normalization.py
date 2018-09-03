# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:30:20 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import datetime
import pickle
from collections import Counter


with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod = pickle.load(fp)   
        
series = vod[vod['시리즈']==1]

# 회원번호        
member_count = series['아이디+회원번호'].value_counts()
member_count.describe()

member = member_count[member_count>=300].index.tolist()

#
data = series[series['아이디+회원번호'].isin(member)][['아이디+회원번호', '상품명2', '거래일시']]

data['거래일시'] = pd.to_datetime(data['거래일시'])
day = datetime.datetime(2017,1,1)

data['거래일시2'] = data['거래일시'].apply(lambda x : (x - day).days)

#
genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\hasGenreVOD.csv')

merge = pd.merge(data, genre, how='left', on='상품명2')

#
drama = merge[merge['Genre']=='드라마']

# 기간
recent = drama[drama['거래일시2']>334] # 최근 30일
once = drama[drama['거래일시2']<275] # 1달 전 부터 11개월 동안
before = drama[drama['거래일시2']<=334] # 3달 전 부터 9개월 동안


# 상품명2
title = np.unique(drama['상품명2'])

def create_matrix(series) : 

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

    # index 정리
    trsc_matrix.index = trsc_matrix['index']
    del trsc_matrix['index']
    
    return trsc_matrix


recent_matrix = create_matrix(recent)
once_matrix = create_matrix(once)
before_matrix = create_matrix(before)

all_matrix = create_matrix(drama)

# 나름 단순 정규화
norm_matrix = all_matrix

for i in range(len(norm_matrix)) :
    mx = max(norm_matrix.iloc[i,:].values)
    mn = min(norm_matrix.iloc[i,:].values)
    
    for j in range(len(norm_matrix.iloc[0])) :
        norm_matrix.iloc[i,j] = (norm_matrix.iloc[i,j] - mn) / (mx-mn) * 0.2


final_matrix = norm_matrix

for i in range(len(final_matrix)) :
    for j in range(len(final_matrix.iloc[0])) :
        if recent_matrix.iloc[i,j] >= 3 : # 최근 1달 내에 3회 이상 시청
            final_matrix.iloc[i,j] = final_matrix.iloc[i,j] + 0.8
        elif before_matrix.iloc[i,j] >= 10 : # 1달 전 부터 11달 동안 10회 이상 시청
            final_matrix.iloc[i,j] = final_matrix.iloc[i,j] + 0.7
        elif once_matrix.iloc[i,j] <= 2 &  once_matrix.iloc[i,j] >= 1: # 3개월 이전에 2번 이하 시청하고 최근 3개월간 시청하지 않음
            final_matrix.iloc[i,j] = -100
        




























