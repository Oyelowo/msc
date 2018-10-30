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
import re
import pysal as ps

from rasterToPolygon import polygonize
import clip_raster as ras


# =============================================================================
# 
# =============================================================================
aoi_crs_epsg = {'init' :'epsg:32737'}
aoi_crs_epsg_code = 32737
rain_raster_data_epsg_code = 4326

#readthe shapefile for the area of interest
aoi_shapefile = gpd.read_file(r'E:\LIDAR_FINAL\data\AOI\fishnet_926_1sqm.shp')

#bbox_aoi2 = ras.get_vector_extent(aoi_shapefile)'
#bbox_aoi = ras.get_vector_extent(aoi_shapefile)
#bbox_aoi = ras.get_raster_extent(r'E:\LIDAR_FINAL\data\AOI\clipped_mean_annual_rain.tif')
bbox_aoi = [38.19986023835, -3.2418059025499986, 38.52486023705, -3.516805901449999]
#aoi_polygon =  gpd.read_file('E:\LIDAR_FINAL\data\AOI\AOI_polygon.shp')
#aoi_polygon.crs = aoi_crs_epsg
#bbox_aoi = ras.get_vector_extent(aoi_polygon)


# =============================================================================
# #LOAD THE FILEPATH
# =============================================================================
#mean_annual_filepath = r'E1:\LIDAR_FINAL\data\precipitation\mean_annual\CHELSA_bio_12.tif'
#mean_annual_clipped_path = r'E:\LIDAR_FINAL\data\precipitation\mean_annual\mean_annual_rain_clipped.tif'
#mean_annual_rain_raster = rasterio.open(mean_annual_filepath)
#clip the mean annual rainfall raster data
#mean_annual_rain_clipped = ras.get_clipped_raster(mean_annual_rain_raster, mean_annual_clipped_path,
#                                                  bbox_aoi, 4326)

#READ THE VALUES OF THE JUST CLIPPED RASTER
#mean_annual_rain = rasterio.open(mean_annual_clipped_path).read().astype(float)


#SPECIFY PLOT SIZE IN THE CONSOLE
plt.rcParams['figure.figsize'] = (4, 12) 


#PLOT
sns.set_style("white")
# Plot newly classified and masked raster
fig, ax = plt.subplots(figsize = (3,2))
#show((mean_annual_rain_clipped, 1),cmap='Blues', title="Mean Annual Rainfall")
#show((clipped, 1), cmap='Blues', title="Mean Annual Rainfall", contour=True)


# =============================================================================
# # CLIP ALL THE MONTHLY DATA AND ALSO SUM THEM
# =============================================================================
sum_rain = 0
monthly_rain_raster = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\*.tif')
for i, month_file_path in enumerate(monthly_rain_raster, 1):
    print(i)
    filename = os.path.basename(month_file_path)
#    Match the first number in the file name which is the month
    if filename[:-4] == 'annual_rainfall':
        month_name = 'ann'
    else:
        month_number = re.search(r'\d+', filename).group()
        month_name = calendar.month_name[int(month_number)]
    month_abbreviation = month_name[:3]+'_rain'
    output_tif = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped', month_abbreviation + '.tif')
    print(output_tif)
    ras.clip_and_export_raster(month_file_path, output_tif, bbox_aoi)
    
    month_raster = rasterio.open(output_tif).read().astype(float)
    sum_rain += month_raster


   

cc = sum_rain/12

show(sum_rain,cmap='Blues', title="Mean Annual Rainfall")

# =============================================================================
# CONVERT THE RASTER FILES INTO VECTOR
# =============================================================================
monthly_rain_clipped=glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\*.tif')
for i, month_file in enumerate(monthly_rain_clipped, 1):
    month_field_name = os.path.basename(month_file)[:3] + '_rain'
    output_shp = os.path.join('E:/LIDAR_FINAL/data/precipitation/mean_monthly/clipped/to_vector', month_field_name + '.shp')
    print(month_field_name)
#    month_raster = rasterio.open(month_file)
    polygonized_raster = ras.polygonize(month_file, rain_raster_data_epsg_code, aoi_crs_epsg_code)
    polygonized_raster=polygonized_raster.rename(columns={'grid_value': month_field_name})
    polygonized_raster.to_file(output_shp)
    
