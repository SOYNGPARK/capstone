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


def predict_rating(u, i, k=5) :
    ## INPUT : u(user_id), i(item_id), k(# of neighbors of u) ##
    ## OUTPUT : r_ui(user u's rating for item i) ##
    
    # vs : neighbors of u  
    vs = [x for x in range(len(users))]
    vs.remove(u)
          
    r_vis = [ratings.iloc[i,v] for v in vs if ratings.iloc[i,v] != 0] # user v's rating for item i
    sim_uvs = [sim[u,v] for v in vs if ratings.iloc[i,v] != 0] # similarity between u and v
   
    neighbors = list()
    for x in range(len(r_vis)) :
        neighbors.append((sim_uvs[x], r_vis[x]))

    neighbors.sort(key=lambda x: x[0], reverse=True) # sort by similarity in descending order
    
    # predict rating
    divid = sum(sim_uv*r_vi for (sim_uv, r_vi) in neighbors[:k])
    divis = sum(sim_uv for (sim_uv, r_vi) in neighbors[:k])
    
    r_ui = divid/divis
    
    # similar neighbors
    similar_neighbors = [(sim_uv, r_vi) for (sim_uv, r_vi) in neighbors[:k]]
    
    return r_ui, similar_neighbors


def tell_me(user) :
    ## INPUT : user(user name)##
    ## OUTPUT : None ##
    
    uid = users.index(user)
    
    # 이미 시청한 아이템
    see = ratings[user][ratings[user]>0].index.tolist() # item 제목
    see_r = ratings[user][ratings[user]>0].tolist() # item 평점
    
    see_ratings = list()
    for i in range(len(see)) :
        see_ratings.append( (see[i], see_r[i]) ) # item 제목, item 평점
        
    see_ratings.sort(key=lambda x : x[1], reverse=True)
    
    # 실제로 좋아하는 아이템 top3
    like = [(t, r) for (t, r) in see_ratings if r > 0.6]
    
    if len(like) == 0 :
        print('* {} cold start *'.format(user))
    
    else :
        print('* {} 고객님이 실제로 좋아하시는 프로그램이에요! *'.format(user))
        for x in like :
            print('{}\t {}'.format(x[0], x[1]))

        # 아직 안 본 아이템
        nosee = ratings[user][ratings[user]==0].index.tolist() # item 제목
        nosee_id = [items.index(i) for i in nosee] # item id
    
        nosee_ratings = list()
        for i in range(len(nosee)) :
            nosee_ratings.append( (nosee[i], predict_rating(uid, nosee_id[i])[0]) ) # item 제목, item 평점
    
        nosee_ratings.sort(key=lambda x : x[1], reverse=True)
    
        # 추천 아이템 top3
        recommend = nosee_ratings[:3]
    
        print('* {} 고객님께 추천드려요! *'.format(user))
        for x in recommend :
            print('{}\t {}'.format(x[0], x[1]))
    
        # similar neighbors
        print('* {}\'s similar neighbors *'.format(user))
        for x in recommend :
            print(x[0])
            similar_neighbors = predict_rating(uid, items.index(x[0]))[1]
            for n in similar_neighbors :
                print(n)

    return None


tell_me('KTPGMTV001_526357')
tell_me(users[15])


for u in users:
    tell_me(u)
    print()




user = 'KTPGMTV001_526357'

u = users.index(user)
i = 0

r_ui, sne = predict_rating(u,i)

# 시청기록 횟수와 유사도에 따른 분류, 좋아하는 그리고 추천하는 프로그램 수 = max(0.7보다 큰 수, 3)







a = []

[i for i in a if i>2]

for aa in a :
    print(aa)

a[0]
