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




#For bounding box in longitude and latitude
grid = ras.create_grid(926.1, 926.1, bbox_aoi, is_utm=True)

#For bounding box in UTM Zone
grid = ras.create_grid(926.1, 926.1, bbox_aoi2, is_utm=False)

grid = ras.create_grid(gridHeight=926.1, gridWidth=926.1,shapefile=aoi_shapefile)
grid.plot()


# CREATE A FISHNET/GRID OF 926.1m PIXEL
grid_path = r'E:\LIDAR_FINAL\data\grid\grid.shp'
points=gpd.read_file(grid_path)
minx,miny,maxx,maxy =  aoi_shapefile.total_bounds
bbox_aoi2=[minx,miny,maxx,maxy]

#grid_output_fp= r'E:\LIDAR_FINAL\data\grid\grid.shp'


# TO CREATE THE GRID, YOU CAN EITHER USE A SHAPEFILE OR INPUT THE BBOX MANUALLY
grid = ras.create_grid(gridHeight=926.1, gridWidth=926.1, bbox=bbox_aoi, is_utm=False, zone_number=37)
grid.plot()
