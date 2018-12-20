# -*- coding: utf-8 -*-
"""
Created on Tue Oct 16 01:24:44 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_light1016.txt',"rb") as fp :
        vod = pickle.load(fp)
        
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\norecos.txt',"rb") as fp :
        norecos = pickle.load(fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\recos.txt',"rb") as fp :
        recos = pickle.load(fp)

userlist = norecos.columns.tolist()

data = vod[vod['거래일시2']<=60] #11,12월
data = data[data['아이디+회원번호'].isin(userlist)]



def show_result(norecos) :
    users = []
    vods = []
    count = []

    for u in userlist :
        user_vod = data[['상품명2', '아이디+회원번호']][data['아이디+회원번호'] == u]
        user_vod = user_vod.drop_duplicates()
    
        count.append(len(user_vod))
    
        noreco = [norecos.loc[:,u][i][0] for i in range(len(norecos)) if norecos.loc[:,u][i] != 0]
        noreco_see = user_vod['상품명2'][user_vod['상품명2'].isin(noreco).tolist()]
    
        if len(noreco_see) != 0 :
            users.append(u)
            vods.append(noreco_see.tolist())
        
    return users, vods, count
    
users, vods, count = show_result(norecos)
max(count)
min(count)
