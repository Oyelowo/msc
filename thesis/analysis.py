# =============================================================================
import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import rasterio
from rasterio.plot import show
from rasterio.plot import show_hist
import seaborn as sns
import glob
import os
import calendar
import re
from mpl_toolkits.axes_grid1 import make_axes_locatable
from shapely import speedups
speedups.available
speedups.enable()

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
aoi_polygon =  gpd.read_file('E:\LIDAR_FINAL\data\AOI\AOI_polygon.shp')
aoi_polygon.crs = aoi_crs_epsg
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
# AOI POLYGON
# =============================================================================
# =============================================================================
vertices = gpd.read_file(r'E:\LIDAR_FINAL\data\AOI\aoi_vertices.shp')
vertices.plot()
aoi_vertices_list = [p.xy for p in vertices.geometry]
aoi_polygon = Polygon([[points.x, points.y] for points in vertices.geometry])
aoi_polygon_df = gpd.GeoDataFrame(data=[aoi_polygon],  columns=['geometry'])
aoi_polygon_df.crs= aoi_crs_epsg
aoi_polygon_df.plot()
print(aoi_polygon)
# =============================================================================




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
grid = ras.create_grid(926.1, 926.1, shapefile=buildings_centroid)
#generating grid based on shapefile extent
#grid2 = ras.create_grid(926.1, 926.1, shapefile=aoi_shapefile)

#grid = ras.create_grid(gridHeight=926.1, gridWidth=926.1,shapefile=aoi_shapefile)
#grid.plot()

grid_path = r'E:\LIDAR_FINAL\data\grid\grid.shp'
grid.to_file(grid_path)

# =============================================================================
# CLIP THE GRID INTO THE AOI
grid.crs = aoi_crs_epsg
aoi_grid_clipped = gpd.overlay(grid, aoi_polygon_df, how='intersection')

#reset the index of the joined data and use the index values + 1, as the ID of each grid
aoi_grid_clipped['grid_ID'] = aoi_grid_clipped.reset_index(drop=True).index + 1
aoi_grid_clipped.plot()
aoi_grid_clipped.to_file(r'E:\LIDAR_FINAL\data\grid\aoi_grid_clipped.shp')

#grid = gpd.read_file(r'E:\LIDAR_FINAL\data\grid\grid_clipped.shp'
# =============================================================================
# 
# =============================================================================





# =============================================================================
# SPATIAL JOIN
# =============================================================================
grid.crs = buildings_centroid.crs = aoi_crs_epsg
#join the grid with the buildings, to get the areas per grid
buildings_grid = gpd.sjoin(aoi_grid_clipped,buildings_centroid, how="left", op='intersects') 

#some grids might be without buildings and will be nan values. Replace those with 0
buildings_grid = buildings_grid.fillna(0)

#delete the index_right column to avoid issues later
del buildings_grid['index_right']

months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')



# =============================================================================
# AGGREGATE ROOF AREAS BASED ON GRID ID
# =============================================================================



buildings_grouped = buildings_grid.groupby('grid_ID')
buildings_aggr = gpd.GeoDataFrame()
#buildings_aggr['geometry']=None
grid_ID, geom ,area = [], [], []
for key, (i, group ) in enumerate(buildings_grouped,1):
    group_geometry = group.iloc[0]['geometry']
    grid_ID.append(key)
    geom.append(group_geometry)
    area.append(group['area'].sum())
    print('Aggregating grid', key,  'Total Area=', group['area'].sum())
buildings_aggr['grid_ID'] = grid_ID
buildings_aggr['geometry'] = geom
buildings_aggr['area_sum'] = area
    

buildings_aggr.plot('area_sum', linewidth=0.03, cmap="Blues", scheme="quantiles", k=19, alpha=0.9)



# =============================================================================
# AGGREGATE RAINFALL DATA
# =============================================================================
#3CREATE FUNCTION TO HELP WITH AGGREGATING THE DATA
#test['geometry'] = test.centroid

def aggregate_grid_rain(new_dataframe, old_dataframe, month_field_name):
    grouped_data = old_dataframe.groupby('grid_ID')
    #buildings_aggr['geometry']=None
    grid_ID_list, geometry_list, total_grid_rain_list , roof_area_list=[], [], [], []
    for key, (i, group ) in enumerate(grouped_data,1):
        group_geometry = group.iloc[0]['geometry']
        grid_ID_list.append(key)
        geometry_list.append(group_geometry)
        total_grid_rain_list.append(round(group[month_field_name].mean(), 2))
        roof_area_list.append(group['area_sum'].sum())
        print('Aggregating', key, month_field_name, group[month_field_name].mean())

    new_dataframe['area_sum'] = roof_area_list
    new_dataframe['geometry'] = geometry_list
    new_dataframe['grid_ID'] =grid_ID_list
    new_dataframe[month_field_name] = total_grid_rain_list
    return new_dataframe


