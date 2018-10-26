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
from gdalconst import GA_ReadOnly
from osgeo import gdal
import os

'''
Author: Oyelowo Oyedayo
Purpose: For my thesis 
Contact: www.github.com(Oyelowo)
'''
def get_raster_extent(raster_file_path):
    data = gdal.Open(raster_file_path, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    print('[minx, maxy , maxx, miny] is',  [minx, maxy , maxx, miny] )
    data = None
    return [minx, maxy , maxx, miny]


def get_vector_extent(shapefile='', geometry_field='geometry', utm_zone=37, northern=False):
    '''
    extent: An array of the extent of the window in this order: [minx, maxy , maxx, miny]
    '''
    minx, miny, maxx, maxy = shapefile[geometry_field].total_bounds
    latlow, lonlow = utm.to_latlon(minx, miny, utm_zone, northern=northern)
    lathigh, lonhigh = utm.to_latlon(maxx, maxy, utm_zone, northern=northern)
    return [lonlow, lathigh, lonhigh, latlow] 


def clip_and_export_raster(raster_path, output_tif, extent):
    '''
    extent: An array of the extent of the window in this order: [minx, maxy , maxx, miny]
    '''
    raster_data = gdal.Open(raster_path)
    raster_data = gdal.Translate(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif', raster_data, projWin=extent)
    raster_data = None
#    data = rasterio.open(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif')
#    show((data, 1), cmap='terrain')
    
   

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]




def get_clipped_raster(raster_data, output_path, extent, bbox_epsg_code=4326):
    '''
    extent: An array of the extent of the window in this order: [minx, maxy , maxx, miny]
    '''
    minx, maxy , maxx, miny = extent
    bbox = box(minx, maxy , maxx, miny)

    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(bbox_epsg_code))
    
    try:
        geo = geo.to_crs(crs=raster_data.crs.data)
    except ValueError: 
        print('The raster crs is not defined')
    coords = getFeatures(geo)
    
    clipped_img, clipped_img_transform = mask(raster=raster_data, shapes=coords, crop=True)
    clipped_img_meta = raster_data.meta.copy()
    clipped_img_meta.update({"driver": "GTiff",
              "height": clipped_img.shape[1],
                "width": clipped_img.shape[2],
                 "transform": clipped_img_transform,
                "crs": raster_data.crs.data})
    
    with rasterio.open(output_path, "w", **clipped_img_meta) as output:
        output.write(clipped_img)
            
    clipped = rasterio.open(output_path)
    show((clipped, 1), cmap='terrain')
    return clipped_img
