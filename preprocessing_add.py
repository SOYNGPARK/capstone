# -*- coding: utf-8 -*-
"""
Created on Thu Aug 23 15:09:48 2018

@author: soug9
"""

# '~~시즌' 전처리

import pandas as pd
import re
import pickle

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final.txt',"rb") as fp :
        vod_final = pickle.load(fp)  
        
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_unique.txt',"rb") as fp :
        vu = pickle.load(fp)  

titles = list()
for i in range(len(vu)) :
    if re.compile('.*하이큐.*').match(vu['title'][i]) : 
        print(vu['title'][i], vu['count'][i])
        titles.append(vu['title'][i])
   
titles.remove('하이큐: 세컨드 시즌')    

problems = pd.DataFrame(columns = vod_final.columns)    
for t in titles :
     v = vod_final[vod_final['상품명2'] == t]
     problems = pd.concat([problems ,v])
             
clean = problems['상품명']  

# 상품명2 전처리
clean = clean.apply(lambda x : re.sub('\s?\([A-Za-z0-9\s]*\)','',x))
clean = clean.apply(lambda x : re.sub('\s?\([\d]+회\)','',x))

# 회차 분리
p = re.compile('.*\s(\d{1,2}회)$')
num = clean.apply(lambda x : p.search(x).group(1) if p.search(x) != None else x)

# 회차 삭제
clean = clean.apply(lambda x : re.sub('\s\d{1,2}회$','',x))

# df에 넣기
problems['상품명2'] = clean
problems['회차'] = num

# 기존 데이터 삭제
vod_final1 = vod_final.drop(problems.index)
vod_final2 = pd.concat([vod_final1, problems])

# unique vod    
def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique 

# unique 상품명2 확인
vu2 = unique_vod(vod_final2)

for i in range(len(vu2)) :
    if re.compile('.*콜드 케이스.*').match(vu2['title'][i]) : 
        print(vu2['title'][i], vu2['count'][i])
        
vod_final2['상품명2'][vod_final2['상품명2']=='캐슬 시즌 7'] = '캐슬 시즌7'
vod_final2['상품명2'][vod_final2['상품명2']=='캐슬 시즌 8'] = '캐슬 시즌8'


#save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add.txt',"wb") as fp :
        pickle.dump(vod_final2,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add.txt',"rb") as fp :
        vod_final2_test = pickle.load(fp)  
        
        
#save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add_unique.txt',"wb") as fp :
        pickle.dump(vu2,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final_add_unique.txt',"rb") as fp :
        vu2_test = pickle.load(fp)  






