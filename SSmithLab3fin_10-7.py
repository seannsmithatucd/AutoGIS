import sys
import pandas as pd
import fiona
import geopandas as gpd
import glob
from shapely.geometry import Point, LineString, Polygon
from rasterstats import zonal_stats
import numpy as np
import random
import matplotlib.pyplot as plt

#variable definitions
Sv2='C:\lab3\lab3.gpkg'
NewFile = gpd.read_file('C:\lab3\lab3.gpkg')
File_bounds = NewFile.total_bounds
HUC_w = fiona.listlayers(Sv2)
huc8=gpd.read_file(Sv2, layer='wdbhuc8')
huc12=gpd.read_file(Sv2, layer='wdbhuc12')
ssurgo=gpd.read_file(Sv2, layer='ssurgo_mapunits_lab3')

np.random.seed(0)
HUC = []

for w in HUC_w:
    if "wdbhuc" in w:
        HUC.append(w)

#create empty dictionary to append generated points
sample_points8 = {'point_id': [], 'geometry':[], 'HUC8': []}
sample_points12 = {'point_id': [], 'geometry':[], 'HUC12': []}

for p in HUC:
    HUC8_w_gdf = gpd.read_file(r'C:\lab3\lab3.gpkg')
    HUC8code = [f for f in HUC8_w_gdf.columns if 'HUC' in f][0]
    HUC12_w_gdf = gpd.read_file(r'C:\lab3\lab3.gpkg', layer=p)
    HUC12code = [f for f in HUC12_w_gdf.columns if 'HUC' in f][0]
    for idx, row in HUC8_w_gdf.iterrows():
        huc8_bounds = row['geometry'].bounds
        hucsqkm = row["Shape_Area"]/1000000
        nearinthuc=(int(round(hucsqkm*0.05)))
        s8 = 0
        while s8 < nearinthuc:
            x8 = (random.uniform(huc8_bounds[0], huc8_bounds[2]))
            y8 = (random.uniform(huc8_bounds[1], huc8_bounds[3]))
            point8 = Point(x8,y8)
            
            if row['geometry'].contains(point8):
                sample_points8['geometry'].append(point8)
                sample_points8['point_id'].append(row[HUC8code][:8])
                sample_points8['HUC8'].append(HUC8code)
                s8 += 1
    for idx, row in HUC12_w_gdf.iterrows():
        huc12_bounds = row['geometry'].bounds
        hucsqkm = row["Shape_Area"]/1000000
        nearinthuc=(int(round(hucsqkm*0.05)))
        s12 = 0
        while s12 < nearinthuc:
            x12 = (random.uniform(huc12_bounds[0], huc12_bounds[2]))
            y12 = (random.uniform(huc12_bounds[1], huc12_bounds[3]))
            point12 = Point(x12,y12)

            if row['geometry'].contains(point12):
                sample_points12['geometry'].append(point12)
                sample_points12['point_id'].append(row[HUC12code][:8])
                sample_points12['HUC12'].append(HUC12code)
                s12 += 1

