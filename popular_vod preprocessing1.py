# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:04:08 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle


# vod의 unique title과 count 반환하는 함수
def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique


# load data
month = ['0'+str(i) for i in range(1,10)] + ['10', '11', '12(1)', '12(2)']

vod = pd.DataFrame(columns = ['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드', '상품명2', '회차'])

for i in month :
    print(i)
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_2017-{}.txt'.format(i),"rb") as fp :
        nonkt = pickle.load(fp)
        print(len(nonkt))
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\kt_2017-{}.txt'.format(i),"rb") as fp :
        kt = pickle.load(fp)
        print(len(kt))
    vod = pd.concat([vod, nonkt, kt])


# 12개월 동안 30번 이상 구매된 vod만 남기기
vod_unique = unique_vod(vod)

vod_unique['count'][vod_unique['count']<=50].value_counts().sort_index()
vod_unique['title'][vod_unique['count']==30]

vod_poplr = vod_unique[vod_unique['count']>=30]

vod['삭제여부'] = vod['상품명2'].apply(lambda x : '' if x in vod_poplr['title'].values else '싹쩨')
vod_new = vod[vod['삭제여부'] != '싹쩨']
vod_new = vod_new.drop(['삭제여부'], axis=1)

vod_new.head()

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt',"wb") as fp :
        pickle.dump(vod_new,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt',"rb") as fp :
        vod_new1 = pickle.load(fp)    


# 
vu = unique_vod(vod_new)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new_unique.txt',"wb") as fp :
        pickle.dump(vu,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new_unique.txt',"rb") as fp :
        vu1 = pickle.load(fp)

