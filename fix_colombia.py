# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:48:56 2020

@author: USUARIO
"""

#%%
import pandas as pd
df_colombia = pd.read_excel("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\inputs\\colombia.xlsx", sheet_name = "colombia")
print(df_colombia.columns)

#%%
#create missing columns and order
columns_missing = [pd.datetime(2020, 3, 7), pd.datetime(2020, 3, 8), pd.datetime(2020, 3, 10)]
for col in columns_missing:
    df_colombia[col] = 0
columns_ordered = df_colombia.columns[df_colombia.columns != 'Etiquetas de fila'].sort_values().to_list()
df_colombia = df_colombia[["Etiquetas de fila"] + columns_ordered]
print(df_colombia.head(), df_colombia.columns, df_colombia.shape)

#%%
#Sum columns for total cases
df_colombia = df_colombia.fillna(0)
for i in range(len(columns_ordered)):
    if i+1 < len(columns_ordered):
        col = columns_ordered[i]
        sig_col = columns_ordered[i + 1]
        df_colombia[sig_col] = df_colombia[col] + df_colombia[sig_col]
    
#df_colombia.to_excel("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\outputs\\colombia_fixed_pivoted.xlsx", index = False)

#%%
#Unpivot df
df_colombia_fixed = pd.melt(df_colombia, id_vars=['Etiquetas de fila'], value_vars=columns_ordered)        
df_colombia_fixed.to_excel("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\outputs\\colombia_fixed.xlsx", index = False)

