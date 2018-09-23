# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:30:20 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import datetime


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod = pickle.load(fp)     

genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\genre.csv')
del genre['movieCd']


# vod 파생변수 거래일시2 : 2018년 1월 1일 기준으로 얼마나 전인지
vod['거래일시'] = pd.to_datetime(vod['거래일시'])
day = datetime.datetime(2018,1,1)

vod['거래일시2'] = vod['거래일시'].apply(lambda x : (day-x).days)


# merge data
merge = pd.merge(vod, genre, how='left', on='상품명2')

# data
data = merge[merge['Genre'] == '드라마'][['아이디+회원번호', '상품명2', '거래일시2']]

# 상품명2
items = data['상품명2'].value_counts()
items = items.index.tolist()


# creat matrix for how many times each user sees each item

# list all users and all items
fixed_group = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count()
fixed_group[:] = -100

fixed_group = fixed_group.rename('count1')
fixed_group = fixed_group.reset_index(level='아이디+회원번호')
fixed_group = fixed_group.reset_index()


def create_matrix(data) : 
    ## INPUT : data(DataFrame, col : 상품명2(item), 아이디+회원번호(user)) ##
    ## OUTPUT : matrix(DataFrame, col : 상품명2(item), row : 아이디+회원번호(user)) ##
    
    data_group = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count()
    
    # unset index
    data_group = data_group.rename('count')
    data_group = data_group.reset_index(level='아이디+회원번호')
    data_group = data_group.reset_index()
    
    # create fixed size(# of users X # of items) matrix by joining fixed_group
    data_group = pd.merge(data_group, fixed_group, how='outer', on=['상품명2', '아이디+회원번호'])
    del data_group['count1']
    
    data_group['count'] = data_group['count'].fillna(0)
    #data_group['count'] = data_group['count'].astype(int)
   
    # set index
    data_group = data_group.set_index(['아이디+회원번호', '상품명2'])
    data_group = data_group['count']
    
    # to matrix
    matrix = data_group.unstack('상품명2')
    matrix = matrix.fillna(0)
      
    return matrix


# 기간
recent = data[data['거래일시2']<=30] # 최근 30일(12월)
once = data[data['거래일시2']>30] # 30일 이전

# 기간 matrix
recent_matrix = create_matrix(recent)
once_matrix = create_matrix(once)

all_matrix = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count().unstack('상품명2')
all_matrix = all_matrix.fillna(0)

norm_matrix = all_matrix.divide(all_matrix.max(0), axis=1)

# infer score for drama

# 1) 30일 전까지 1~2번 시청한게 전부인 item = 0.001
once_matrix[(once_matrix<=2) & (once_matrix>0) & ((all_matrix - once_matrix) == 0)] = 0.001
once_matrix[once_matrix>2] = 0

# 2) 최근 30일 내에 3번 이상 시청한 item = 0.8 
recent_matrix[recent_matrix<3] = 0
recent_matrix[recent_matrix>=3] = 0.8

# 3) 전체 기간 동안 10번 이상 시청한 item = 0.7
all_matrix[all_matrix<10] = 0
all_matrix[all_matrix>=10] = 0.7

# 2) + 3)
all_matrix[(recent_matrix -all_matrix) > 0] = recent_matrix

# 4) 특정 기간에 몇 회 이상 시청했는지 여부(1,2)에 따라 80% weight + 기간에 상관없이 시청횟수 정규화로 20% weight
final_matrix = norm_matrix * 0.2 + all_matrix 

# 1) + 4)
final_matrix[(once_matrix -all_matrix) == 0.001] = once_matrix


# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"wb") as fp :
        pickle.dump(final_matrix,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"rb") as fp :
        test = pickle.load(fp)



# test

all_matrix1 = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count().unstack('상품명2')
all_matrix1 = all_matrix1.fillna(0)

recent_matrix1 = create_matrix(recent)
once_matrix1 = create_matrix(once)

am = all_matrix.T['KTPGMTV001_8136063']
rm = recent_matrix.T['KTPGMTV001_8136063']
om = once_matrix.T['KTPGMTV001_8136063']

am1 = all_matrix1.T['KTPGMTV001_8136063']
rm1 = recent_matrix1.T['KTPGMTV001_8136063']
om1 = once_matrix1.T['KTPGMTV001_8136063']

nm = norm_matrix.T['KTPGMTV001_8136063']
nm2 = nm*0.2

fm = test.T['KTPGMTV001_8136063']

m = pd.concat([am1, rm1, om1, am, rm, om, nm, nm2, fm], axis=1)
m.columns = ['전체시청횟수', '최근시청횟수', '예전시청횟수', 
             '전체시청점수', '최근시청점수', '예전시청점수', '정규화', '정규화*0.2', '선호도']
m = m.sort_values(['전체시청횟수'], ascending=[False])