# =============================================================================
# SPATIAL JOIN OF RAINFALL AND ROOF AREAS TO GRID DATA
# =============================================================================
import time
start_time = time.time()



months_shp_filepaths = glob.glob(r'E:\LIDAR_FINAL\data\precipitation\mean_monthly\clipped\to_vector\*.shp')


buildings_rain_aggr = gpd.GeoDataFrame()
#del buildings_rain['area']
for i, month_filepath in enumerate(months_shp_filepaths, 1):  
    print(i)
    month_rain_data = gpd.read_file(month_filepath)
    
    buildings_aggr.crs = month_rain_data.crs=  aoi_crs_epsg
    
    joined_data = gpd.sjoin(buildings_aggr, month_rain_data, how='left', op='intersects')
    
#    Get field name from file name and exclude the file format
    month_field_name = os.path.basename(month_filepath)[:-4]
    print(month_field_name)
    
    buildings_rain_aggr = aggregate_grid_rain(buildings_rain_aggr, joined_data, month_field_name)
    

print("--- %s seconds ---" % (time.time() - start_time))
# =============================================================================
# PLOT THE ROOF AREA AND RAINFALL DATA
# =============================================================================

for column in buildings_rain_aggr.columns[3:]:
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
  
 
 
def colorbar(ax, vmin, vmax):
  # add colorbar
    fig = ax.get_figure()
    sm = plt.cm.ScalarMappable(cmap='RdBu', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    # fake up the array of the scalar mappable. Urgh...
    sm._A = []
    cbar=fig.colorbar(sm, cax=cax)
    cbar.set_label('100,000 litres')
    cbar.ax.set_title('RWHP')
import pysal as ps

def find_month(column_name):
  month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
  month_abbreviation= column_name[:3]
  print(month_abbreviation)
#  month = filter(lambda x: x.startswith(month_abbreviation), month_list)
  month = [month for month in month_list if month.startswith(month_abbreviation)]
  return ' '.join(month)


month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
rain_pot_list = list(map(lambda x: x[:3] + '_rainPOT', month_list))
rain_list =list(map(lambda x: x[:3] + '_rain', month_list))


#classifier = ps.Natural_Breaks.make(k=150)
#dataFrame[rain_pot_list] = dataFrame[rain_pot_list].apply(classifier)
#
#mode_classif.columns = [ rain_pot_list + '_class']
  
def plot_map(dataFrame,  column_list):
  fig, axes = plt.subplots(3, 2, figsize=(12,12), sharex=True, sharey=True)
  classied_df = dataFrame.copy()
  classifier = ps.Natural_Breaks.make(k=15)
  classied_df[rain_pot_list] = classied_df[rain_pot_list].apply(classifier)
  for ax, column in zip(axes.flatten(), column_list):
    #Join the classes back to the main data.
    month = find_month(column)
    print(month)
#    vmin, vmax = dataFrame[column].min(), dataFrame[column].max()
    vmin, vmax = dataFrame[rain_pot_list].min().min(), dataFrame[rain_pot_list].max().max()
    map_plot=classied_df.plot(ax=ax, column=column , cmap='RdBu')
    ax.grid()
    fig.suptitle('RAINWATER HARVESTING POTENTIAL IN TAITA')
    ax.set_aspect('equal')
    
    # Rotate the x-axis labels so they don't overlap
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)  
    map_plot.set_facecolor("#eeeeee")
    minx,miny,maxx,maxy =  dataFrame.total_bounds
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='#eaeaea', alpha=0)
    map_plot.text(x=minx+1000,y=maxy-5000, s=u'N \n\u25B2 ', ha='center', fontsize=20, weight='bold', family='Courier new', rotation = 0)
    map_plot.text(x=426000,y=maxy+2100, s=month,  ha='center', fontsize=20, weight='bold', family='Courier new', bbox=props)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
    colorbar(map_plot, vmin/1000, vmax/1000)
  #    plt.tight_layout()
    plt.savefig(r'C:\Users\oyeda\Desktop\msc\test.jpg', bbox_inches='tight', pad_inches=0.1)


