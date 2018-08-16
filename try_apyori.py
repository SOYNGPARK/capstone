# -*- coding: utf-8 -*-
"""
Created on Thu Aug 16 17:50:14 2018

@author: soug9
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from apyori import apriori

# load data
with open(r'C:\Users\soug9\Desktop\Capstone\data\vod_data_1.txt',"rb") as fp :
    data = pickle.load(fp)
    
data['가맹점아이디'].value_counts()    

skb = data[(data['가맹점아이디'] =='KTPGMTV001') or (data['가맹점아이디'] == 'KTPGOTM001')]


# 5회 이상 구매 기록이 있는 고객데이터 추출
plt.hist(skb['회원번호'].value_counts())
skb['회원번호'].value_counts().describe()
vc = skb['회원번호'].value_counts()

plt.boxplot(vc)

nums =list(map(lambda x : x.index if 2<= x <= 4 else None , vc))
#nums = vc[vc>2].index.values.tolist()
skb['temp'] = list(map(lambda x : x if x in nums else 'X', skb['회원번호']))
skb1 = skb[skb['temp'] != 'X']
nums1 = np.unique(skb1['회원번호'].values).tolist()


# create transaction list
item_ex = skb1['상품명2'][skb1['회원번호'] == 1763].values.tolist()

trsc = [skb1['상품명2'][skb1['회원번호'] == i].values.tolist() for i in nums1]

trsc = [list(set(skb1['상품명2'][skb1['회원번호'] == i].values.tolist())) for i in nums1]

trsc3 = list(filter(lambda x : len(x) >= 12, trsc))

# 너무 적게 혹은 많이 구매되는 아이템 제거
items = list()
for t in trsc :
    items = items + t

items_arr = np.array(items)
items, count = np.unique(items_arr, return_counts=True)

items_df = pd.DataFrame([items, count]).T
items_df.columns = ['item', 'count']
items_df['count'] = items_df['count'].astype(int)
items_df1 = items_df[items_df['count']>100]
items_df1 = items_df1[items_df['count']<600]

skb1['temp'] = list(map(lambda x : x if x in items_df1['item'].values else 'X', skb1['상품명2']))
skb2 = skb1[skb1['temp'] != 'X']
nums2 = np.unique(skb2['회원번호'].values).tolist()

# create transaction list again
trsc1 = [skb2['상품명2'][skb2['회원번호'] == i].values.tolist() for i in nums2]

# (option이라고 생각) list내에 item 중복 제거
trsc1 = [list(set(skb2['상품명2'][skb2['회원번호'] == i].values.tolist())) for i in nums2]

#
trsc2 = list(filter(lambda x : len(x) >=4, trsc1))



# apply association rule
rules = list(apriori(trsc3))

support = list()
items = list()
condition = list()
result = list()
confidence = list()
lift = list()

for RelationRecord in rules:    
    print('RelationRecord')    
    for ordered_stat in RelationRecord.ordered_statistics:
        print('ordered_stat')
        print('support', RelationRecord.support)
        print('items', RelationRecord.items)
        print('items_base', ordered_stat.items_base)
        print('items_add', ordered_stat.items_add)
        print('confidence', ordered_stat.confidence)
        print('lift', ordered_stat.lift, end='\n\n')
    print(end='\n\n')
    
    for ordered_stat in RelationRecord.ordered_statistics:
        support.append(RelationRecord.support)
        items.append(RelationRecord.items)
        condition.append(ordered_stat.items_base)
        result.append(ordered_stat.items_add)
        confidence.append(ordered_stat.confidence)
        lift.append(ordered_stat.lift)


result = pd.DataFrame({'items' : items, 'support' : support, 'condition' : condition, 'result' : result, 'confidence' : confidence, 'lift' : lift})
result = result.drop([i for i in range(len(result)) if not len(result['items'][i]) > 1])                   
result = result.sort_values('lift',ascending=False)    
result.head(n=10)

# Draw plot for comparison
graph = result.head(n=10).plot(title = "RESULT", kind='bar', legend=True)       























