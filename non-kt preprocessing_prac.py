# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 17:41:26 2018

@author: Soyoung
"""

import numpy as np
import pandas as pd
import pickle
import re

with open(r'C:\Users\Soyoung\Desktop\data\temp.txt',"rb") as fp : #685125
    data = pickle.load(fp)


### drop some rows ###

# 가맹점 아이디 KT 제외
#data = data.drop(data[data['가맹점아이디'] == 'KTPGMTV001'].index)
#data = data.drop(data[data['가맹점아이디'] == 'KTPGOTM001'].index)    

var = [i for i in range(len(data)) if 'KT' not in data['가맹점아이디'][i]]
data = data.loc[var]

# 거래유형 PC아닌 것 삭제
data = data.drop(data[data['거래유형'] != 'PC'].index)

# 상품명 단편구매 인것 삭제
data = data.drop(data[data['상품명'] == '단편구매'].index)

# 상품명 시리즈구매 인것 삭제
data = data.drop(data[data['상품명'] == '시리즈구매'].index)

with open(r'C:\Users\Soyoung\Desktop\data\temp1.txt',"wb") as fp :
    pickle.dump(data,fp)
    
with open(r'C:\Users\Soyoung\Desktop\data\temp1.txt',"rb") as fp : #187580
    test = pickle.load(fp)


### 상품명 전처리 ###

# 상품명 대체 정규식 list
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

del_dic = ['.*월정액.*', '.*외\s\d+종.*']

    
# 상품명 대체 정규식 적용
clean = test['상품명']

for i in (re_dic + del_dic) :
    print(i)
    clean = clean.apply(lambda x : re.sub(i,'',x))



### 회차 전처리 ###

# 정규식
num_dic = ['\s(\d{1,4}[회화])\(\d{1,4}[회화]\)$', '\s?\(?(\d{1,4}[회화])\)?\s?']

# 회차 칼럼 분리
clean3 = clean
clean3 = clean3.apply(lambda x : '' if re.compile(num_dic[0]).search(x) == None and re.compile(num_dic[1]).search(x) == None else x)
for i in num_dic :   
    p = re.compile(i)
    clean3 = clean3.apply(lambda x : p.search(x).group(1) if p.search(x) != None else x)
clean3 = clean3.apply(lambda x : re.sub('^0{1,2}','',x)) # 001회 -> 1회

# 회차 unique
clean3_uq = pd.DataFrame(pd.unique(clean3))

# 제목에서 회차 삭제 하기
clean4 = clean
for i in num_dic :
    clean4 = clean4.apply(lambda x : re.sub(i,'',x))

# 제목에서 회차 잘 지웠는지 확인
for i in clean4 :
    if re.compile('.*\d{1,4}[회화].*').match(i) :
        print(i)

# 회차 칼럼 잘 분리 했는 지 확인
total = pd.concat([clean, clean4, clean3], axis=1)
total.columns = ['clean', 'title' , 'num']

for i in total[total['num']=='']['clean'] :
    if re.compile('.*\d{1,4}[회화].*').match(i) :
        print(i)


### 상품명 전처리 2 ###
re_dic_after = ['\s?\(본편', '\s?\(제', '\s?\(.*\)\s?']

clean5 = clean4
for i in re_dic_after :
    print(i)
    clean5 = clean5.apply(lambda x : re.sub(i,'',x))


# 제목 unique
a, counts = np.unique(clean5, return_counts = True)
a_df = pd.DataFrame(a)
counts_df = pd.DataFrame(counts)
aa = pd.concat([a_df, counts_df], axis=1)


### 합치기 ###
data2 = pd.concat([test, clean5, clean3], axis=1)
data2.columns= ['회원번호', '거래일시', '가맹점아이디', '거래유형', '상품명', '생년', '성별코드', '상품명2', '회차']

data2 = data2.drop(data2[data2['상품명2']==''].index) # del_dic 에 있던 애들 삭제

with open(r'C:\Users\Soyoung\Desktop\data\temp2.txt',"wb") as fp :
    pickle.dump(data2,fp)
    
with open(r'C:\Users\Soyoung\Desktop\data\temp2.txt',"rb") as fp :
    test2 = pickle.load(fp)



















