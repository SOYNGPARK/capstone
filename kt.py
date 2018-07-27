# -*- coding: utf-8 -*-
"""
Created on Wed Jul 25 11:23:02 2018

@author: soug9
"""

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori

# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_201701.txt',"rb") as fp :
    data = pickle.load(fp)
  
# extract only kt data
data['가맹점아이디'].value_counts()    

idx = [i for i in range(len(data)) if data['가맹점아이디'][i] in ['KTPGMTV001', 'KTPGOTM001']]
kt = data.loc[idx]

# date
kt['거래일시'] = pd.to_datetime(kt['거래일시'])
sample_date = kt['거래일시'][888]
sample_date.month
sample_date.day
sample_date.hour
sample_date.weekday()

# EDA
kt.columns
kt.head(5)
kt['상품명2'].value_counts().head(50)


count = kt['상품명2'].value_counts()
count = pd.DataFrame(count)
count = count.reset_index()
count.columns = ['상품명2', 'count']

# 한 번 구매된 상품 제외
count1 = count['상품명2'][count['count'] == 1].tolist()

kt['상품명2'] = list(map(lambda x : x if x not in count1 else '', kt['상품명2']))
kt = kt.drop(kt[kt['상품명2'] == ''].index)

# 인기있는(=많이 구매된 vod)
count.head(30)
count.head(10).plot(kind='bar')

count.to_excel("C:\\Users\soug9\Desktop\Capstone Design 1\data\count_201701_kt.xlsx", sheet_name='sheet1', index=False)





