#    FOR TEST PURPOSE
    month_rain_data_test = gpd.read_file(output_shp)
    month_rain_data_test.plot(column=month_field_name, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)

 







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
# 
# =============================================================================


# =============================================================================
# 
# # CREATE A FISHNET/GRID OF 926.1m PIXEL
# =============================================================================
#generating grid by directly providing the bounding box
grid = ras.create_grid(926.1, 926.1, shapefile=buildings_centroid, convex_hull=True)

grid = gpd.read_file(r'E:\LIDAR_FINAL\data\grid\grid_clipped.shp')
#generating grid based on shapefile extent
#grid2 = ras.create_grid(926.1, 926.1, shapefile=aoi_shapefile)

#grid = ras.create_grid(gridHeight=926.1, gridWidth=926.1,shapefile=aoi_shapefile)
#grid.plot()

grid_path = r'E:\LIDAR_FINAL\data\grid\grid.shp'
grid.to_file(grid_path)
# =============================================================================
# 
# =============================================================================






# =============================================================================
# SPATIAL JOIN
# =============================================================================
grid.crs = buildings_centroid.crs = aoi_crs_epsg
buildings_grid = gpd.sjoin(grid,buildings_centroid, how="left", op='intersects') 
buildings_grid = buildings_grid.fillna(0)
del buildings_grid['index_right']

months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')

#The op options determines the type of join operation to apply. op can be set to “intersects”, “within” or 
#“contains” (these are all equivalent when joining points to polygons, but differ when 
#joining polygons to other polygons or lines).
grid.plot()



# =============================================================================
# AGGREGATE ROOF AREAS BASED ON GRID ID
# =============================================================================

buildings_grouped = buildings_grid.groupby('grid_ID')
buildings_aggr = gpd.GeoDataFrame()
#buildings_aggr['geometry']=None
for key, (i, group ) in enumerate(buildings_grouped,1):
    print(i)
    group_geometry = group.iloc[0]['geometry']
    buildings_aggr.loc[key, 'grid_ID'] = key
    buildings_aggr.loc[key,'geometry'] = group_geometry
    buildings_aggr.loc[key,'area_sum'] = group['area'].sum()
    print('Aggregating', key, group['area'].sum())


buildings_aggr.plot('area_sum', linewidth=0.03, cmap="Blues", scheme="quantiles", k=19, alpha=0.9)



# =============================================================================
# AGGREGATE RAINFALL DATA
# =============================================================================

#3CREATE FUNCTION TO HELP WITH AGGREGATING THE DATA
#test['geometry'] = test.centroid
def aggregate_grid_rain(new_dataframe, old_dataframe, month_field_name):
    grouped_data = old_dataframe.groupby('grid_ID')
    #buildings_aggr['geometry']=None
    for key, (i, group ) in enumerate(grouped_data,1):
        group_geometry = group.iloc[0]['geometry']
        new_dataframe.loc[key,'geometry'] = group_geometry
        new_dataframe.loc[key, 'grid_ID'] = key
        new_dataframe.loc[key, month_field_name] =round(group[month_field_name].mean(), 2)
        print('Aggregating', key, month_field_name, group[month_field_name].mean())
#        
        if i == len(new_dataframe):
            new_dataframe.loc[key,'area_sum'] = group['area_sum'].sum()
    return new_dataframe


# =============================================================================
# SPATIAL JOIN OF RAINFALL AND ROOF AREAS TO GRID DATA
# =============================================================================

months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')


buildings_rain_aggr = gpd.GeoDataFrame()
buildings_rain  = buildings_aggr.copy()
#del buildings_rain['area']
for i, month_filepath in enumerate(months_shp_filepaths, 1):  
    print(i)
    month_rain_data = gpd.read_file(month_filepath)
    
    buildings_rain.crs = month_rain_data.crs=  aoi_crs_epsg
    
    joined_data = gpd.sjoin(buildings_rain, month_rain_data, how='left', op='intersects')
    
#    Get field name from file name and exclude the file format
    month_field_name = os.path.basename(month_filepath)[:-4]
    print(month_field_name)
    
    buildings_rain_aggr = aggregate_grid_rain(buildings_rain_aggr, joined_data, month_field_name)
    

# =============================================================================
# PLOT THE ROOF AREA AND RAINFALL DATA
# =============================================================================

