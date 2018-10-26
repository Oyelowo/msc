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
# =============================================================================

import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from rasterToPolygon import polygonize
import clip_raster as ras
from make_grid import create_grid
import geopandas as gpd
from shapely.geometry import box

#readthe shapefile for the area of interest
aoi_shapefile = gpd.read_file(r'E:\LIDAR_FINAL\data\AOI\fishnet_926_1sqm.shp')

bbox_aoi2 = ras.get_vector_extent(aoi_shapefile)
bbox_aoi = ras.get_raster_extent(r'E:\LIDAR_FINAL\data\AOI\clipped_mean_annual_rain.tif')
#[38.19986023835, -3.2418059025499986, 38.52486023705, -3.516805901449999]


mean_annual_filepath = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\CHELSA_bio_12.tif'
mean_annual_clipped_path = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rain_cli.tif'
mean_annual_rain_raster = rasterio.open(mean_annual_filepath)
#clip the mean annual rainfall raster data
mean_annual_rain_clipped = ras.get_clipped_raster(mean_annual_rain_raster, mean_annual_clipped_path,
                                                  bbox_aoi, 4326)



