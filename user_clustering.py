# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:50:31 2018

@author: soug9
"""


import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix10.txt',"rb") as fp :
        drama_matrix = pickle.load(fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_light0925.txt',"rb") as fp :
        vod = pickle.load(fp)     

genre = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\genre.csv')
del genre['movieCd']

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\users0925.txt',"rb") as fp :
        users = pickle.load(fp) 


# merge data : vod + genre
merge = pd.merge(vod, genre, how='left', on='상품명2')

# only drama genre
drama = merge[merge['Genre'] == '드라마']
drama = drama[drama['거래일시2']>60] # 10월까지

## drama users ## 
users_list = drama['아이디+회원번호'].value_counts().index.tolist()
users = users[users['아이디+회원번호'].isin(users_list)]
age_dummy = pd.get_dummies(users['나이대'])
users = pd.concat([users, age_dummy], axis=1)
users = users.drop(['나이대'], axis=1)


## popular & mania item ##
items_count = pd.DataFrame(drama['상품명2'].value_counts().sort_index())
items_count.columns = ['구매횟수합']
items_count['사용자수'] = np.count_nonzero(drama_matrix, axis=0)
items_count['구매비율'] = items_count['구매횟수합']/items_count['사용자수']

#drama_matrix[drama_matrix<10] = 0
#items_count['선호도합'] = np.sum(drama_matrix, axis=0)
#items_count['선호사용자수'] = np.count_nonzero(drama_matrix, axis=0)
#items_count['선호비율'] = items_count['선호도합']/items_count['선호사용자수']

# popular : 구매횟수가 많은 item 상위 20개
popular = items_count.sort_values(['구매횟수합'], ascending=[False])[:20]
popular['구매횟수합'].plot.line()
popular_list = popular.index.tolist()

# mania : 사용자수가 너무 적지 않고 구매비율이 높은 item 상위 20개
mania = items_count[items_count['사용자수'] >= 100].sort_values(['구매비율'], ascending=[False])[:20]
mania['구매비율'].plot.line()
mania['구매횟수합'].plot.line()
mania_list = mania.index.tolist()

# create matrix
popnia_matrix = drama_matrix[popular_list+mania_list]
cluster_matrix = popnia_matrix[np.sum(popnia_matrix, axis=1)>=10] # 선호도 합이 10점이상 준 user만..

# merge data : cluster_matrix + users
cluster_matrix = cluster_matrix.reset_index()
cluster_matrix = pd.merge(users, cluster_matrix, how = 'right', on='아이디+회원번호')
cluster_matrix = cluster_matrix.set_index('아이디+회원번호')


# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix10.txt',"wb") as fp :
        pickle.dump(cluster_matrix,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix10.txt',"rb") as fp :
        cluster_matrix_test = pickle.load(fp)


