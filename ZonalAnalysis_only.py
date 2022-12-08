#!/usr/bin/env python
# coding: utf-8

# In[36]:

import pandas as pd
import geopandas as gpd
import rasterio
from rasterstats import zonal_stats


# In[43]:

import warnings
warnings.filterwarnings("ignore")


# In[44]:

merge = gpd.read_file(".\Data\merged\Def_Mis_merged.shp") # open merged sidewalk shapefile
rpath = "./Data/Raster/LP_Distance_Raster_5ft.tif"  # path to distance raster from arcpro


# In[45]:

stats = zonal_stats(merge['geometry'], rpath, stats= "mean")


# In[46]:

means = []
for stat in stats:
    means.append(stat['mean'])


# In[40]:

merge['AvgDistLP'] = means


# In[41]:

merge.head() # can see that column was added


# In[42]:

merge.to_file("./Data/Raster/MeanDist_sidewalks.shp")
