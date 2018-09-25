# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 21:10:30 2018

@author: soug9
"""


import numpy as np
import pandas as pd
import pickle
import datetime


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod0924.txt',"rb") as fp :
        vod = pickle.load(fp)    

# vod 파생변수 거래일시2 : 2018년 1월 1일 기준으로 얼마나 전인지
vod['거래일시'] = pd.to_datetime(vod['거래일시'])
day = datetime.datetime(2018,1,1)

vod['거래일시2'] = vod['거래일시'].apply(lambda x : (day-x).days)

## save
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod0925.txt',"wb") as fp :
#        pickle.dump(vod,fp)
#    
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod0925.txt',"rb") as fp :
#        vod_test = pickle.load(fp)


## user ##

# 변수 '생년' -> 생년 결측값 제거
vod['생년'].value_counts().sort_index()
vod = vod.drop(vod[vod['생년'] <= 1900].index)

users = vod[['아이디+회원번호', '생년', '성별코드']]
users = users.drop_duplicates()

# 파생 변수 '나이대' 생성
def to_age(year) :
    if year <= 1947 :
        age = 70
    elif year <= 1957 :
        age = 60
    elif year <= 1967 :
        age = 50
    elif year <= 1977 :
        age = 40
    elif year <= 1987 :
        age = 30
    elif year <= 1997 :
        age = 20
    else :
        age = 10
    return age

users['나이대'] = users['생년'].apply(lambda x : to_age(x))
    
users = users.drop(['생년'], axis=1)

# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\users0925.txt',"wb") as fp :
        pickle.dump(users,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\users0925.txt',"rb") as fp :
        users_test = pickle.load(fp)


## vod light##
vod_light = vod.drop(['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드',
                        '회차','시리즈'], axis=1)

# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_light0925.txt',"wb") as fp :
        pickle.dump(vod_light,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_light0925.txt',"rb") as fp :
        vod_light_test = pickle.load(fp)









