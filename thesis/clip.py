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



fp= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\test_lowo.tif'

# show((data, 1), cmap='terrain')
# plt.show()
grid_path = r'E:\LIDAR_FINAL\data\2015\fishnet\fishnet_925_1sqm.shp'


data = rasterio.open(fp)
fishnet = gpd.read_file(grid_path)
# print(fishnet.bounds)
# print(fishnet.total_bounds)
# fishnet.plot()
# plt.show()

bbox = fishnet.total_bounds
print(bbox)
# print(fishnet.crs)
# print(from_epsg(32737))

# minx, miny = 24.60, 60.00
# maxx, maxy = 25.22, 60.35
# bbox = box(minx, miny, maxx, maxy)
geo = gpd.GeoDataFrame({'geometry': bbox}, crs=fishnet.crs)
# geo.plot()
# plt.show()
minx, miny, maxx, maxy = bbox

# min, max=bbox[0:2], bbox[2:4]
# print(minx)
min = utm.to_latlon(minx,miny, 37, northern=False)
max = utm.to_latlon(maxx,maxy, 37, northern=False)

# unpack the values from the tuple
bbox_lat_lon = [*min, *max]
print(bbox_lat_lon)
# ds = gdal.Open(fp)
# ds = gdal.Translate('new.tif', ds, projWin = bbox)
# ds = None

# geo = geo.to_crs(crs=data.crs)

# def getFeatures(gdf):
#     """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
#     import json
#     return [json.loads(gdf.to_json())['features'][0]['geometry']]

# coords = getFeatures(geo)







# print(coords)

# out_img, out_transform = mask(raster=data, shapes=coords, crop=True)

# out_meta = data.meta.copy()

# print(out_meta)

# epsg_code = int(data.crs.data['init'][5:])

# print(epsg_code)

# out_meta.update({"driver": "GTiff",
#                      "height": out_img.shape[1],
#                      "width": out_img.shape[2],
#                      "transform": out_transform,
#                      "crs": pycrs.parser.from_epsg_code(epsg_code).to_proj4()})

# with rasterio.open(out_tif, "w", **out_meta) as dest:dest.write(out_img)

# clipped = rasterio.open(out_tif)

# show((clipped, 5), cmap='terrain')