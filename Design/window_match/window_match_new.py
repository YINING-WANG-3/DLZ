import warnings
warnings.simplefilter(action='ignore', category = FutureWarning)

import numpy as np
import pandas as pd
from statistics import multimode
import matplotlib.pyplot as plt
import random
from itertools import chain
from collections import Counter

pd.set_option('mode.chained_assignment', None)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# Input data
ori_data = '凸窗_全局.xlsx'

# Import data
data = pd.read_excel('凸窗测试_全局.xlsx', sheet_name = 'Sheet1')
colors = []

# Color data
data['颜色编号'] = data['标准件'].apply(lambda x: int(x.partition('件')[2]))

# Function to check if two lists are intersecting
def common(a, b):
    a_set = set(a)
    b_set = set(b)
    if len(a_set.intersection(b_set)) > 0:
        return True
    return False
    
# Function to retrieve matchable lists
def interval(x, y, threshold_1, threshold_2):
    database = pd.read_excel(ori_data, sheet_name = 'Sheet2', index_col='构件')
    '''x = round(x, -2)'''
    s = x - threshold_1
    e = x + threshold_1
    s2 = y - threshold_2
    e2 = y + threshold_2
    database = database[(database['宽'] >= s) & (database['宽'] <= e) & (database['高'] >= s2) & (database['高'] <= e2)]
    l = database.index.tolist()
    return l

# Function to determine the standard component
def cho_comp(data, tem_data):
    database = pd.read_excel(ori_data, sheet_name = 'Sheet2', index_col='构件')
    tem_data['可匹配标准件'] = tem_data['可匹配标准件'].apply(list)
    l = tem_data['可匹配标准件'].values.tolist()
    if isinstance(l[0], list):
        new_l = list(set.intersection(*map(set,l)))
    else:
        new_l = l
    d_l = data['宽'].values.tolist()
    if len(new_l) <= 1:
        return new_l[0]
    else:
        m = 0
        fin_l = new_l[0]
        for i in new_l:
            n = d_l.count(database.at[i, '宽'])
            if n > m:
                m = n
                fin_l = i
        return fin_l

# Function to find the least frequent list
'''def lea_freq(data, l):
    d_l = data['可匹配标准件'].values.tolist()
    l = sorted(l, reverse = True)
    l = Counter(l)
    lea = l.most_common()[-1][0]
    for i in d_l:
        if lea in i:
            print(i)
            return i
            break '''
            
# Function to find the largest and shortest list
def larg(data, l):
    d_l = data['可匹配标准件'].values.tolist()
    l = sorted(l, key=lambda x: int(x.partition('件')[2]))
    lea = l[-1]
    n = 10
    fin_l = []
    for i in d_l:
        if lea in i:
            if len(i) < n:
                n = len(i)
                fin_l = i
    print(fin_l)
    return fin_l

# Main function
def mer_new(data, threshold_1, threshold_2):
    database = pd.read_excel(ori_data, sheet_name = 'Sheet2', index_col='构件')
    data['可匹配标准件'] = data.apply(lambda x: interval(x['宽'], x['高'], threshold_1, threshold_2), axis=1)
    res_data = data
    new_data = pd.DataFrame()
    fin_data = pd.DataFrame()
    while len(res_data) > 0:
        l = res_data['可匹配标准件'].values.tolist()
        l = list(chain.from_iterable(l))
        lea = larg(res_data, l)
        res_data['可匹配标准件'] = res_data['可匹配标准件'].apply(tuple)
        for i, row in res_data.iterrows(): 
            if common(lea, row['可匹配标准件']):
                new_data = new_data.append(row)
        fin_comp = cho_comp(res_data, new_data)
        for i, row in res_data.iterrows(): 
            if fin_comp in row['可匹配标准件']:
                # print(new_data)
                # print(fin_comp)
                # print('-------------------')
                res_data.at[i,'标准件'] = fin_comp
                res_data.at[i,'标准件-宽'] = database.at[fin_comp, '宽']
                res_data.at[i,'标准件-高'] = database.at[fin_comp, '高']
                fin_data = fin_data.append(res_data.loc[i])
        i = new_data.index.tolist()
        new_data = pd.DataFrame()
        res_data = res_data.drop(index = i)
        res_data['可匹配标准件'] = res_data['可匹配标准件'].apply(list)
        fin_data = fin_data.sort_index()
    return fin_data
    
# Run functions
df = pd.read_excel(ori_data, sheet_name = 'Sheet1')
fin_data = mer_new(df, 200, 20)
fin_data.at[-1,'标准件'] = fin_data['标准件'].nunique()
with pd.ExcelWriter('凸窗测试_全局.xlsx') as writer:
    fin_data.to_excel(writer, sheet_name = 'Sheet1', index = False)
