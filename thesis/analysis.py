# =============================================================================
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import matplotlib.pyplot as plt
from osgeo import gdal
import utm
from rasterToPolygon import polygonize
import clip_raster
import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np
# =============================================================================

import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
import geopandas as gpd
from shapely.geometry import box
import seaborn as sns
import glob
import os
import calendar
import re

from rasterToPolygon import polygonize
import clip_raster as ras

#readthe shapefile for the area of interest
aoi_shapefile = gpd.read_file(r'E:\LIDAR_FINAL\data\AOI\fishnet_926_1sqm.shp')

bbox_aoi2 = ras.get_vector_extent(aoi_shapefile)
bbox_aoi = ras.get_raster_extent(r'E:\LIDAR_FINAL\data\AOI\clipped_mean_annual_rain.tif')
#[38.19986023835, -3.2418059025499986, 38.52486023705, -3.516805901449999]


#LOAD THE FILEPATH
mean_annual_filepath = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\CHELSA_bio_12.tif'
mean_annual_clipped_path = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rain_clipped.tif'
mean_annual_rain_raster = rasterio.open(mean_annual_filepath)
#clip the mean annual rainfall raster data
mean_annual_rain_clipped = ras.get_clipped_raster(mean_annual_rain_raster, mean_annual_clipped_path,
                                                  bbox_aoi, 4326)

#READ THE VALUES OF THE JUST CLIPPED RASTER
mean_annual_rain = rasterio.open(mean_annual_clipped_path).read().astype(float)


#SPECIFY PLOT SIZE IN THE CONSOLE
plt.rcParams['figure.figsize'] = (4, 12) 


#PLOT
sns.set_style("white")
# Plot newly classified and masked raster
fig, ax = plt.subplots(figsize = (3,2))
show((mean_annual_rain_clipped, 1),cmap='Blues', title="Mean Annual Rainfall")
#show((clipped, 1), cmap='Blues', title="Mean Annual Rainfall", contour=True)


# CLIP ALL THE MONTHLY DATA AND ALSO SUM THEM
sum_rain = 0
monthly_rain_raster = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\CHELSA*.tif')
for i, month_file_path in enumerate(monthly_rain_raster, 1):
    print(i)
    filename = os.path.basename(month_file_path)
#    Match the first number in the file name which is the month
    month_number = re.search(r'\d+', filename).group()
    
    month_name = calendar.month_name[int(month_number)]
    output_tif = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped', month_name[:3]+'_rain' + '.tif')
    print(output_tif)
    ras.clip_and_export_raster(month_file_path, output_tif, bbox_aoi)
    
    month_raster = rasterio.open(output_tif).read().astype(float)
    sum_rain += month_raster


   

cc = sum_rain/12

show(sum_rain,cmap='Blues', title="Mean Annual Rainfall")

# =============================================================================
# CONVERT THE RASTER FILES INTO VECTOR
# =============================================================================
monthly_rain_clipped=glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\*.tif')
for i, month_file in enumerate(monthly_rain_clipped, 1):
    month_field_name = os.path.basename(month_file)[:3] + '_rain'
    output_shp = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped/to_vector', month_field_name + '.shp')
    print(month_field_name)
#    month_raster = rasterio.open(month_file)
    polygonized_raster = ras.polygonize(month_file, 4326, 32737)
    polygonized_raster=polygonized_raster.rename(columns={'grid_value': month_field_name})
    polygonized_raster.to_file(output_shp)
    
#    FOR TEST PURPOSE
    month_rain_data_test = gpd.read_file(output_shp)
    month_rain_data_test.plot(column=month_field_name, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)

 



# =============================================================================
# 
# # CREATE A FISHNET/GRID OF 926.1m PIXEL
# =============================================================================
#generating grid by directly providing the bounding box
grid = ras.create_grid(926.1, 926.1, bbox_aoi, is_utm=False)
grid['grid_ID'] = grid.index + 1
grid = grid.reset_index(drop=True)
#generating grid based on shapefile extent
#grid2 = ras.create_grid(926.1, 926.1, shapefile=aoi_shapefile)

#grid = ras.create_grid(gridHeight=926.1, gridWidth=926.1,shapefile=aoi_shapefile)
grid.plot()

grid_path = r'E:\LIDAR_FINAL\data\grid\grid.shp'
grid.to_file(grid_path)
# =============================================================================
# 
# =============================================================================


# =============================================================================
# WORKING WITH THE BUILDING SHAPEFILE
# =============================================================================
buildings_fp = r'E:\LIDAR_FINAL\data\2015\buildings\buildings_2015_simplified.shp'
buildings_shp = gpd.read_file(buildings_fp)

# calculate area and centroid of the buildings
buildings_shp['area'] = buildings_shp['geometry'].area

# filter roof areas lower than 10sqm or higher than 2000sqm

buildings_shp = buildings_shp.loc[(buildings_shp['area']>10) & (buildings_shp['area']<2000)]

# get the centroid of every building
buildings_shp['centroid']= buildings_shp['geometry'].centroid


buildings_centroid = buildings_shp.copy()
buildings_centroid['geometry'] = buildings_shp['centroid']
buildings_centroid = buildings_centroid.reset_index(drop=True)

#set ID for the filtered buildings. Start from one
buildings_centroid['ID'] =  buildings_centroid.index + 1
del buildings_centroid['centroid']


centroid_fp = r'E:\LIDAR_FINAL\data\2015\buildings_centroid\buildings_centroid.shp'
buildings_centroid.to_file(centroid_fp)
#buildings_centroid.plot()

# =============================================================================
# 
# =============================================================================


# =============================================================================
# SPATIAL JOIN
# =============================================================================

buildings_grid = gpd.sjoin(grid,buildings_centroid, how="left", op='intersects')
months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')

#The op options determines the type of join operation to apply. op can be set to “intersects”, “within” or 
#“contains” (these are all equivalent when joining points to polygons, but differ when 
#joining polygons to other polygons or lines).
grid.plot()



buildings_grid.columns

# =============================================================================
# AGGREGATE ROOF AREAS BASED ON GRID ID
# =============================================================================

buildings_grouped = buildings_grid.groupby('grid_ID')
buildings_aggr = gpd.GeoDataFrame()
#buildings_aggr['geometry']=None
for key, group  in buildings_grouped:
    group_geometry = group.iloc[0]['geometry']
    buildings_aggr.loc[key, 'grid_ID'] = key
    buildings_aggr.loc[key,'geometry'] = group_geometry
    buildings_aggr.loc[key,'area_sum'] = group['area'].sum()
    print('Aggregating', key, group['area'].sum())


buildings_aggr.plot('area_sum', linewidth=0.03, cmap="Blues", scheme="quantiles", k=19, alpha=0.9)



# =============================================================================
# AGGREGATE RAINFALL DATA
# =============================================================================



kkr = gpd.read_file(months_shp_filepaths[0])
kk2 = gpd.read_file(months_shp_filepaths[1])

#test['geometry'] = test.centroid
def aggregate_grid_rain(new_dataframe, old_dataframe, month_field_name):
    grouped_data = old_dataframe.groupby('grid_ID')
    #buildings_aggr['geometry']=None
    for key, group  in grouped_data:
        group_geometry = group.iloc[0]['geometry']
        new_dataframe.loc[key, 'grid_ID'] = key
        new_dataframe.loc[key,'geometry'] = group_geometry
        new_dataframe.loc[key, month_field_name] = group[month_field_name].mean()
        print('Aggregating', key, month_field_name, group[month_field_name].mean())
    return new_dataframe

print(grid.crs, )
kktest = aggregate_grid_rain(buildings_aggr, kkr, 32737, 'Apr_rain')



kktest.plot(column='Apr_rain', cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)


# =============================================================================
# 
# =============================================================================

months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')


buildings_rain_aggr = gpd.GeoDataFrame()
buildings_rain  = buildings_grid.copy()
del buildings_rain['index_right']
for i, month_filepath in enumerate(months_shp_filepaths, 1):  
    print(i)
    month_rain_data = gpd.read_file(month_filepath)
    
    buildings_rain.crs = {'init' :'epsg:32737'}
    month_rain_data.crs= {'init' :'epsg:32737'}
    
    joined_data = gpd.sjoin(buildings_rain, month_rain_data, how='left', op='intersects')
    
#    Get field name from file name and exclude the file format
    month_field_name = os.path.basename(month_filepath)[:-4]
    print(month_field_name)
    
    buildings_rain_aggr = aggregate_grid_rain(buildings_rain_aggr, joined_data, month_field_name)
    

month_data.columns
    
    buildings_rain = gpd.sjoin(buildings_rain, month_data, how="left", op='intersects')
    del buildings_rain['index_right']
    print(buildings_rain.columns)
    
month_rain_data = gpd.read_file(months_shp_filepaths[0])    
month_rain_data.plot(column='Apr_rain', cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)

month.plot()

bg = gpd.read_file(monthly_rain_files[0])
bg.crs = {'init' :'epsg:32737'}

cc.plot()

cc.plot(column='grid_value', linewidth=0.03, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)
buildings_grid.plot(column='area', linewidth=0.03, cmap="Blues", scheme="quantiles", k=9, alpha=0.9)







































