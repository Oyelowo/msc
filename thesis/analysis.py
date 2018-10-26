import rasterio
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

help(clip_raster)


fp= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\test_lowo.tif'


grid_path = r'E:\LIDAR_FINAL\data\2015\fishnet\fishnet_925_1sqm.shp'

data = rasterio.open(fp)
print(data)
show((data, 1), cmap='terrain')
# plt.show()
fishnet = gpd.read_file(grid_path)



print(data.crs)
print(fishnet.crs)
polygonized_raster = polygonize(fp, data.crs, 32737)
polygonized_raster.plot(column='raster_val', linewidth=0.03, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)


polygonized_raster.to_file('lowo.shp')
# show((data, 1), cmap='terrain')
# plt.show()