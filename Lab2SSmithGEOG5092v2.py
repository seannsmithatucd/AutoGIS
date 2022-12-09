
import pandas as pd
import fiona
import geopandas as gpd
import glob
from shapely.geometry import Point, LineString, Polygon
from rasterstats import zonal_stats

a4='C:/lab2/agriculture/GLOBCOVER_2004_lab2.tif'
a9='C:/lab2/agriculture/GLOBCOVER_2009_lab2.tif'
d1='C:\lab2\districts\district01.txt'
d5='C:\lab2\districts\district05.txt'
d6='C:\lab2\districts\district06.txt'

data1 = pd.read_csv(d1, sep='\t')
data11 = data1.values
data1_polygon=Polygon(data11)
data5 = pd.read_csv(d5, sep='\t')
data55 = data5.values
data5_polygon=Polygon(data55)
data6 = pd.read_csv(d6, sep='\t')
data66 = data6.values
data6_polygon=Polygon(data66)

District01gdf = 'Vertices', data1.shape[0]
District05gdf = 'Vertices', data5.shape[0]
District06gdf = 'Vertices', data6.shape[0]

dist_i = {}
district_vert = [District01gdf, District05gdf, District06gdf]

dist_num = ['01', '05', '06']

blank_names = [' ', '  ', '   ']
for idx, dist in enumerate(blank_names):
    dist_i[dist] = {'num_coords': district_vert[idx], 'districts': dist_num[idx]}

districts_df = pd.DataFrame.from_dict(dist_i, orient='index')

gdf1 = gpd.GeoDataFrame(geometry=[data1_polygon])
gdf1.to_file(filename='dPolygon1.shp', driver='ESRI Shapefile')
geodf1 = gpd.read_file("dPolygon1.shp")
z14=zonal_stats(geodf1,a4,stats="count")
zt14=zonal_stats(geodf1,a4,categorical=True)

value_dict=z14[0]
value_z14=value_dict['count']
value_dict=zt14[0]
value_zt14=value_dict[1]
zpct14=round((((value_zt14)/(value_z14))*100),0)

gdf1 = gpd.GeoDataFrame(geometry=[data1_polygon])
gdf1.to_file(filename='dPolygon1.shp', driver='ESRI Shapefile')
geodf1 = gpd.read_file("dPolygon1.shp")
z19=zonal_stats(geodf1,a9,stats="count")
zt19=zonal_stats(geodf1,a9,categorical=True)

value_dict=z19[0]
value_z19=value_dict['count']
value_dict=zt19[0]
value_zt19=value_dict[1]
zpct19=round((((value_zt19)/(value_z19))*100),0)

gdf5 = gpd.GeoDataFrame(geometry=[data5_polygon])
gdf5.to_file(filename='dPolygon5.shp', driver='ESRI Shapefile')
geodf5 = gpd.read_file("dPolygon5.shp")
z54=zonal_stats(geodf5,a4,stats="count")
zt54=zonal_stats(geodf5,a4,categorical=True)

value_dict=z54[0]
value_z54=value_dict['count']
value_dict=zt54[0]
value_zt54=value_dict[1]
zpct54=round((((value_zt54)/(value_z54))*100),0)

gdf5 = gpd.GeoDataFrame(geometry=[data5_polygon])
gdf5.to_file(filename='dPolygon5.shp', driver='ESRI Shapefile')
geodf5 = gpd.read_file("dPolygon5.shp")
z59=zonal_stats(geodf5,a9,stats="count")
zt59=zonal_stats(geodf5,a9,categorical=True)

value_dict=z59[0]
value_z59=value_dict['count']
value_dict=zt59[0]
value_zt59=value_dict[1]
zpct59=round((((value_zt59)/(value_z59))*100),0)

gdf6 = gpd.GeoDataFrame(geometry=[data6_polygon])
gdf6.to_file(filename='dPolygon6.shp', driver='ESRI Shapefile')
geodf6 = gpd.read_file("dPolygon6.shp")
z64=zonal_stats(geodf6,a4,stats="count")
zt64=zonal_stats(geodf6,a4,categorical=True)

value_dict=z64[0]
value_z64=value_dict['count']
value_dict=zt64[0]
value_zt64=value_dict[1]
zpct64=round((((value_zt64)/(value_z64))*100),0)

gdf6 = gpd.GeoDataFrame(geometry=[data6_polygon])
gdf6.to_file(filename='dPolygon6.shp', driver='ESRI Shapefile')
geodf6 = gpd.read_file("dPolygon6.shp")
z69=zonal_stats(geodf6,a9,stats="count")
zt69=zonal_stats(geodf6,a9,categorical=True)

value_dict=z69[0]
value_z69=value_dict['count']
value_dict=zt69[0]
value_zt69=value_dict[1]
zpct69=round((((value_zt69)/(value_z69))*100),0)

print(districts_df)

print('district 01 agricultural land')
print('in 2004 =', zpct14,'%')
print('in 2009 =', zpct19,'%')

print('district 05 agricultural land')
print('in 2004 =', zpct54,'%')
print('in 2009 =', zpct59,'%')

print('district 06 agricultural land')
print('in 2004 =', zpct64,'%')
print('in 2009 =', zpct69,'%')
