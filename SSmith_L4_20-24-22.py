
import numpy as np
import numpy.ma as ma
import glob
import rasterio
from rasterio.plot import show, show_hist
from rasterio.warp import calculate_default_transform, reproject, Resampling
from rasterio import Affine as A
import random
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
from scipy.spatial import ckdtree, kdtree, cKDTree

#open each raster> fix> create moving window> generate mean average
srcRst_PA = rasterio.open('./protected_areas.tif')
srcRst_S = rasterio.open('./slope.tif')
srcRst_UA = rasterio.open('./urban_areas.tif')
srcRst_WB = rasterio.open('./water_bodies.tif')
srcRst_80 = rasterio.open('./ws80m.tif')

dstCrs_PA = {'init': 'EPSG:4326'}

transform, width, height = calculate_default_transform(
        srcRst_PA.crs, dstCrs_PA, srcRst_PA.width, srcRst_PA.height, *srcRst_PA.bounds)

dstCrs_S = {'init': 'EPSG:4326'}

transform, width, height = calculate_default_transform(
        srcRst_S.crs, dstCrs_S, srcRst_S.width, srcRst_S.height, *srcRst_S.bounds)

dstCrs_UA = {'init': 'EPSG:4326'}

transform, width, height = calculate_default_transform(
        srcRst_UA.crs, dstCrs_UA, srcRst_UA.width, srcRst_UA.height, *srcRst_UA.bounds)

dstCrs_WB = {'init': 'EPSG:4326'}

transform, width, height = calculate_default_transform(
        srcRst_WB.crs, dstCrs_WB, srcRst_WB.width, srcRst_WB.height, *srcRst_WB.bounds)

dstCrs_80 = {'init': 'EPSG:4326'}

transform, width, height = calculate_default_transform(
        srcRst_80.crs, dstCrs_80, srcRst_80.width, srcRst_80.height, *srcRst_80.bounds)

#update meta of the destination
kwargs = srcRst_PA.meta.copy()
kwargs.update({
        'crs': dstCrs_PA,
        'transform': transform,
        'width': width,
        'height': height
    })

#update meta of the destination
kwargs = srcRst_S.meta.copy()
kwargs.update({
        'crs': dstCrs_S,
        'transform': transform,
        'width': width,
        'height': height
    })

#update meta of the destination
kwargs = srcRst_UA.meta.copy()
kwargs.update({
        'crs': dstCrs_UA,
        'transform': transform,
        'width': width,
        'height': height
    })

#update meta of the destination
kwargs = srcRst_WB.meta.copy()
kwargs.update({
        'crs': dstCrs_WB,
        'transform': transform,
        'width': width,
        'height': height
    })

#update meta of the destination
kwargs = srcRst_80.meta.copy()
kwargs.update({
        'crs': dstCrs_80,
        'transform': transform,
        'width': width,
        'height': height
    })

#open destination raster
dstRst_PA4326 = rasterio.open('./data4326/protected_areas4326.tif', 'w', **kwargs)
dstRst_S4326 = rasterio.open('./data4326/slope4326.tif', 'w', **kwargs)
dstRst_UA4326 = rasterio.open('./data4326/urban_areas4326.tif', 'w', **kwargs)
dstRst_WB4326 = rasterio.open('./data4326/water_bodies4326.tif', 'w', **kwargs)
dstRst_804326 = rasterio.open('./data4326/ws80m4326.tif', 'w', **kwargs)

#reproject & save/close destination
for i in range(1, srcRst_PA.count + 1):
    reproject(
        source=rasterio.band(srcRst_PA, i),
        destination=rasterio.band(dstRst_PA4326, i),
        #src_transform=srcRst.transform,
        src_crs_PA=srcRst_PA.crs,
        #dst_transform=transform,
        dst_crs_PA=dstCrs_PA,
        resampling=Resampling.nearest)
#close destination raster
dstRst_PA4326.close()

#reproject & save/close destination
for i in range(1, srcRst_S.count + 1):
    reproject(
        source=rasterio.band(srcRst_S, i),
        destination=rasterio.band(dstRst_S4326, i),
        #src_transform=srcRst.transform,
        src_crs_S=srcRst_S.crs,
        #dst_transform=transform,
        dst_crs_S=dstCrs_S,
        resampling=Resampling.nearest)
#close destination raster
dstRst_S4326.close()

#reproject & save/close destination
for i in range(1, srcRst_UA.count + 1):
    reproject(
        source=rasterio.band(srcRst_UA, i),
        destination=rasterio.band(dstRst_UA4326, i),
        #src_transform=srcRst.transform,
        src_crs_UA=srcRst_UA.crs,
        #dst_transform=transform,
        dst_crs_UA=dstCrs_UA,
        resampling=Resampling.nearest)
#close destination raster
dstRst_UA4326.close()

