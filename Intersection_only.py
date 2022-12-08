#!/usr/bin/env python
# coding: utf-8

# In[8]:

import geopandas as gpd
import glob


# In[9]:

DATA_DIR = '.\Data\\reprojected'  # data folder containing REPROJECTED shape files
inter_folder = '.\Data\intersected' # path to folder you want intersected files to go to

files = glob.glob(f'{DATA_DIR}/*.shp')
print(files)


# In[10]:

shp_files_proj = []
names = []

for shp in files:
    file = gpd.read_file(shp)
    if "Boundary" in shp:
        boundary = file
    else:
        shp_files_proj.append(file)
        names.append(shp)

        
# In[11]:

for shp in names:
    print(shp)
    txt = shp.split("\\")
    print(f"{inter_folder}\{txt[-1][:-4]}_intersected.shp")


# In[12]:

def intersection(boundary, shps):
    """
    Performs an intersection for every shape file in a list using the provided boundary.

    boundary: geodataframe of project boundary (polygon)
    files: list containing the geodataframes you want to intersect
    returns the list of interesected geodataframes
    """
    list = []
    for i, shp in enumerate(shps):
        intersection = gpd.overlay(shp, boundary, how="intersection")
        list.append(intersection)
        txt = names[i].split("\\")
        intersection.to_file(f"{inter_folder}\{txt[-1][:-4]}_intersected.shp")
    return list


# In[13]:

intersected_shps = intersection(boundary, shp_files_proj)


# In[14]:

for shp in intersected_shps: 
    shp.plot()

    
