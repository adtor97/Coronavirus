# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 16:18:37 2020

@author: USUARIO
"""

#%%
import pandas as pd
import requests
import json
from datetime import date
#%%
response = requests.get("https://coronavirus-19-api.herokuapp.com/countries")
json_df = json.dumps(response.json()) 
df_today = pd.read_json(json_df, orient = 'records')
df_today["date"] = date.today()
print(df_today, df_today[df_today.country == "Colombia"])
#%%
df_all_days = pd.read_csv("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\inputs\\base_diaria.csv", sep = ";")
print(df_all_days.shape, df_all_days[df_all_days.country == "Peru"].cases, df_all_days.date.unique())
#%%
df_all_days = pd.concat([df_all_days,df_today], axis = 0)
print(df_all_days.head(), df_all_days.columns, df_all_days.shape)
df_all_days.to_csv("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\inputs\\base_diaria.csv", sep = ";", index = False)

#%%
#fix date
fix_date = "2020-03-19"
df_all_days = df_all_days[df_all_days.date != fix_date]
df_all_days



