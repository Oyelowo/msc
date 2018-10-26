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
from gdalconst import GA_ReadOnly


data = gdal.Open(clipped_path, GA_ReadOnly)
geoTransform = data.GetGeoTransform()
minx = geoTransform[0]
maxy = geoTransform[3]
maxx = minx + geoTransform[1] * data.RasterXSize
miny = maxy + geoTransform[5] * data.RasterYSize
print([minx, miny, maxx, maxy])
data = None



   kk = list(fishnet.total_bounds)
    minx,miny, maxy, maxy = kk[0], kk[1], kk[2], kk[3]
    minx,miny = utm.to_latlon(minx,miny, 37, northern=True)
    maxx,maxy = utm.to_latlon(maxx,maxy, 37, northern=True)

#411326.9602166185,447444.86021661846,9611034.927098723,9641596.227098722

from osgeo import gdal

ds = gdal.Open(fp)
ds = gdal.Translate(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif', ds, projWin = [minx, maxy , maxx, miny])
ds = gdal.Translate(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\new.tif', ds, projWin = [minx, maxy , maxx, miny])
data = rasterio.open(r'E:\LIDAR_FINAL\data\precipitation\mean_annual\newnew.tif')
show((data, 1), cmap='terrain')
ds = None


arr = [minx, miny, maxx, maxy]
arr
box(*arr)
bbox = box(minx, miny, maxx, maxy)

fishnet.total_bounds




geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

geo = geo.to_crs(crs=data.crs.data)
data.crs
fishnet.crs

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(geo)
print(coords)

out_img, out_transform = mask(raster=data, shapes=coords, crop=True)
out_meta = data.meta.copy()

epsg_code = int(data.crs.data['init'][5:])

pycrs.parser.from_epsg_code(epsg_code)
out_meta.update({"driver": "GTiff",
              "height": out_img.shape[1],
                "width": out_img.shape[2],
                 "transform": out_transform,
                "crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})
    
    
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\testtest.tif'
with rasterio.open(out_tif, "w", **out_meta) as dest:
       dest.write(out_img)

clipped = rasterio.open(out_tif)

show((clipped, 1), cmap='terrain')











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

