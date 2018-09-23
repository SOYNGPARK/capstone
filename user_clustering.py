# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:50:31 2018

@author: soug9
"""


# User clustering


import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"rb") as fp :
        drama_matrix = pickle.load(fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_series.txt',"rb") as fp :
        vod = pickle.load(fp)     

genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\genre.csv')
del genre['movieCd']


# merge data
merge = pd.merge(vod, genre, how='left', on='상품명2')

# only drama genre
drama = merge[merge['Genre'] == '드라마']



## user ##
users = drama[['아이디+회원번호', '생년', '성별코드']]
users = users.drop_duplicates()

# 변수 '생년' -> 생년 결측값 제거
users['생년'].value_counts().sort_index()
users = users.drop(users[users['생년'] <= 1900].index)

def to_age(year) :
    if year < 1947 :
        age = 60
    elif year < 1957 :
        age = 50
    elif year < 1967 :
        age = 40
    elif year < 1977 :
        age = 30
    elif year < 1987 :
        age = 20
    else :
        age = 10
    return age

# 파생 변수 '나이대' 생성
users['나이대'] = users['생년'].apply(lambda x : to_age(x))
    
# 변수 '나이대' -> 더미변수 생성    
age_dummy = pd.get_dummies(users['나이대'])
users = pd.concat([users, age_dummy], axis=1)
users = users.drop(['생년','나이대'], axis=1)



## popular item ##
items_count = drama['상품명2'].value_counts()
plt.hist(items_count[items_count>=10000], bins=50, alpha=0.5)

popular = items_count[items_count>=5000].index.tolist()

popular_matrix = drama_matrix[popular]

#data = drama[['아이디+회원번호', '상품명2', 'Genre']][drama['상품명2'].isin(popular)]


# clusterig을 위한 최종 데이터 생성
popular_matrix = popular_matrix.reset_index()
final_matrix = pd.merge(users, popular_matrix, how='left', on='아이디+회원번호')
final_matrix = final_matrix.set_index('아이디+회원번호')

final_matrix = final_matrix[np.sum(final_matrix.iloc[:,7:], axis=1) != 0]


## clustering ##
final_matrix.loc['KTPGMTV001_8136063',:][final_matrix.loc['KTPGMTV001_8136063',:] != 0]

from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN

cls_kmeans =KMeans(n_clusters=5, init='random')
cls_kmeans.fit(final_matrix)

label=cls_kmeans.labels_




cls0 = final_matrix.iloc[label==0,:]
# 성별
cls0['성별코드'].value_counts()
# 나이대
np.sum(cls0[[10, 20, 30, 40, 50, 60]], axis=0)
# 드라마 선호도 합
np.sum(cls0.iloc[:,7:], axis=0)
# 드라마 시청한 사람 수
for_count = cls0.iloc[:,7:]
for_count[for_count != 0] = 1
np.sum(for_count, axis=0)





















