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

fp= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\CHELSA_bio_12.tif'
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\test_lowo.tif'
clipped_path= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'

# show((data, 1), cmap='terrain')
# plt.show()
grid_path = r'E:\LIDAR_FINAL\data\2015\fishnet\fishnet_925_1sqm.shp'


data = rasterio.open(fp)
fishnet = gpd.read_file(grid_path)

fishnet.crs

#import gdal


def get_raster_extent(raster_path):
    data = gdal.Open(clipped_path, GA_ReadOnly)
    geoTransform = data.GetGeoTransform()
    minx = geoTransform[0]
    maxy = geoTransform[3]
    maxx = minx + geoTransform[1] * data.RasterXSize
    miny = maxy + geoTransform[5] * data.RasterYSize
    print('[minx, maxy , maxx, miny] is',  [minx, maxy , maxx, miny] )
    data = None
    return [minx, maxy , maxx, miny]




def clip_and_export_raster(raster_path, output_tif, extent):
    '''
    extent: An array of the extent of the window in this order: [minx, maxy , maxx, miny]
    '''
    data = gdal.Open(raster_path)
    data = gdal.Translate(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif', ds, projWin=extent)
    data = None
#    data = rasterio.open(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif')
#    show((data, 1), cmap='terrain')
    
   

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]




def clip_and_export_raster(raster_data, clipped_tif_path,extent, bbox_epsg_code=4326, export=True):
    '''
    extent: An array of the extent of the window in this order: [minx, maxy , maxx, miny]
    '''
    bbox = box(*extent)

    geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(bbox_epsg_code))
    
    try:
        geo = geo.to_crs(crs=raster_data.crs.data)
    except: raise projectionError('The raster crs is not defined')
    coords = getFeatures(geo)
    
    clipped_img, clipped_img_transform = mask(raster=raster_data, shapes=coords, crop=True)
    clipped_img_meta = raster_data.meta.copy()
    clipped_img_meta.update({"driver": "GTiff",
              "height": clipped_img.shape[1],
                "width": clipped_img.shape[2],
                 "transform": clipped_img_transform,
                "crs": data.crs.data})
    if export:
        with rasterio.open(out_tif, "w", **clipped_img_meta) as output:
            output.write(clipped_img)
            
    clipped = rasterio.open(clipped_img_tif)
    show((clipped, 1), cmap='terrain')
    return [clipped_img_tif, clipped_img_meta]











ds = gdal.Translate('new.tif', ds, projWin = [minx, maxy , maxx, miny])


from osgeo import gdal

ds = gdal.Open(fp)
ds = gdal.Translate('new.tif', ds, projWin = [minx, maxy , maxx, miny])
ds = gdal.Translate('new.tif', ds, projWin = [minx, maxy , maxx, miny])
data = rasterio.open('new.tif')
show((data, 1), cmap='terrain')
ds = None


from osgeo import gdal,osr
ds=gdal.Open(fp)
prj=ds.GetProjection()
print(prj)

srs=osr.SpatialReference(wkt=prj)
if srs.IsProjected:
    print (srs.GetAttrValue('projcs'))
print(srs.GetAttrValue('geogcs'))



import os
inDS = fp # input raster
outDS = ... # output raster
lon =   # lon of your flux tower
lat = ... # lat of your flux tower
ulx = lon - 24.5
uly = lat + 24.5
lrx = lon + 24.5
lry = lat - 24.5
translate = 'gdal_translate -projwin %s %s %s %s %s %s' %(ulx, uly, lrx, lry, inDS, outDS)
os.system(translate)