#reproject & save/close destination
for i in range(1, srcRst_WB.count + 1):
    reproject(
        source=rasterio.band(srcRst_WB, i),
        destination=rasterio.band(dstRst_WB4326, i),
        #src_transform=srcRst.transform,
        src_crs_WB=srcRst_WB.crs,
        #dst_transform=transform,
        dst_crs_WB=dstCrs_WB,
        resampling=Resampling.nearest)
#close destination raster
dstRst_WB4326.close()

#reproject & save/close destination
for i in range(1, srcRst_80.count + 1):
    reproject(
        source=rasterio.band(srcRst_80, i),
        destination=rasterio.band(dstRst_804326, i),
        #src_transform=srcRst.transform,
        src_crs_80=srcRst_80.crs,
        #dst_transform=transform,
        dst_crs_80=dstCrs_80,
        resampling=Resampling.nearest)
#close destination raster
dstRst_804326.close()

shape = np.ones((11,9))
#provided Moving Window
def mean_filter(ma, mask):

    pct_array = np.zeros(ma.shape)
    win_area = float(mask.sum())
    row_dim = mask.shape[0]//2
    col_dim = mask.shape[1]//2
    for row in range(row_dim,ma.shape[0]-row_dim):
        for col in range(col_dim,ma.shape[1]-col_dim):
            win = ma[row-row_dim:row+row_dim+1,col-col_dim:col+col_dim+1]
            pct_array[row,col] = win.sum()
    return pct_array/win_area

#read list of rasters
files = glob.glob(r'.\data4326\*.tif')

#create empty array
empty_array = []

for i in files:
    with rasterio.open(i) as data:
        array = data.read(1)
        array = np.where(array < 0, 0, array)
        mean_a = np.zeros_like(array)
        
        for row in range(5, array.shape[0] - 5):
            for col in range(4, array.shape[1] - 4):
                window = array[row-5:row+5 +1, col - 4:col+4 +1]
                mean_a[row, col] = window.mean()
        empty_array.append(mean_a)

#site conditions to generate boolean arrays
#protected #3. Less than 5% of the site can be within protected areas.
empty_array[0] = np.where(empty_array[0] < 0.05, 1, 0)
#slope #4. An average slope of less than 15 degrees is necessary for the development plans.
empty_array[1] = np.where(empty_array[1] < 15, 1, 0)
#urban#1. The site cannot contain urban areas.
empty_array[2] = np.where(empty_array[2] !=0, 0, 1)
#water#2. Less than 2% of land can be covered by water bodies.
empty_array[3] = np.where(empty_array[3] < 0.02, 1, 0)
#wind#5. The average wind speed must be greater than 8.5m/s.cv
empty_array[4] = np.where(empty_array[4] < 8.5, 0, 1)
#sum arrays
array_sum = empty_array[0] + empty_array[1] + empty_array[2] + empty_array[3] + empty_array[4]

type(dstRst_PA4326)


#create a final boolean array from the sum of the arrays
final_array = np.where(array_sum == 5, 1, 0)
print('The total number of suitable sites:', final_array.sum())

#change dtype of the final boolean
final_array = final_array.astype('float64')


type(final_array)

#create tif from final boolean
with rasterio.open(r'./data4326/slope4326.tif') as dataset:
        
    with rasterio.open(f'./data4326/suitable_sites4326.tif', 'w',
                      driver='GTiff',
                      height=final_array.shape[0],
                      width=final_array.shape[1],
                      count=1,
                      dtype=final_array.dtype,
                      crs=dataset.crs,
                      transform = dataset.transform, 
                      nodata=-9999
                      ) as tif_dataset:
        tif_dataset.write(final_array,1)


#open w/ rasterio> read as array> display suitable sites
with rasterio.open(r'./data4326/suitable_sites4326.tif') as dataset2:
    test_array = dataset2.read(1)

show(test_array)

#generate list of transmission station coordinates
xs = []
ys = []
with open(r'./data4326/transmission_stations.txt') as coords:
    lines = coords.readlines()[1:]
    for l in lines:
        x,y = l.split(',')
        xs.append(float(x))
        ys.append(float(y))
    stations = np.vstack([xs, ys])
    stations = stations.T

#find centroids of suitable sites
with rasterio.open(r'./data4326/suitable_sites4326.tif') as file:
    
    bounds = file.bounds
    topLeft = (bounds[0], bounds[3])
    lowRight = (bounds[2], bounds[1])
    cellSize = 1000

    x_coords = np.arange(topLeft[0] + cellSize/2, lowRight[0], cellSize) 
    y_coords = np.arange(lowRight[1] + cellSize/2, topLeft[1], cellSize) 
    
    x, y = np.meshgrid(x_coords, y_coords)
    cent_coords = np.c_[x.flatten(), y.flatten()]

#multiply total centroids by the final boolean in part 1 to get the final list of centroids
suitable_cent_coords = []
for sx, sy in zip(cent_coords, final_array.flatten()):
        sxcoord = np.multiply(sx[0], sy)
        sycoord = np.multiply(sx[1], sy)
        if sxcoord != 0 and sycoord != 0:
            suitable_cent_coords.append([sxcoord, sycoord])
