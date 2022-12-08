#!/usr/bin/env python
# coding: utf-8

# In[1]:

import pandas as pd
import geopandas as gpd
import glob


# In[2]:

DATA_DIR = '.\Data\intersected'  # data folder containing INTERSECTED shape files
merge_folder = '.\Data\merged' # path to folder you want merged files to go to

files = glob.glob(f'{DATA_DIR}/*.shp')
print(files)


# In[3]:

intersected_shps = []

for shp in files:
    file = gpd.read_file(shp)
    intersected_shps.append(file)


# In[4]:

Deficient = intersected_shps[0]
Existing = intersected_shps[1]
Missing = intersected_shps[2]


# In[5]:

merge = pd.concat([Deficient, Missing])
merge.to_file(f"{merge_folder}\Def_Mis_merged.shp")
merge.plot()
