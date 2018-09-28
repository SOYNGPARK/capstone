# -*- coding: utf-8 -*-
"""
Created on Mon Sep 10 20:58:31 2018

@author: soug9
"""

import pickle
from sklearn.metrics.pairwise import pairwise_distances
import numpy as np
import pandas as pd

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\drama_matrix.txt',"rb") as fp :
        drama_matrix = pickle.load(fp)
        
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\user_labels.txt',"rb") as fp :
        user_labels = pickle.load(fp)

# user <- clustering 
ratings = drama_matrix.loc[user_labels[user_labels['labels']==2]['users'].tolist(),:]        
     
# item <- 5명 이상의 유저가 시청
ratings_t = ratings.T[np.count_nonzero(ratings, axis=0)>=5]
ratings = ratings_t.T
   
# similarity
sim = 1 - pairwise_distances(ratings, metric='cosine') # 1 - (1-cosine similarity) = cosine similarity

items= ratings.columns.tolist()
users = ratings.index.tolist()


def predict_rating(u, i, k=3) :
    ## INPUT : u(user_id), i(item_id), k(# of neighbors of u) ##
    ## OUTPUT : r_ui(user u's rating for item i) ##
    
    # vs : neighbors of u  
    vs = [x for x in range(len(users))]
    vs.remove(u)
          
    r_vis = [ratings.iloc[v,i] for v in vs if ratings.iloc[v,i] != 0] # user v's rating for item i
    sim_uvs = [sim[u,v] for v in vs if ratings.iloc[v,i] != 0] # similarity between u and v
   
    neighbors = list()
    for x in range(len(r_vis)) :
        if sim_uvs[x] > 0.5 :
            neighbors.append((sim_uvs[x], r_vis[x]))
            
    if len(neighbors) < k :
        return np.nan, np.nan
    
    neighbors.sort(key=lambda x: x[0], reverse=True) # sort by similarity in descending order
    
    # predict rating
    divid = sum(sim_uv*r_vi for (sim_uv, r_vi) in neighbors[:k])
    divis = sum(sim_uv for (sim_uv, r_vi) in neighbors[:k])
    
    r_ui = divid/divis
    
    similar_neighbors = [(sim_uv, r_vi) for (sim_uv, r_vi) in neighbors[:k]]
    
    return r_ui, similar_neighbors
    
#    try : 
#        r_ui = divid/divis
#    except ZeroDivisionError : # 이웃이 없으면
#        return np.nan, np.nan
#    else :
#        # similar neighbors
#        similar_neighbors = [(sim_uv, r_vi) for (sim_uv, r_vi) in neighbors[:k]]
#    
#        return r_ui, similar_neighbors


def tell_me(user) :
    ## INPUT : user(user name)##
    ## OUTPUT : None ##
    
    uid = users.index(user)
    
    # 이미 시청한 아이템
    see = ratings.loc[user,:][ratings.loc[user,:]>0].index.tolist() # item 제목
    see_r = ratings.loc[user,:][ratings.loc[user,:]>0].tolist() # item 평점
    
    see_ratings = list()
    for i in range(len(see)) :
        see_ratings.append( (see[i], see_r[i]) ) # item 제목, item 평점
        
    see_ratings.sort(key=lambda x : x[1], reverse=True)
    
    # 실제로 좋아하는 아이템 top3
    like = [(t, r) for (t, r) in see_ratings if r > 60]
    
    if len(like) == 0 :
        print('* {} cold start *'.format(user))
    
    else :
        print('* {} 고객님이 실제로 좋아하시는 프로그램이에요! *'.format(user))
        for x in like :
            print('{}\t {}'.format(x[0], x[1]))

        # 아직 안 본 아이템
        nosee = ratings.loc[user,:][ratings.loc[user,:]==0].index.tolist() # item 제목
        nosee_id = [items.index(i) for i in nosee] # item id
    
        nosee_ratings = list()
        for i in range(len(nosee)) :
            pr = predict_rating(uid, nosee_id[i])[0]
            if pr > 10 : # 10점 이상만 추천
                nosee_ratings.append( (nosee[i], pr) ) # item 제목, item 평점
    
        nosee_ratings.sort(key=lambda x : x[1], reverse=True)
    
        # 추천 아이템 top10
        recommend = nosee_ratings[:10]
    
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



best_users = ratings[ratings.sum(1) > 250].index.tolist()

for u in best_users[23:27] :
    tell_me(u)
    print()


tell_me(users[0])




