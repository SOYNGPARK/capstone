# -*- coding: utf-8 -*-
"""
Created on Mon Sep  3 17:30:20 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_light1016.txt',"rb") as fp :
        vod = pickle.load(fp)     

genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\genre.csv')
del genre['movieCd']

# merge data
merge = pd.merge(vod, genre, how='left', on='상품명2')

# data
data = merge[merge['Genre'] == '드라마']
data = data[data['거래일시2']>60] # 10월까지

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
recent = data[data['거래일시2']<=90] # 최근 30일(10월)
once = data[data['거래일시2']>90] # 30일 이전

# 기간 matrix
recent_matrix = create_matrix(recent)
once_matrix = create_matrix(once)

all_matrix = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count().unstack('상품명2')
all_matrix = all_matrix.fillna(0)

norm_matrix = all_matrix.divide(all_matrix.max(0), axis=1)
norm_matrix = norm_matrix*100

# infer score for drama

# 1) 30일 전까지 1~2번 시청한게 전부인 item = 0.1
once_matrix[(once_matrix<=2) & (once_matrix>0) & ((all_matrix - once_matrix) == 0)] = 0.1
once_matrix[once_matrix>2] = 0

# 2) 최근 30일 내에 3번 이상 시청한 item = 80 
recent_matrix[recent_matrix<3] = 0
recent_matrix[recent_matrix>=3] = 80

# 3) 전체 기간 동안 5번 이상 시청한 item = 70
all_matrix[all_matrix<5] = 0
all_matrix[all_matrix>=5] = 70

# 2) + 3)
all_matrix[(recent_matrix -all_matrix) > 0] = recent_matrix

# 4) 특정 기간에 몇 회 이상 시청했는지 여부(1,2)에 따라 80% weight + 기간에 상관없이 시청횟수 정규화로 20% weight
final_matrix = norm_matrix * 0.2 + all_matrix 

# 1) + 4)
final_matrix[(once_matrix -all_matrix) == 0.1] = once_matrix


# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix10.txt',"wb") as fp :
        pickle.dump(final_matrix,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix10.txt',"rb") as fp :
        final_matrix_test = pickle.load(fp)



# test

all_matrix1 = data['상품명2'].groupby([data['아이디+회원번호'], data['상품명2']]).count().unstack('상품명2')
all_matrix1 = all_matrix1.fillna(0)

recent_matrix1 = create_matrix(recent)
once_matrix1 = create_matrix(once)


def user_rating(user) :
    am = all_matrix.T[user]
    om = once_matrix.T[user]

    am1 = all_matrix1.T[user]
    rm1 = recent_matrix1.T[user]
    om1 = once_matrix1.T[user]

    nm = norm_matrix.T[user]
    nm2 = nm*0.2

    fm = final_matrix.T[user]

    m = pd.concat([am1, rm1, om1, am, om, nm, nm2, fm], axis=1)
    m.columns = ['전체시청횟수', '최근시청횟수', '예전시청횟수', 
                 '기간가중치점수(80%)', '예전시청점수', '정규화', '정규화(20%)', '선호도']
    m = m.sort_values(['전체시청횟수'], ascending=[False])
    
    return m

user = user_rating('KTPGMTV001_8136063')
user = user_rating('CNMHAS002_9929214')


def drama_rating(drama) :
    am = all_matrix[drama]
    om = once_matrix[drama]

    am1 = all_matrix1[drama]
    rm1 = recent_matrix1[drama]
    om1 = once_matrix1[drama]

    nm = norm_matrix[drama]
    nm2 = nm*0.2

    fm = final_matrix[drama]
    
    m = pd.concat([am1, rm1, om1, am, om, nm, nm2, fm], axis=1)
    m.columns = ['전체시청횟수', '최근시청횟수', '예전시청횟수', 
                 '기간가중치점수(80%)', '예전시청점수', '정규화', '정규화(20%)', '선호도']
    m = m.sort_values(['전체시청횟수'], ascending=[False])
    
    return m

drama = drama_rating('워킹데드 시즌1')
drama2 = drama_rating('슬기로운 감빵생활')

a = drama2.sort_values(['선호도'], ascending=[False])['선호도'][drama2['선호도'] > 0]
b = a[a <= 20]
b.plot.line()



#### 전체 회차가 적은 아이템은 절대 선호도가 70점을 넘길수가 없어!!! ###
## drama matrix
#drama_stack = drama_matrix.stack()
#drama_stack = drama_stack[drama_stack > 0]
#drama_stack.describe()
#plt.hist(drama_stack[drama_stack > 10], bins=9)
#plt.hist(drama_stack[(drama_stack > 3) & (drama_stack<=20)], bins=17)
#
#a = drama_stack[(drama_stack >= 10) & (drama_stack<=20)] # 회차가 애초에 적은 애들이 이 사이에 들어가네..
#b = a.reset_index()['상품명2'].value_counts().index.tolist()

