# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 23:49:37 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix.txt',"rb") as fp :
        cluster_matrix = pickle.load(fp)
        

# find k for k-means clustering
ks = range(2,20)
inertias = list()

for k in ks :
    print(k)
    cls = KMeans(n_clusters=k)
    cls.fit(cluster_matrix)   
    inertias.append(cls.inertia_)
        

plt.plot(ks, inertias, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()


# k-means clustering with k 8
k=4
cls = KMeans(n_clusters=k)
cls.fit(cluster_matrix)
labels = cls.labels_

items = cluster_matrix.iloc[:,8:]
items_list = items.columns.tolist()


sex_df = pd.DataFrame()
age_df = pd.DataFrame()
max_df = pd.DataFrame(index = items_list)
min_df = pd.DataFrame(index = items_list)
mean_df = pd.DataFrame(index = items_list)
count_df = pd.DataFrame(index = items_list) 

for i in range(k) :
    print(i)
    # 성별분포
    sex_df[i] = cluster_matrix[labels==i]['성별코드'].value_counts() / len(cluster_matrix[labels==i])
    # 나이 분포
    age_df[i] = np.sum(cluster_matrix[labels==i][[10, 20, 30, 40, 50, 60]], axis=0) / len(cluster_matrix[labels==i])
    # 최대 선호도
    max_df[i] = items[labels==i].max(0)
    # 최소 선호도
    min_df[i] = items[labels==i].min(0)
    # 시청한 사람들의 평균 선호도
    mean_df[i] = items[items>0][labels==i].mean(0)
    # 시청한 사람 수
    count_df[i] = np.count_nonzero(items[labels==i], axis=0)
    











