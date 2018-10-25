import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import matplotlib.pyplot as plt



fp= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\test_lowo.tif'

# show((data, 1), cmap='terrain')
# plt.show()
grid_path = r'E:\LIDAR_FINAL\data\2015\fishnet\fishnet_925_1sqm.shp'


data = rasterio.open(fp)
fishnet = gpd.read_file(grid_path)
fishnet.plot()
plt.show()


minx, miny = 24.60, 60.00
maxx, maxy = 25.22, 60.35
bbox = box(minx, miny, maxx, maxy)
geo = gpd.GeoDataFrame({'geometry': bbox}, index=[0], crs=from_epsg(4326))

geo = geo.to_crs(crs=data.crs.data)

def getFeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

coords = getFeatures(geo)

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