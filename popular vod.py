# -*- coding: utf-8 -*-
"""
Created on Thu Aug  2 15:04:08 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt


def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique





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


vod_unique = unique_vod(vod)
vod_unique['count'][vod_unique['count']<=50].value_counts().sort_index()

vod_unique['title'][vod_unique['count']==30]

vod_poplr = vod_unique[vod_unique['count']>=30]

vod['삭제여부'] = vod['상품명2'].apply(lambda x : '' if x in vod_poplr['title'].values else '싹쩨')
vod_new = vod[vod['삭제여부'] != '싹쩨']
vod_new = vod_new.drop(['삭제여부'], axis=1)


with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt'.format(month),"wb") as fp :
        pickle.dump(vod_new,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt'.format(i),"rb") as fp :
        vod_new = pickle.load(fp)    

##### 이제 전처리 다시 해야함 ######
vu = unique_vod(vod_new)


vod_new = vod_new.drop(vod_new[vod_new['상품명2'] == ''].index)



vu = vu.sort_values(['count', 'title'], ascending=False)



a = vod[vod['상품명2'] == '3,']
