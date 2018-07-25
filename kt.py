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
with open(r'C:\Users\soug9\Desktop\Capstone\data\vod_data_1.txt',"rb") as fp :
    data = pickle.load(fp)
  
# extract only kt data
data['가맹점아이디'].value_counts()    

idx = [i for i in range(len(data)) if data['가맹점아이디'][i] in ['KTPGMTV001', 'KTPGOTM001']]
kt = data.loc[idx]

# EDA
kt.columns
kt.head(5)
kt['상품명2'].value_counts().head(50)
count = kt['상품명2'].value_counts()
count = pd.DataFrame(count)

