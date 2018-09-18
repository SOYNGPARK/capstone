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


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod = pickle.load(fp)     

genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\hasGenreVOD_update.csv')
del genre['Unnamed: 0']


# vod 파생변수 거래일시2 : 2018년 1월 1일 기준으로 얼마나 전인지
vod['거래일시'] = pd.to_datetime(vod['거래일시'])
day = datetime.datetime(2018,1,1)

vod['거래일시2'] = vod['거래일시'].apply(lambda x : (day-x).days)


# merge data
merge = pd.merge(vod, genre, how='left', on='상품명2')


# 장르 : drama
drama = merge[merge['Genre'] == '드라마']

# 회원번호 : 3번 이상 구매한 회원       
users_count = drama['아이디+회원번호'].value_counts()
users_count.describe()

users = users_count[users_count>=3].index.tolist()

data = drama[drama['아이디+회원번호'].isin(users)][['아이디+회원번호', '상품명2', '거래일시2']]

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
    
    data_group = recent['상품명2'].groupby([recent['아이디+회원번호'], recent['상품명2']]).count()
    
    # unset index
    data_group = data_group.rename('count')
    data_group = data_group.reset_index(level='아이디+회원번호')
    data_group = data_group.reset_index()
    
    # fix size
    data_group = pd.merge(data_group, fixed_group, how='outer', on=['상품명2', '아이디+회원번호'])
    del data_group['count1']
    
    data_group['count'] = data_group['count'].fillna(0)
    data_group['count'] = data_group['count'].astype(int)
   
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
#all_matrix = create_matrix(data)

# normalization
def to_norm(matrix) :
    
    mx = matrix.max(0)
    mn = matrix.min(0)
    
    matrix = (matrix - mn) / (mx - mn)
    
    return matrix
 
  
norm_matrix = to_norm(all_matrix)


# infer score for drama
once_matrix[(once_matrix<=2) & (once_matrix>0) & ((all_matrix - once_matrix) == 0)] = 0.001
once_matrix[once_matrix>2] = 0

recent_matrix[recent_matrix<3] = 0
recent_matrix[recent_matrix>=3] = 0.8

all_matrix[all_matrix<10] = 0
all_matrix[all_matrix>=10] = 0.7

all_matrix[(recent_matrix -all_matrix) > 0] = recent_matrix

final_matrix = norm_matrix * 0.2 + all_matrix
final_matrix[(once_matrix -all_matrix) == 0.001] = once_matrix


# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\final_matrix.txt',"wb") as fp :
        pickle.dump(final_matrix,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\final_matrix.txt',"rb") as fp :
        test = pickle.load(fp)



# test

all_matrix = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count().unstack('상품명2')
all_matrix = all_matrix.fillna(0)

am = all_matrix.T['KTPGMTV001_8136063']
rm = recent_matrix.T['KTPGMTV001_8136063']
om = once_matrix.T['KTPGMTV001_8136063']
fm = test.T['KTPGMTV001_8136063']


m = pd.concat([am, rm, om,fm], axis=1)
m.columns = ['전체시청횟수', '최근 시청횟수', '예전 시청횟수', '선호도']
m = m.sort_values(['전체시청횟수'], ascending=[False])



#
## score = if recent > before : recent, else before
#group['score'] = group.apply(lambda x : x[0] if x[0] > x[1] else x[1], axis=1)
#
## score1 = if score == 0 : once, else score
#group['score1'] = group.apply(lambda x : x[2] if x[3] == 0 else x[3], axis=1)



#for i in range(len(final_matrix)) :
#    print(i)
#    for j in range(len(final_matrix.iloc[0])) :
#        if recent_matrix.iloc[i,j] >= 3 : # 최근 30일 내에 3회 이상 시청
#            final_matrix.iloc[i,j] = final_matrix.iloc[i,j] + 0.8
#        elif before_matrix.iloc[i,j] >= 10 : # 30일 전까지 10회 이상 시청
#            final_matrix.iloc[i,j] = final_matrix.iloc[i,j] + 0.7
#        elif once_matrix.iloc[i,j] <= 2 and once_matrix.iloc[i,j] > 0 : # 90일 전까지 0번 이상 2번 이하 시청하고 최근 3개월간 시청하지 않음
#            final_matrix.iloc[i,j] = 0.001
        
#
## 지금 여기 쓰레기야 #
#
#recent_group = recent_matrix.stack('상품명2')
#once_group = once_matrix.stack('상품명2')
#all_group = all_matrix.stack('상품명2')
#norm_group = norm_matrix.stack('상품명2')
#
#
#group = pd.concat([recent_group, once_group, all_group, norm_group], axis=1)
#group.columns = ['recent', 'once', 'all', 'norm']
#
#
#def infer_rating(count) :
#    if count[0] >= 3 : # 최근에 3번 이상 보면
#        x = 0.8 + count[3]*0.2
#    elif count[2] >= 10 : # 전체 기간에 10번 이상 보면
#        x = 0.7 + count[3]*0.2
#    elif 0 < count[1] <= 2 and (count[2] - count[1]) == 0 : # 예전에 2번 이하 보고 안봤으면
#        x = 0.01
#    else :
#        x = count[3]*0.2 #
#    return x
#
## test
#df = pd.DataFrame(data = {'recent' : [5, 0, 0, 5, 0, 0],
#                  'once' : [2, 2, 1, 10, 0, 0],
#                  'all' : [7, 2, 13, 25, 0, 11],
#                  'norm' : [0.35, 0.1, 0.65, 0.88, 0, 0.55]})
#
#import time    
#start_time = time.time() 
#
#df['score'] = df.apply(lambda x : 0 if x[2] == 0 else infer_rating(x), axis=1)
##df['score'] = df.apply(lambda x : infer_rating(x), axis=1)
#
#print("--- %s seconds ---" %(time.time() - start_time))
#
##







##시작부분 코드
#
#start_time = time.time() 
##------------------------
# 
# 
#group['score'] = group.apply(lambda x : 0 if x[2] == 0 else infer_rating(x), axis=1)
# 
##----------------------------
##종료부분 코드
#print("start_time", start_time) #출력해보면, 시간형식이 사람이 읽기 힘든 일련번호형식입니다.
#print("--- %s seconds ---" %(time.time() - start_time))
#
#




##########################










## matrix for how many times user sees item
#def create_matrix(data) : 
#    ## INPUT : data(DataFrame, col : 상품명2(item), 아이디+회원번호(user)) ##
#    ## OUTPUT : trsc_matrix(DataFrame, row : 상품명2(item), col: 아이디+회원번호(user)) ##
#
#    # 회원번호 당 상품명2
#    trsc = [data['상품명2'][data['아이디+회원번호'] == i].values.tolist() for i in users]
#    trsc_counter = [Counter(trsc[i]) for i in range(len(trsc))] # unique title + counts
#    trsc2 = [[list(i.keys()), list(i.values())] for i in trsc_counter]
#
#    # create matrix
#    trsc_matrix = pd.DataFrame(index = items, columns= member)
#    trsc_matrix = trsc_matrix.reset_index()
#    
#    # input value to matrix
#    for i in range(len(trsc2)) :
#        trsc_matrix.iloc[:,(i+1)] = trsc_matrix['index'].apply(lambda x : trsc2[i][1][trsc2[i][0].index(x)] if x in trsc2[i][0] else 0)
#
#    # index 정리
#    trsc_matrix.index = trsc_matrix['index']
#    del trsc_matrix['index']
#    
#    return trsc_matrix















