# -*- coding: utf-8 -*-
"""
Created on Sat Mar 21 16:48:56 2020

@author: USUARIO
"""

#%%
from selenium import webdriver
import time
from bs4 import BeautifulSoup
#%%
#Automate get data 
driver = webdriver.Chrome("C:\\Users\\USUARIO\\chromedriver_win32\\chromedriver.exe")
driver.get("https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx")
time.sleep(20)
source = driver.page_source
bs = BeautifulSoup(source)
table = bs.find_all("table")

print(table[3])
table.find(tbody)
tbody.findall(tr)

#%%
import pandas as pd
ciudad_departamento = {"Anapoima":"Cundinamarca", "Armenia":"Quindio", "Barranquilla":"Atlántico",
                       "Bogotá":"Cundinamarca", "Bucaramanga":"Santander", "Buga":"Valle del Cauca", "Cajicá":"Cundinamarca",
                       "Cali":"Valle del Cauca", "Cartagena":"Bolívar", "Chía":"Cundinamarca", "Cúcuta":"Norte de Santander",
                       "Dosquebradas":"Risaralda", "Envigado":"Antioquia", "Ibagué":"Tolima", "Itagüí":"Antioquia",
                       "Madrid":"Cundinamarca", "Manizales":"Caldas", "Medellín":"Antioquia", "Neiva":"Huila",
                       "Palmira":"Valle del Cauca", "Pereira":"Risaralda", "Popayán":"Cauca", "Rionegro":"Antioquia",
                       "Santa Marta":"Magdalena", "Soacha":"Cundinamarca", "Subachoque":"Cundinamarca", "Tolima":"Tolima",
                       "Villa del Rosario":"Norte de Santander", "Villavicencio":"Meta", "Viterbo":"Caldas",
                       "Guarne":"Antioquia", "Calarcá":"Quindio", "Valledupar":"Cesar",
                       "La Dorada":"Caldas", "Chinchiná":"Caldas", "San Andrés Islas":"Archipiélago de San Andrés, Providencia y Santa Catalina",
                       "Yumbo":"Valle del Cauca", "Yopal":"Casanare"
                       }


print("ciudades: ", list(ciudad_departamento.keys()))
print("\n")
print("departamentos: ", list(ciudad_departamento.values()))

#%%
#Fuente original: https://www.ins.gov.co/Noticias/Paginas/Coronavirus.aspx
path_to_csv = "C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\inputs\\casos_colombia.csv"
df_colombia = pd.read_csv(path_to_csv)
faltantes = []
for ciudad in df_colombia["Ciudad de ubicación"].unique():
    if ciudad not in list(ciudad_departamento.keys()):
        faltantes = faltantes + [ciudad]
print("ciudades que faltan agregar al diccionario: ", faltantes)
#%%
df_colombia["Ciudad de ubicación"] = df_colombia["Ciudad de ubicación"].replace(ciudad_departamento)
df_colombia.rename(columns = {"Ciudad de ubicación":"Departamento"}, inplace = True)
df_colombia = df_colombia.pivot_table(index='Departamento', columns='Fecha de diagnóstico', aggfunc=len, fill_value=0)["ID de caso"]
df_colombia = df_colombia.reset_index(level=0, drop=False)
#df_colombia = df_colombia.reset_index(level=1, drop=True)
print(df_colombia.head(), df_colombia["Departamento"].values, df_colombia.columns, df_colombia.shape)

#%%
#create missing columns and order
columns_missing = ["07/03/2020", "08/03/2020", "10/03/2020"]
for col in columns_missing:
    df_colombia[col] = 0
columns_ordered = df_colombia.columns[df_colombia.columns != 'Departamento'].sort_values().to_list()
df_colombia = df_colombia[["Departamento"] + columns_ordered]
print(df_colombia.head(), df_colombia.columns, df_colombia.shape)

#%%
#Sum columns for total cases
df_colombia = df_colombia.fillna(0)
for i in range(len(columns_ordered)):
    if i+1 < len(columns_ordered):
        col = columns_ordered[i]
        sig_col = columns_ordered[i + 1]
        df_colombia[sig_col] = df_colombia[col] + df_colombia[sig_col]

path_save_pivoted =  "C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\outputs\\colombia_fixed_pivoted.xlsx"
df_colombia.to_excel(path_save_pivoted, index = False)

#%%
#Unpivot df
df_colombia_fixed = pd.melt(df_colombia, id_vars=['Departamento'], value_vars=columns_ordered)  
path_save_final = "C:\\Users\\USUARIO\\Desktop\\Python\\Coronavirus\\outputs\\colombia_fixed.xlsx"       
df_colombia_fixed.to_excel(path_save_final, index = False)

#%%
#Send email with update
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os.path
fecha = df_colombia_fixed["Fecha de diagnóstico"].max()
email="adrian135torrejon@gmail.com"
password="Entel2000"
send_to_email="pablo.diazv@pucp.edu.pe"
subject="Update Colombia hasta " + fecha
message=""
file_location= path_save_final

msg=MIMEMultipart()
msg["From"]=email
msg["To"]=send_to_email
msg["Subject"]=subject
msg.attach(MIMEText(message,"plain"))
filename=os.path.basename(file_location)
attachment=open(file_location,"rb")
part=MIMEBase("application","octet-stream")
part.set_payload((attachment).read())
encoders.encode_base64(part)
part.add_header('Content-Disposition',"attachment; filename= %s" % filename)
msg.attach(part)
server=smtplib.SMTP('smtp.gmail.com',587)
server.starttls()
server.login(email,password)
text=msg.as_string()
server.sendmail(email,send_to_email,text)
server.quit()