#pot_list = [pot for pot in buildings_rain_aggr.columns if pot.endswith('rainPOT') and pot != 'ann_rainPOT']


#plot_map(buildings_rain_aggr, rain_list)
plot_map(buildings_rain_aggr, rain_pot_list)
# =============================================================================
# 
# =============================================================================






    #Rename the columns of our classified columns.

# =============================================================================
# 
# 
# aa= buildings_rain_aggr.copy()
# aa[rain_pot_list].min(axis=0).min()
# aa[rain_pot_list].max(axis=0).max()
# #aa=aa.loc[aa['Sep_rainPOT']>0]
# classifier = ps.Natural_Breaks.make(k=100)
# aa[rain_pot_list] = aa[rain_pot_list].apply(classifier)
# aa.plot(column='Jun_rainPOT', cmap='RdBu', scheme='equal_interval', k=20)
# aa.plot(column='Apr_rainPOT', cmap='RdBu',scheme='equal_interval', k=20)
# aa.plot(column='Nov_rainPOT', cmap='RdBu',scheme='equal_interval', k=20)
# aa.plot(column='Sep_rainPOT', cmap='RdBu',scheme='equal_interval', k=20)
# =============================================================================
# =============================================================================
# 
# merged_metro['label_' + tt_col ] = mode_classif
#         
# 
# 
# 
# my_map = merged_metro.plot(column=tt_col, linewidth=0.02, legend=True, cmap="RdYlGn", scheme=class_type, k=n_classes, alpha=0.9)
# # =============================================================================
# #  
# =============================================================================
# 
# 
# if class_type == "Natural_Breaks":
#         classifier = ps.Natural_Breaks.make(k=n_classes)
#     elif class_type == "Equal_Interval":
#         classifier = ps.Equal_Interval.make(k=n_classes)
#     elif class_type == "Box_Plot":
#         classifier = ps.Box_Plot.make(hinge)
#     elif class_type == "Fisher_Jenks":
#         classifier = ps.Fisher_Jenks.make(k=n_classes)
# #                elif class_type == "Fisher_Jenks_Sampled":
# #                    classifier = ps.Fisher_Jenks_Sampled.make(k=n_classes, pct=0.1)
#     elif class_type == "HeadTail_Breaks":
#         classifier = ps.HeadTail_Breaks.make(k=n_classes)
#     elif class_type == "Jenks_Caspall":
#         classifier = ps.Jenks_Caspall.make(k=n_classes)
#     elif class_type == "Jenks_Caspall_Forced":
#         classifier = ps.Jenks_Caspall_Forced.make(k=n_classes)
#     elif class_type == "Quantiles":
#         classifier = ps.Quantiles.make(k=n_classes)
#     elif class_type == "Percentiles":
#         classifier = ps.Percentiles.make(pct_classes)
#     elif class_type == "Std_Mean":
#         classifier = ps.Std_Mean.make(multiples)
#     mode_classif = merged_metro[[tt_col]].apply(classifier)
#    
#     
#     #Rename the columns of our classified columns.
#     mode_classif.columns = [tt_col+"_ud"]
#     
#     
#     #Join the classes back to the main data.
#     merged_metro = merged_metro.join(mode_classif)
#     
#         
#     merged_metro['label_' + tt_col ] = mode_classif
#         
#     
# 
# elif classification == "User_Defined":
#      #Next, we want to classify the travel times with 5 minute intervals until 200 minutes.
# 
#     #Let’s create a list of values where minumum value is 5, maximum value is 200 and step is 5.
#     breaks = [x for x in range(class_lower_limit, class_upper_limit, class_step)]
#     #Now we can create a pysal User_Defined classifier and classify our travel time values.
# 
#     classifier = ps.User_Defined.make(bins=breaks)
# 
#     #walk_classif = data[['walk_t']].apply(classifier)
#     
#     mode_classif = merged_metro[[tt_col]].apply(classifier)
#     
#     
#     #Rename the columns of our classified columns.
#     mode_classif.columns = [tt_col+"_ud"]
#     #walk_classif.columns = ['walk_t_ud']
#     
#     #Join the classes back to the main data.
#     merged_metro = merged_metro.join(mode_classif)
# 
# 
# 
# my_map = merged_metro.plot(column=tt_col, linewidth=0.02, legend=True, cmap="RdYlGn", scheme=class_type, k=n_classes, alpha=0.9)
#                         
# =============================================================================
