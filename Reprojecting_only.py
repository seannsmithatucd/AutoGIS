#!/usr/bin/env python
# coding: utf-8

# In[1]:

import geopandas as gpd
import glob


# In[2]:

DATA_DIR = '.\Data'  # data folder containing shape files
rep_folder = '.\Data\\reprojected' # path to folder you want reprojected files to go to

files = glob.glob(f'{DATA_DIR}/*.shp')
print(files)


# Below cell can be used to check that the path to the reprojected folder looks right, and that the a new name for the reprojected files is generated correctly.

# In[ ]:

# for shp in files:
#     print(shp)
#     txt = shp.split("\\")
#     print(f"{rep_folder}\{txt[-1][:-4]}_reprojected.shp")


# In[3]:

shp_files_proj = []  # empy list where reprojected shape files will be added (except boundary)

for shp in files:
    print(shp)
    file = gpd.read_file(shp)
    print("Original crs:", file.crs)
    if file.crs == "epsg:2232":
        print("No need to reproject")
    else:
        file = file.to_crs(epsg=2232)
        print("New crs:", file.crs)
    if "Boundary" in shp:
        boundary = file  # keeping boundary file seperate
    else:
        shp_files_proj.append(file)
    txt = shp.split("\\")
    file.to_file(f"{rep_folder}\{txt[-1][:-4]}_reprojected.shp") # saves file to reprojected folder


# In[4]:

for shp in shp_files_proj:
    shp.plot()


# In[5]:

boundary.plot()