for column in buildings_rain_aggr.columns[2:]:
    buildings_rain_aggr.plot(column=column, cmap="Blues", scheme="quantiles", k=9, alpha=0.9)
    print(column)
    


# =============================================================================
#     CALCULATE MONTHLY RAINWATER HARVESTING POTENTIALS
# =============================================================================
#buildings_rain_aggr = buildings_rain_aggr.fillna(0)
for column in buildings_rain_aggr.columns:
    if column in ['geometry', 'grid_ID', 'area_sum']:
        continue
    roof_coefficient = 0.7
    roof_area = buildings_rain_aggr['area_sum']
    rainfall = buildings_rain_aggr[column]
    
#    1 m2) * 1 mm = 1litre. roof area is m2 and rain is in mm.
    roof_harvesting_potential = (roof_area * rainfall * roof_coefficient)
    buildings_rain_aggr[column + 'POT'] =round(roof_harvesting_potential, 2)
    print(buildings_rain_aggr.columns)


# =============================================================================
# PLOT ROOF HARVESTING POTENTIAL FOR ALL MONTHS
# =============================================================================
for column in buildings_rain_aggr.columns:
    if column.endswith('rainPOT'):
        ax=grid.plot()
        buildings_rain_aggr.plot(ax=ax,column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9, edgecolor='1')
  
        print(column)
#edgecolor='0.8
buildings_rain_aggr.describe()


# =============================================================================
# TODO:
# HISTOGRAM FOR MONTHLY AND ANNUAL RAINFALL
# HISTOGRAM FOR ROOF SIZE DISTRIBUTION
# HISTOGRAM FOR ROOF POTENTIAL FOR ALL MONTHS
# HISTOGRAM FOR ANNUAL ROOF POTENTIAL
#
#
#
# =============================================================================



# =============================================================================
# 
 
 import pandas as pd
 import numpy as np
 import shapely
 import matplotlib.pyplot as plt
 from mpl_toolkits.axes_grid1 import make_axes_locatable
 
 
 
 gdf = buildings_rain_aggr
 ## the plotting
 #buildings_rain_aggr.plot(column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9, edgecolor='1')
        
 vmin, vmax = buildings_rain_aggr['ann_rainPOT'].min(), buildings_rain_aggr['ann_rainPOT'].max()
 
 ax = gdf.plot(column='ann_rainPOT', colormap='RdBu',  scheme="quantiles", k=10, alpha=0.9, edgecolor='1')

 
 
 
 import numpy as np
 import matplotlib.pyplot as plt
 import matplotlib.colors
 
 
def colorbar(ax):
    vmin, vmax = buildings_rain_aggr['ann_rainPOT'].min(), buildings_rain_aggr['ann_rainPOT'].max()

#    ax = gdf.plot(column='ann_rainPOT', colormap='RdBu',  scheme="quantiles", k=10, alpha=0.9, edgecolor='1')
  # add colorbar
    fig = ax.get_figure()
    sm = plt.cm.ScalarMappable(cmap='RdBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cbar=fig.colorbar(sm, cax=cax)
    cbar.set_label('Litres')
 



def plot_map():
  fig, axs = plt.subplots(3, 2, figsize=(12,12), sharex=True, sharey=True)
  for ax in axs.flatten():
    map_plot=buildings_rain_aggr.plot(ax=ax, column=column, cmap="RdBu", scheme="quantiles", k=10, alpha=0.9,edgecolor='0.6')
    ax.grid()
  # Figure title
    fig.suptitle('Seasonal temperature observations - Helsinki Malmi airport')
  #    plt.title('linear')
    # Rotate the x-axis labels so they don't overlap
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)  
    map_plot.set_facecolor("#eeeeee")
    minx,miny,maxx,maxy =  buildings_rain_aggr.total_bounds
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='#eaeaea', alpha=0)
    map_plot.text(x=minx+1000,y=maxy-5000, s=u'N \n\u25B2 ', ha='center', fontsize=20, weight='bold', family='Courier new', rotation = 0)
    map_plot.text(x=425000,y=maxy-2000, s='lowo',  ha='center', fontsize=20, weight='bold', family='Courier new', bbox=props)
    #ax11.text(datetime(2013, 2, 15), -25, 'Winter')
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
    colorbar(map_plot)
  #    plt.tight_layout()
    plt.savefig(r'C:\Users\oyeda\Desktop\msc\test.jpg')

plot_map()

   