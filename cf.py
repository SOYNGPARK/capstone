# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 20:58:31 2018

@author: soug9
"""

import pickle
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import pandas as pd

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\final_matrix.txt',"rb") as fp :
        ratings = pickle.load(fp)
        
sim = 1 - pairwise_distances(ratings.T, metric='cosine') # 1 - (1-cosine similarity) = cosine similarity

users = ratings.columns.tolist()
items = ratings.index.tolist()


a = [i for i in range(10)]  
a.remove(3)



def predict_rating(u, i, k=5) :
# u = user, i = item, v= a neighbor of u, r = rating, k = # of neighbors of u
    vs = [x for x in range(len(users))]
    vs.remove(u)
    
    r_vis = [ratings.iloc[i,v] for v in vs]
    sim_uvs = [sim[u,v] for v in vs]
    
    neighbors = list()
    for x in range(len(r_vis)) :
        neighbors.append((sim_uvs[x], r_vis[x]))

    neighbors.sort(key=lambda x: x[0], reverse=True) # 유사도가 높은 순서대로 정렬
    
    divid = sum(sim_uv*r_vi for (sim_uv, r_vi) in neighbors[:k])
    divis = sum(sim_uv for (sim_uv, r_vi) in neighbors[:k])
    
    r_ui = divid/divis
    
    return r_ui


ratings.iloc[0,167]
predict_rating(0, 167)

a = ratings['KTPGMTV001_5489962'][ratings['KTPGMTV001_5489962']==0].index.tolist()
print(a)




def tell_me(u) :
    uid = users.index(u)
    
    # 이미 시청한 아이템
    see = ratings[u][ratings[u]>0].index.tolist()
    see_r = ratings[u][ratings[u]>0].tolist()
    
    see_ratings = list()
    for i in range(len(see_r)) :
        see_ratings.append( (see[i], see_r[i]) )
        
    see_ratings.sort(key=lambda x : x[1], reverse=True)
    
    # 실제로 좋아할 거라고 예상되는 아이템
    like = see_ratings[:3]
    print('* {} 고객님이 실제로 좋아하시는 프로그램이에요! *'.format(u))
    for x in like :
        print('{}\t {}'.format(x[0], x[1]))
    
    # 아직 안 본 아이템
    nosee = ratings[u][ratings[u]==0].index.tolist()
    nosee_id = [items.index(i) for i in nosee]
    
    nosee_ratings = list()
    for i in nosee_id :
        nosee_ratings.append( (i, predict_rating(uid, i)) )
    
    nosee_ratings.sort(key=lambda x : x[1], reverse=True)
    
    # 추천 아이템
    recommend = nosee_ratings[:3]
    
    print('* {} 고객님께 추천드려요! *'.format(u))
    for x in recommend :
        print('{}\t {}'.format(items[x[0]], x[1]))
    
    return None


tell_me('KTPGMTV001_526357')
tell_me(users[17])


for u in users:
    tell_me(u)
    print()





# 시청기록 횟수와 유사도에 따른 분류, 좋아하는 그리고 추천하는 프로그램 수 = max(0.7보다 큰 수, 3)













