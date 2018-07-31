# -*- coding: utf-8 -*-
"""
Created on Tue Jul 31 17:32:37 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import re


# 상품명 1차 전처리 리스트
re_dic = ['\s?\([a-zA-Z\s\d!"#$%&\'*+,-./:;<=>?@\\^_`|~＆Ⅱ]+\)\s?',  # (한글빼고다) ex.(Bridget Jones`s Baby)
          '\s?\([a-zA-Z\s!"#$%&\'*+,-./:;<=>?@\\^_`|~＆]+\)\s?', # (숫자빼고다) ex.(극장판), 
          '\s?\[[가-힣a-zA-Z\s\d!"#$%&\'*+,-./:;<=>?@\\^_`|~]+\]\s?',  # [] ex. [HD], [우리말]
          '\s?\(\d{1,2}\.\d{1,2}\.\d{1,2}\)\s?', # (yy.mm.dd)
          '\s?\(\d{1,2}\/\d{1,2}\/\d{1,2}\)\s?', # (yy/mm/dd)
          '\s?\(\d{1,2}\/\d{1,2}\)\s?', # (mm/dd)
          '\s?\(\d{1,2}\/\d{1,2}방영\)\s?', # (mm/dd방영)
          '\s?\d{1,2}월\d{1,2}일\s?', # yy월mm일
          '\s?\d{1,2}월\d{1,2}일\([가-힣]\)\s?', # yy월mm일(요일)
          '\s?\-무삭제판\s?', '\s?\-무삭제\s?', '\s?무삭제\s?',
          '\s?감독판\s?', '\s?평생소장\s?', '\s?무삭특별판\s?', '\s?패키지\s?', 
          '\s?극장판\s?', '\s?소장용\s?'
          ] 

# 상품명 삭제 리스트
del_dic = ['.*월정액.*', '.*외\s\d+종.*'] 

# 상품명 2차 전처리 리스트
re_dic_after = ['\s?\(본편', '\s?\(제', '\s?\(.*\)\s?']

# 회차 리스트
num_dic = ['\s(\d{1,4}[회화])\(\d{1,4}[회화]\)$', '\s?\(?(\d{1,4}[회화])\)?\s?']

# load data
def load_data(url) :
    data = pd.read_csv(url, engine='python', encoding = 'utf-8')
    data = data.reset_index()
    data.columns = ['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드']
    return data

# preprocessing
def non_kt_preprocessing(month) : 
    
    print('##load data##')
    url = r'C:\Users\soug9\Desktop\Capstone Design 1\data\csv\결제내역 2017-{}.csv'.format(month) 
    data = load_data(url)
    print('#head#\n', data.head())


    print('##non-kt##')
    # non kt 데이터 남기기
    var = [i for i in range(len(data)) if 'KT' not in data['가맹점아이디'][i]]
    data = data.loc[var]
    print('#head#\n', data.head())


    print('##delete##')
    # 거래유형 PC아닌 것 삭제
    data = data.drop(data[data['거래유형'] != 'PC'].index)

    # 상품명 단편구매 인것 삭제
    data = data.drop(data[data['상품명'] == '단편구매'].index)

    # 상품명 시리즈구매 인것 삭제
    data = data.drop(data[data['상품명'] == '시리즈구매'].index)


    clean = data['상품명']

    print('##replace 1##')
    for i in (re_dic + del_dic) :
        clean = clean.apply(lambda x : re.sub(i,'',x))
    

    print('##split episode##')
    # 회차 칼럼 분리
    num = clean.apply(lambda x : '' if re.compile(num_dic[0]).search(x) == None and re.compile(num_dic[1]).search(x) == None else x)
    
    for i in num_dic :   
        p = re.compile(i)
        num = num.apply(lambda x : p.search(x).group(1) if p.search(x) != None else x)
        
    num = num.apply(lambda x : re.sub('^0{1,2}','',x)) # 001회 -> 1회

    # 상품명에서 회차 삭제
    for i in num_dic :
        clean = clean.apply(lambda x : re.sub(i,'',x))


    print('##replace 2##')
    for i in re_dic_after :
        print(i)
        clean = clean.apply(lambda x : re.sub(i,'',x))
    
    
    print('##final dataframe##')
    data2 = pd.concat([data, clean, num], axis=1)
    data2.columns= ['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드', '상품명2', '회차']

    data2 = data2.drop(data2[data2['상품명2']==''].index) # del_dic 에 있던 애들(빈칸) 삭제

    data2.index = range(len(data2)) # 인덱스 초기화
    
    print('#head#\n', data2.head())
    
    
    print('##save data##')
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_2017-{}.txt'.format(month),"wb") as fp :
        pickle.dump(data2,fp)
    
    with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_2017-{}.txt'.format(month),"rb") as fp :
        test = pickle.load(fp)
        
    print('#head#\n', test.head())

    return None



################# test ####################

non_kt_preprocessing('02')

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_2017-02.txt',"rb") as fp :
        test2 = pickle.load(fp)









