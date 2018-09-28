# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 23:49:37 2018

@author: soug9
"""

import numpy as np
import pandas as pd
import pickle
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans

# 한글 폰트
import matplotlib.font_manager as fm

font_list = fm.findSystemFonts(fontpaths=None, fontext='ttf')
path = 'C:\\Windows\\Fonts\\Hancom Gothic Regular.ttf'
font_name = fm.FontProperties(fname=path, size=50).get_name()
print(font_name)
plt.rc('font', family=font_name)


# load data
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\cluster_matrix.txt',"rb") as fp :
        cluster_matrix = pickle.load(fp)


# find k for k-means clustering
ks = range(2,20)
inertias = list()

for k in ks :
    print(k)
    cls = KMeans(n_clusters=k, random_state=0)
    cls.fit(cluster_matrix)   
    inertias.append(cls.inertia_)
        

plt.plot(ks, inertias, '-o')
plt.xlabel('number of clusters, k')
plt.ylabel('inertia')
plt.xticks(ks)
plt.show()


# k-means clustering
k=15
cls = KMeans(n_clusters=k, random_state=0)
cls.fit(cluster_matrix)
labels = cls.labels_

user_labels = pd.DataFrame({'users' : cluster_matrix.index.tolist(), 'labels' : labels})

# save
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\user_labels.txt',"wb") as fp :
        pickle.dump(user_labels,fp)
    
with open(r'C:\Users\soug9\Desktop\Capstone Design 1\data\preprocessing\user_labels.txt',"rb") as fp :
        user_labels_test = pickle.load(fp)


items = cluster_matrix.iloc[:,8:]
items_list = items.columns.tolist()


sex_df = pd.DataFrame()
age_df = pd.DataFrame()
max_df = pd.DataFrame(index = items_list)
min_df = pd.DataFrame(index = items_list)
mean_df = pd.DataFrame(index = items_list)
count_df = pd.DataFrame(index = items_list) 
std_df = pd.DataFrame(index = items_list) 

for i in range(k) :
    print(i)
    # 성별분포
#    sex_df[i] = cluster_matrix[labels==i]['성별코드'].value_counts() / len(cluster_matrix[labels==i])
#    # 나이 분포
#    age_df[i] = np.sum(cluster_matrix[labels==i][[10, 20, 30, 40, 50, 60, 70]], axis=0) / len(cluster_matrix[labels==i])
#    # 최대 선호도
#    max_df[i] = items[labels==i].max(0)
#    # 최소 선호도
#    min_df[i] = items[labels==i].min(0)
#    # 시청한 사람들의 평균 선호도
#    mean_df[i] = items[items>0][labels==i].mean(0)
#    # 시청한 사람 비율
#    count_df[i] = np.count_nonzero(items[labels==i], axis=0) / len(items[labels==i])
    # 분산
    std_df[i] = items[items>0][labels==i].std(0)

#전체
# 성별분포
sex_df['전체'] = cluster_matrix['성별코드'].value_counts() / len(cluster_matrix)
# 나이 분포
age_df['전체'] = np.sum(cluster_matrix[[10, 20, 30, 40, 50, 60, 70]], axis=0) / len(cluster_matrix)
# 최대 선호도
max_df['전체'] = items.max(0)
# 최소 선호도
min_df['전체'] = items.min(0)
# 시청한 사람들의 평균 선호도
mean_df['전체'] = items[items>0].mean(0)
# 분산
std_df['전체'] = items[items>0].std(0)

std_df_t = std_df.T
# 드라마 당 시청자 선호도 평균
mean_df_t = mean_df.T


#
def to_arr(label, kw):
    df= pd.DataFrame()
    
    if kw == 'mean' :
        df[kw] = items[items>0][labels==label].mean(0)
    elif kw == 'max' :
        df[kw] = items[labels==label].max(0)
    elif kw == 'min' :
        df[kw] = items[labels==label].min(0)
    else : # watch
        df[kw] = np.count_nonzero(items[labels==label], axis=0) / len(items[labels==label])
        df.index = items.columns.tolist()

    df = df.reset_index()
    df.sort_values(by=kw, inplace=True, ascending=False)
    if kw == 'max' :
        df.sort_values(by=kw, inplace=True, ascending=True)
    arr = np.array(df)
    return arr

def to_total_df(kw) :
    total = to_arr(0, kw)
    for i in range(1, k):
        print(i)
        total = np.concatenate((total, to_arr(i, kw)), axis=1)
        total_df = pd.DataFrame(total)
    return total_df

means = to_total_df('mean')
maxs = to_total_df('max')
mins = to_total_df('min')
watchs = to_total_df('watch')

# save
#writer = pd.ExcelWriter(r'C:\Users\soug9\Desktop\Capstone Design 1\data\cls15_result.xlsx', engine = 'xlsxwriter') 
#
#sex_df.to_excel(writer, sheet_name='sex_df')
#age_df.to_excel(writer,sheet_name='age_df')
#maxs.to_excel(writer,sheet_name='maxs')
#mins.to_excel(writer,sheet_name='mins')
#means.to_excel(writer,sheet_name='means')
#mean_df_t.to_excel(writer, sheet_name='mean_df_t')
#watchs.to_excel(writer, sheet_name='watchs')
#
#writer.save() 
#writer.close()

fig = plt.figure(figsize=(25, 10))
mean_df[0].sort_values(0, ascending=[False]).plot.bar()


fig = plt.figure(figsize=(25, 10))
#mean_df.sort_values(0, ascending=[False])[0].plot.line(legend=True)
#mean_df.sort_values(1, ascending=[False])[1].plot.line(legend=True)
#mean_df.sort_values(2, ascending=[False])[2].plot.line(legend=True)
#mean_df.sort_values(3, ascending=[False])[3].plot.line(legend=True)
#mean_df.sort_values(4, ascending=[False])[4].plot.line(legend=True)
mean_df.sort_values(5, ascending=[False])[5].plot.line(legend=True)
#mean_df.sort_values(6, ascending=[False])[6].plot.line(legend=True)
#mean_df.sort_values(7, ascending=[False])[7].plot.line(legend=True)
mean_df.sort_values(8, ascending=[False])[8].plot.line(legend=True)
#mean_df.sort_values(9, ascending=[False])[9].plot.line(legend=True)
#mean_df.sort_values(10, ascending=[False])[10].plot.line(legend=True)
#mean_df.sort_values(11, ascending=[False])[11].plot.line(legend=True)
#mean_df.sort_values(12, ascending=[False])[12].plot.line(legend=True)
#mean_df.sort_values(13, ascending=[False])[13].plot.line(legend=True)
mean_df.sort_values(14, ascending=[False])[14].plot.line(legend=True)
plt.xlabel('선호도를 기준으로 내림차순으로 정렬한 드라마')
plt.ylabel('선호도')




