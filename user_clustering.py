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
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"rb") as fp :
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

#drama_matrix[drama_matrix<70] = 0
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
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix.txt',"wb") as fp :
        pickle.dump(cluster_matrix,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"rb") as fp :
        cluster_matrix_test = pickle.load(fp)





#
### clustering ##
#final_matrix1.loc['KTPGMTV001_8136063',:][final_matrix1.loc['KTPGMTV001_8136063',:] != 0]
#
#from sklearn.cluster import AgglomerativeClustering
#from scipy.cluster.hierarchy import dendrogram, linkage
#
## dendrogram
#Z = linkage(final_matrix1[:100], 'average')
#fig = plt.figure(figsize=(25, 10))
#dn = dendrogram(Z)
#
#
#
#
## build model
#cls1=AgglomerativeClustering(n_clusters=5, linkage='average')
#cls1.fit(final_matrix1[:1000])
#label=cls1.labels_
#children = cls1.children_
#
#plt.scatter(x1[:,0],x1[:,1],c=label2)
#
#
#






#
## clusterig을 위한 최종 데이터 생성
#popular_matrix = popular_matrix.reset_index()
#final_matrix = pd.merge(users, popular_matrix, how='left', on='아이디+회원번호')
#final_matrix = final_matrix.set_index('아이디+회원번호')
#
#
### eda ##
#
## sum
#rating_sum = np.sum(final_matrix.iloc[:,7:], axis=1)
#rating_sum.describe()
#plt.hist(rating_sum, bins=100)
#
## count
#users_list = rating_sum.index.tolist()
#rating_count = pd.Series(np.count_nonzero(final_matrix.iloc[:,7:], axis=1))
#rating_count.index = users_list
#rating_count.describe()
#plt.hist(rating_count, bins=22)
#
#
#rating_log = pd.concat([rating_sum, rating_count], axis=1)
#rating_log.columns = ['sum', 'count']
#rating_log=rating_log.sort_values(['sum'], ascending=[False])
#rating_log['sum'].plot.line()
#rating_log['sum'][rating_log['sum']<=200].plot.line()
#rating_log['count'].plot.line()
#
#
#
## cold start 제외
#drama_matrix = drama_matrix.reset_index()
#final_matrix1 = pd.merge(users, drama_matrix, how='left', on='아이디+회원번호')
#final_matrix1 = final_matrix1.set_index('아이디+회원번호')
#final_matrix1 = final_matrix1[rating_log['sum'] > 70]
#
#
#final_matrix = final_matrix[rating_log['sum'] > 70]
#
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\clustering_matrix.txt',"wb") as fp :
#        pickle.dump(final_matrix1,fp)
#    
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\clustering_matrix.txt',"rb") as fp :
#        final_matrix2 = pickle.load(fp)





#cls_kmeans =KMeans(n_clusters=5, init='random')
#cls_kmeans.fit(final_matrix)
#
#label=cls_kmeans.labels_
#
#
#
#
#cls0 = final_matrix.iloc[label==0,:]
## 성별
#cls0['성별코드'].value_counts()
## 나이대
#np.sum(cls0[[10, 20, 30, 40, 50, 60]], axis=0)
## 드라마 선호도 합
#np.sum(cls0.iloc[:,7:], axis=0)
## 드라마 시청한 사람 수
#for_count = cls0.iloc[:,7:]
#for_count[for_count != 0] = 1
#np.sum(for_count, axis=0)





















