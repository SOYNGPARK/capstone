# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 18:14:19 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import re


re_dic = ["\[.*\] *", "\(.*판매종료\) *", "\(소장용\) ", "\d{4}-\d{2}\-\d{2} ",
          " *\(배리어프리\) *", " *\(.*중지.*\) *", " *\(.*종료.*\) *", " *\(.*무삭제.*\) *", " *\(.*더빙.*\) *", 
          " *\(.*자막.*\) *", " *\(.*OpenVOD.*\) *", "\d{2}\/\d{2} ", " *\(.*확장판.*\) *", " *\(.*2D.*\) *", 
          " *\(.*3D.*\) *", " *\(.*감독판.*\) *", ' *3D *']

mod_dic = [".*1.*박.*2.*일.*", ".*무.*한.*도.*전.*"]

del_dic = ["\A\d{1,3}위\.","\A\d{1,3}회 *", "\A\d{1,3}화 *", "\A\d{1,3}강 *", "\A\d{1,2}.*\d{1,2}화 *", "\A싹쩨.*"]


# load data
def load_data(url) :
    data = pd.read_csv(url, engine='python', encoding = 'utf-8')
    data = data.reset_index()
    data.columns = ['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드']
    return data


# preprocessing
def kt_preprocessing(month):
    
    print('##load data##')
    url = r'C:\Users\soug9\Desktop\Capstone Design 1\data\csv\결제내역 2017-{}.csv'.format(month)
    data = load_data(url)
    print('#head#\n', data.head())
    
          
    print('##kt##')
    kt = pd.merge(data[data['가맹점아이디']=='KTPGOTM001'], data[data['가맹점아이디']=='KTPGMTV001'], how = 'outer')


    clean = kt['상품명']
    
    print('##replace1##')
    for i in re_dic:
       clean = clean.apply(lambda x: re.sub(i,"", x))


    print('##delete##')
    for i in del_dic:
        clean = clean.apply(lambda x: re.sub(i, "싹쩨", x))  


    print('##split episode##' )
    kt['상품명2'] = clean.apply(lambda x: re.sub(" *\d{1,4}[회화] *","", x))
    kt['회차'] = clean.apply(lambda x: str(re.search('\d{1,4}[화회] *', x).group()) if re.search(' *\d{1,4}[화회] *',x) != None else "")

    print('##replace2##')
    kt['상품명2'] = kt['상품명2'].apply(lambda x: re.sub(".*1.*박.*2.*일.*","1박 2일", x))
    kt['상품명2'] = kt['상품명2'].apply(lambda x: re.sub(".*무.*한.*도.*전.*","무한도전", x))
    
    
    kt = kt[kt["상품명2"]!="싹쩨"]
    print('##final dataframe##')
    print('#head#\n', kt.head())
    
    
    print('##save data##')
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\kt_2017-{}.txt'.format(month),"wb") as fp :
        pickle.dump(kt,fp)
    
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\kt_2017-{}.txt'.format(month),"rb") as fp :
        test = pickle.load(fp)
        
    print('#head#\n', test.head())

    return None


################# test ####################

month = ['0'+str(i) for i in range(1,10)] + ['10', '11', '12(1)', '12(2)']

for i in month :
    print(i)
    kt_preprocessing(i)
    












