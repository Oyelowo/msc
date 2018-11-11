import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
from rasterio.mask import mask
from shapely.geometry import box
import geopandas as gpd
from fiona.crs import from_epsg
import pycrs
import matplotlib.pyplot as plt
#from osgeo import gdal
import utm



fp= r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'
out_tif=r'E:\LIDAR_FINAL\data\precipitation\mean_annual\test_lowo.tif'


grid_path = r'E:\LIDAR_FINAL\data\grid.shp'
fishnet = r'E:\LIDAR_FINAL\data\2015\fishnet\fishnet_925_1sqm.shp'
centroid = r'E:\LIDAR_FINAL\data\2015\buildings\buildings_2015_centroid.shp'
centroid = gpd.read_file(centroid)
fishnet = gpd.read_file(fishnet)
print(fishnet.crs)
data = rasterio.open(fp)

grid= gpd.read_file(r'E:\LIDAR_FINAL\data\2015\final\buildings_rainfall_grid.shp')
grid2= gpd.read_file(r'E:\LIDAR_FINAL\data\2015\final\rainfall_grid.shp')
grid3= gpd.read_file(r'E:\LIDAR_FINAL\data\2015\final\rainfall_fishnet.shp')

buildings = gpd.read_file(r'E:\LIDAR_FINAL\data\2015\buildings\buildings_2015_simplified.shp')
buildings['area'] = buildings['geometry'].area

buildings = buildings.loc[(buildings['area'] > 10) & (buildings['area'] < 5000)]

buildings['geomtry'] = buildings['geometry'].centroid

buildings.plot()
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = r"E:\LIDAR_FINAL\data\2015\maps\static_map.png"
plt.savefig(outfp, dpi=300)

aaaa = gpd.sjoin(buildings, polys, op='within') 

# Get the CRS of the grid
gridCRS = fishnet.crs
print(centroid.crs)

# Reproject geometries using the crs of travel time grid
fishnet['geometry'] = fishnet['geometry'].to_crs(crs=gridCRS)

aaa = gpd.sjoin(centroid, fishnet, op='within')
pointInPoly = gpd.sjoin(points, polys, op='within') 

grid['area_clean'] = grid.loc[grid['area']>5, 'area']

grid['RWHP'] = grid['DN'] * grid['area'] * 0.7 
# Visualize the travel times into 9 classes using "Quantiles" classification scheme
# Add also a little bit of transparency with `alpha` parameter
# (ranges from 0 to 1 where 0 is fully transparent and 1 has no transparency)
my_map = grid.plot(column="RWHP", linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)

plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = r"E:\LIDAR_FINAL\data\2015\maps\static_map.png"
plt.savefig(outfp, dpi=300)



# Add roads on top of the grid
# (use ax parameter to define the map on top of which the second items are plotted)
#roads.plot(ax=my_map, color="grey", linewidth=1.5)

# Add metro on top of the previous map
#metro.plot(ax=my_map, color="red", linewidth=2.5)

# Remove the empty white-space around the axes
plt.tight_layout()

# Save the figure as png file with resolution of 300 dpi
outfp = r"/home/geo/data/static_map.png"
plt.savefig(outfp, dpi=300)



















import os
from osgeo import gdal, ogr
from shapely.geometry import shape
import geopandas as gpd

ras  = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rainfall_clipped.tif'




poly = polygonize(ras, data.crs, fishnet.crs)

fishnet.crs = gpd_polygonized_raster.crs
fishnet.crs
join = gpd.sjoin(fishnet, gpd_polygonized_raster, how="inner")


join.plot(column='raster_val', linewidth=0.03, cmap="Reds", scheme="quantiles", k=9, alpha=0.9)

join.to_file(r'E:\LIDAR_FINAL\data\test.shp')



help(gpd.sjoin)
cities_with_country = gpd.sjoin(fishnet, gpd_polygonized_raster, how="inner", op='intersects')

# show((data, 1), cmap='terrain')
# plt.show()



