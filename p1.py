#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np 
import pandas as pd
import json 
import requests 
from pandas.io.json import json_normalize
from bs4 import BeautifulSoup
import lxml


source = requests.get("https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M").text
canada_list = BeautifulSoup(source, 'lxml') 
toronto_list = pd.DataFrame(columns=['Postalcode','Borough', 'Neighborhood'])

content = canada_list.find('div', class_='mw-parser-output')
table = content.table.tbody 
postcode = 0
borough = 0
neighborhood = 0

for tr in table.find_all('tr'):
    i = 0
    for td in tr.find_all('td'):
        if i == 0: 
            postcode = td.text
            i = i + 1
        elif i == 1: 
            borough = td.text
            i = i + 1
        elif i == 2: 
            neighborhood = td.text.strip('\n').replace(']','') 
    toronto_list = toronto_list.append({'Postalcode': postcode,'Borough': borough,'Neighborhood': neighborhood},ignore_index=True)
    
toronto_list = toronto_list[toronto_list.Borough!='Not assigned']
toronto_list = toronto_list[toronto_list.Borough!= 0]
toronto_list.reset_index(drop = True, inplace = True)

#
i = 0
for i in range(0,toronto_list.shape[0]):
    if toronto_list.iloc[i][2] == 'Not assigned':
        toronto_list.iloc[i][2] = toronto_list.iloc[i][1]
        i = i+1
        
#print the dataframe
df = toronto_list.groupby(['Postalcode','Borough'])['Neighborhood'].apply(', '.join).reset_index()
df.head(11)


# In[ ]:




