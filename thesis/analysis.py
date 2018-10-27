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
for month_index, month_file in enumerate(monthly_rain_raster, 1):
    print(month_index)
    output_tif = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped', calendar.month_name[month_index] + '.tif')
    print(output_tif)
    ras.clip_and_export_raster(month_file, output_tif, bbox_aoi)
    
    month_raster = rasterio.open(output_tif).read().astype(float)
    sum_rain += month_raster


   

cc = sum_rain/12

show(sum_rain,cmap='Blues', title="Mean Annual Rainfall")

# =============================================================================
# CONVERT THE RASTER FILES INTO VECTOR
# =============================================================================
monthly_rain_clipped=glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\*.tif')
for month_index, month_file in enumerate(monthly_rain_clipped, 1):
    month = calendar.month_name[month_index] 
    output_shp = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped/to_vector', month + '.shp')
    print(month)
#    month_raster = rasterio.open(month_file)
    polygonized_raster = ras.polygonize(month_file, 4326, 32737)
    polygonized_raster=polygonized_raster.rename(columns={'grid_value': month + '_temp'})
    polygonized_raster.to_file(output_shp)
 



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
# OVERLAY ANALYSIS
# =============================================================================


overlay = buildings_centroid.copy()
bb = gpd.read_file(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\january.shp')

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
    buildings_aggr['grid_ID'] = key
    buildings_aggr.loc[key,'geometry'] = group_geometry
    buildings_aggr.loc[key,'areaSum'] = group['area'].sum()
    print('Aggregating', key, group)






# =============================================================================
# 
# =============================================================================


buildings_rain  = buildings_grid.copy()
for i, month_filepath in enumerate(months_shp_filepaths, 1):
    print(i)
    month_data = gpd.read_file(month_filepath)
    month_name = calendar.month_name[month_index] 
    month_data.crs = {'init' :'epsg:32737'}
    buildings_rain_grid = gpd.sjoin(buildings_rain, month_data, how="left", op='intersects', lsuffix=month, rsuffix='_' + month_name)
    print(buildings_rain_grid.columns)
    
buildings_grid.plot(column='area', cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)

month.plot()

bg = gpd.read_file(monthly_rain_files[0])
bg.crs = {'init' :'epsg:32737'}

cc.plot()

cc.plot(column='grid_value', linewidth=0.03, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)
buildings_grid.plot(column='area', linewidth=0.03, cmap="Blues", scheme="quantiles", k=9, alpha=0.9)







































