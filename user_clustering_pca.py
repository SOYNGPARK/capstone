# -*- coding: utf-8 -*-
"""
Created on Fri Sep 28 23:31:30 2018

@author: soug9
"""

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import pickle

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix.txt',"rb") as fp :
        X = pickle.load(fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\user_labels.txt',"rb") as fp :
        user_labels = pickle.load(fp)

# clustering 결과 확인
y = user_labels['labels']

pca=PCA(n_components=2)
pca.fit(X)

y_pca=pca.transform(X)

plt.scatter(y_pca[:,0],y_pca[:,1],c=y)
plt.scatter(X.iloc[:,15],X.iloc[:,16],c=y)
