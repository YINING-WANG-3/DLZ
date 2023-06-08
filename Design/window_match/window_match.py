import warnings
warnings.simplefilter(action='ignore', category = FutureWarning)

import numpy as np
import pandas as pd
from statistics import multimode
import matplotlib.pyplot as plt
import random
from itertools import chain

pd.set_option('mode.chained_assignment', None)
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False

# Input data
ori_data = '凸窗_特殊.xlsx'

# Function to retrieve matchable standard components
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
def most_frequent(data, l):
    database = pd.read_excel(ori_data, sheet_name = 'Sheet2', index_col='构件')
    d_l = data['宽'].values.tolist()
    new_l = multimode(l) #Currently the default sort, should be optimized to be based on priority
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

# Function to match standard components
def mer_new(data, threshold_1, threshold_2):
    database = pd.read_excel(ori_data, sheet_name = 'Sheet2', index_col='构件')
    data['可匹配标准件'] = data.apply(lambda x: interval(x['宽'], x['高'], threshold_1, threshold_2), axis=1)
    res_data = data
    new_data = pd.DataFrame()
    fin_data = pd.DataFrame()
    while len(res_data) > 0:
        l = res_data['可匹配标准件'].values.tolist()
        l = list(chain.from_iterable(l))
        most = most_frequent(res_data, l)
        res_data['可匹配标准件'] = res_data['可匹配标准件'].apply(tuple)
        for i, row in res_data.iterrows(): 
            if most in row['可匹配标准件']:
                res_data.at[i,'标准件'] = most
                res_data.at[i,'标准件-宽'] = database.at[most, '宽']
                res_data.at[i,'标准件-高'] = database.at[most, '高']
                new_data = new_data.append(row)
                fin_data = fin_data.append(res_data.loc[i])
        i = new_data.index.tolist()
        new_data = pd.DataFrame()
        res_data = res_data.drop(index = i)
        res_data['可匹配标准件'] = res_data['可匹配标准件'].apply(list)
        fin_data = fin_data.sort_index()
    return fin_data
    
# Run functions
df = pd.read_excel(ori_data, sheet_name = 'Sheet1')
fin_data = mer_new(df, 300, 20)
fin_data.at[-1,'标准件'] = fin_data['标准件'].nunique()
with pd.ExcelWriter('凸窗测试_特殊.xlsx') as writer:
    fin_data.to_excel(writer, sheet_name = 'Sheet1', index = False)