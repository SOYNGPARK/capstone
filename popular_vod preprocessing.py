# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:48:32 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import re


# 
def get_original(new_title) : 
    return vod_new[vod_new['상품명2']==new_title]


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt',"rb") as fp :
        vod_new = pickle.load(fp) 

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new_unique.txt',"rb") as fp :
        vu = pickle.load(fp)
        

# 1. drop 할 것 -> drop_dic 에 상품명2를 채워넣을 것
# 제목 이상한 것, 성인물
drop_dic = ['',]

a = get_original('')

for i in vu['title'].values :
    if re.compile('^\d{1,3},$').match(i) : # ex) 1, 3,
        drop_dic.append(i)

for i in drop_dic :
    vod_new = vod_new.drop(vod_new[vod_new['상품명2'] == i].index)


# 2. 상품명 통일 할 것 -> 엑셀에 dictionary 만들기













