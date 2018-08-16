# -*- coding: utf-8 -*-
"""
Created on Fri Aug  3 10:48:32 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import re


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new.txt',"rb") as fp :
        vod_new = pickle.load(fp) 

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_new_unique.txt',"rb") as fp :
        vu = pickle.load(fp)
    

# unique vod    
def unique_vod(vod) :
    title, count = np.unique(vod['상품명2'], return_counts=True)    
    vod_unique = pd.DataFrame({'title' : title, 'count' : count})
    return vod_unique 


# check original dataframe from new title
def get_original(new_title) : 
    return vod_new[vod_new['상품명2']==new_title]

orig = get_original('보보경심 (하)')

for i in range(len(vu)) :
    if re.compile('.*어떤.*').match(vu['title'][i]) : 
        print(vu['title'][i], vu['count'][i])
    
        
## drop ##

# create drop list in ascending order
drop_dic = [' ',]

for i in vu['title'].values :
    if re.compile('^\d{1,3},$').match(i) : # ex) 1, 3,
        drop_dic.append(i)
    if re.compile('.*\s외$').match(i) : # 거대한 해초 숲 외
        drop_dic.append(i)
    if re.compile('.*\s\/\s.*').match(i) : # 도깨비랑 덩기덕 / 좁쌀 한 톨
        drop_dic.append(i)

delete_dic_sy = pd.read_excel(r'C:\Users\soug9\Desktop\Capstone Design 1\data\delete_dic.xlsx')
delete_dic_sj = pd.read_csv(r'C:\Users\soug9\Desktop\Capstone Design 1\data\delete_dic_sj.csv')
delete_dic = pd.concat([delete_dic_sy, delete_dic_sj])
delete_dic = delete_dic['delete'].tolist()

drop_dic = delete_dic + drop_dic
drop_dic = list(set(drop_dic))
drop_dic.sort()


# split drop list 
drop_idx = list(range(0,len(drop_dic), 200))
drops = list()
for i in range(len(drop_idx))  :
    try :
        drops.append(drop_dic[drop_idx[i]:drop_idx[(i+1)]])
    except IndexError :
        drops.append(drop_dic[drop_idx[i]:])
        

# sort vod_new
vod_new.sort_values('상품명2', inplace = True)
vod_new.index = range(len(vod_new))
vod_new.head()
vod_new.tail()


# split vod_new
split_idx = list()
for i in drops :
    split_idx.append(vod_new[vod_new['상품명2'] == i[0]].index[0])

vods = list()
for i in range(len(split_idx)) :
    try :
        vods.append(vod_new.iloc[split_idx[i]:split_idx[(i+1)]])
    except IndexError :
        vods.append(vod_new.iloc[split_idx[i]:])


# check split result   
for i in range(len(drops)) :    
    if drops[i][0] != vods[i]['상품명2'].iat[0] :
        print('error1')
        
for i in range(len(drops)-1) : 
    if vods[i]['상품명2'].iat[-1] == vods[i+1]['상품명2'].iat[0] :
        print(i, 'error2') 


# drop
for i in range(len(drops)) :
    print("**", i)
    for j in range(len(drops[i])) :
        print("*", j)
        vods[i] = vods[i].drop(vods[i][vods[i]['상품명2'] == drops[i][j]].index)

vod_after_drop = vods[0]
for i in vods[1:] :
    vod_after_drop = pd.concat([vod_after_drop, i])


len(vu) - len(unique_vod(vod_after_drop)) == len(drop_dic) # 확인

# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_drop.txt',"wb") as fp :
        pickle.dump(vod_after_drop,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_drop.txt',"rb") as fp :
        vod_after_drop = pickle.load(fp)    
    


## change ##

# create change list in ascending order
change_dic_sy = pd.read_excel(r'C:\Users\soug9\Desktop\Capstone Design 1\data\change_dic.xlsx')
change_dic_sj = pd.read_excel(r'C:\Users\soug9\Desktop\Capstone Design 1\data\change_dic_sj.xlsx')
change_dic = pd.concat([change_dic_sy, change_dic_sj])

change_dic=change_dic.applymap(str) # df type을 str으로 변경
type(change_dic['before'].iat[50])

change_dic.sort_values('before', inplace = True)
change_dic.index = range(len(change_dic))
change_dic.head()
change_dic.tail()

# split change list 
change_idx = list(range(0,len(change_dic), 200))
changes = list()
for i in range(len(change_idx))  :
    try :
        changes.append(change_dic.iloc[change_idx[i]:change_idx[(i+1)]])
    except IndexError :
        changes.append(change_dic.iloc[change_idx[i]:])
        
        
# sort vod_after_drop
vod_after_drop.sort_values('상품명2', inplace = True)
vod_after_drop.index = range(len(vod_after_drop))
vod_after_drop.head()
vod_after_drop.tail()
        
        
# split vod_after_drop
split_idx1 = list()
for i in changes :
    split_idx1.append(vod_after_drop[vod_after_drop['상품명2'] == i['before'].iat[0]].index[0])

vods2 = list()
for i in range(len(split_idx1)) :
    try :
        vods2.append(vod_after_drop.iloc[split_idx1[i]:split_idx1[(i+1)]])
    except IndexError :
        vods2.append(vod_after_drop.iloc[split_idx1[i]:])
        
 
# check split result   
for i in range(len(changes)) :    
    if changes[i]['before'].iat[0] != vods2[i]['상품명2'].iat[0] :
        print('error1')
        
for i in range(len(changes)-1) : 
    if vods2[i]['상품명2'].iat[-1] == vods2[i+1]['상품명2'].iat[0] :
        print(i, 'error2') 
        
     
# change
vods3 = vods2
for i in range(len(changes)) :
    print("**", i)
    for j in range(len(changes[i])) :
        print("*", i, '-', j)
        vods3[i]['상품명2'].loc[vods3[i]['상품명2'] == changes[i]['before'].iat[j]] = changes[i]['after'].iat[j]
  

vod_after_change = vods3[0]
for i in vods3[1:] :
    vod_after_change = pd.concat([vod_after_change, i])


# save
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_change.txt',"wb") as fp :
#        pickle.dump(vod_after_change,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_change.txt',"rb") as fp :
        vod_after_change = pickle.load(fp)   

# unique vod        
vu1 = unique_vod(vod_after_change)


##additional change & drop##

def drop_vod(vods, drop_dic) :
    # vods : DataFrame / vod 구매 목록 / '상품명2' 칼럼 포함
    # drop_dic : list / '상품명2' 칼럼 중 제거 목록 
    for i in range(len(drop_dic)) :
        print('*', i)
        print(len(vods[vods['상품명2'] == drop_dic[i]].index), '개를 삭제하자')
        vods = vods.drop(vods[vods['상품명2'] == drop_dic[i]].index)
        print(len(vods), '개가 남았다')
        
    return vods


def change_vod(vods, change_dic) :
    # vods : DataFrame / vod 구매 목록 / '상품명2' 칼럼 포함
    # drop_dic : DatFrame(N by 2) / '상품명2' 칼럼 중 변경 목록 / 'before', 'after' 칼럼 포함
    for j in range(len(change_dic)) :
        print(j)
        vods['상품명2'].loc[vods['상품명2'] == change_dic['before'].iat[j]] = change_dic['after'].iat[j]
    
    return vods


# drop
drop_dic2 = pd.read_excel(r'C:\Users\soug9\Desktop\Capstone Design 1\data\delete2_dic.xlsx')
drop_dic2 = drop_dic2['delete'].tolist()
drop_dic2.sort()

vod_after_drop2 = drop_vod(vod_after_change, drop_dic2)

len(vu1) - len(unique_vod(vod_after_drop2)) == len(drop_dic2) # 확인

# save
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_drop2.txt',"wb") as fp :
#        pickle.dump(vod_after_drop2,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_drop2.txt',"rb") as fp :
        vod_after_drop2 = pickle.load(fp)   


# change
change_dic2 = pd.read_excel(r'C:\Users\soug9\Desktop\Capstone Design 1\data\change2_dic.xlsx')
vod_after_change2 = change_vod(vod_after_drop2, change_dic2)

# save
#with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_change2.txt',"wb") as fp :
#        pickle.dump(vod_after_change2,fp)

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_after_change2.txt',"rb") as fp :
        vod_after_change2 = pickle.load(fp)   

# unique vod
vu2 = unique_vod(vod_after_change2)


#
vod_after_change2 = vod_after_change2.drop(vod_after_change2[vod_after_change2['가맹점아이디'] == '1%의 어떤 것'].index)
a = vod_new[vod_new['상품명2'] == '1%의 어떤 것(2016)']
a['상품명2'] = '1%의 어떤 것'
vod_after_change2 = pd.concat([vod_after_change2, a])



## n번이상 구매한 회원 추출 ##

vod_after_change2['아이디+회원번호'] = vod_after_change2[['가맹점아이디', 
                 '회원번호']].apply(lambda x : '{}_{}'.format(x.values[0], x.values[1]), axis=1)

vodBuyNumber = vod_after_change2[['아이디+회원번호', '상품명']].groupby('아이디+회원번호').count()
vodBuyNumber['상품명'].describe()
vodBuyNumber['상품명'].plot.hist(bins=50)
vodBuyNumber['상품명'].plot.box()

len(vodBuyNumber[vodBuyNumber['상품명'] > 7])

vod_final = vod_after_change2[vod_after_change2['아이디+회원번호'].isin(vodBuyNumber[vodBuyNumber['상품명'] > 7].index)]

with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final.txt',"wb") as fp :
        pickle.dump(vod_final,fp)
        
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\vod_final.txt',"rb") as fp :
        vod_final_test = pickle.load(fp)  







