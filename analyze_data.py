# -*- coding: utf-8 -*-
"""
Created on Sun Mar 15 18:57:31 2020

@author: USUARIO
"""

import pandas as pd
#%%
df = pd.read_csv("C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\inputs\\base_diaria.csv", sep = ";")
df["active/cases"] = df.active / df.cases
df["critical/active"] = df.critical / df.active
df["deaths/cases"] = df.deaths / df.cases
df["recovered/cases"] = df.recovered / df.cases
df["todayCases/cases"] = df.todayCases / df.cases
df["todayDeaths/cases"] = df.todayDeaths / df.deaths
#df = df.fillna(0)
print(df)
#%%



