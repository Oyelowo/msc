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
import pysal as ps
from shapely import speedups
from pathlib import Path
speedups.available
speedups.enable()

import lowo_utils as lut

#my_path = os.path.abspath(os.path.dirname('__file__'))
my_dir = r'E:\LIDAR_FINAL\data'


lut.create_dir(my_dir)

def create_path(sub_dir='', my_dir=my_dir):
  return lut.create_dir(Path(my_dir + sub_dir))


aoi_dir = os.path.join(my_dir, 'AOI') 
aoi_filepath =os.path.join(aoi_dir, 'fishnet_926_1sqm.shp')
bbox_raster_filepath = os.path.join(aoi_dir, 'clipped_mean_annual_rain.tif')
aoi_poly_filepath = os.path.join(aoi_dir, 'AOI_polygon.shp')
aoi_vertices_filepath= os.path.join(aoi_dir, 'aoi_vertices.shp')
buildings_filepath = os.path.join(my_dir,  'buildings', '2015', 'roof_polygons', 'buildings_2015_simplified.shp')

#rain_rasters_dir = lut.create_dir(os.path.join(my_dir,'precipitation'))
#output_clipped_raster_dir = lut.create_dir(os.path.join(my_dir, 'precipitation', 'clipped'))
#monthly_rain_shp_dir= lut.create_dir(os.path.join(my_dir, 'precipitation', 'clipped', 'to_vector'))
#centroid_filepath = lut.create_dir(os.path.join(my_dir,  'buildings', '2015', 'buildings_centroid', 'buildings_centroid.shp'))
#grid_filepath = lut.create_dir(os.path.join(my_dir,  'grid', 'grid.shp'))
#aoi_grid_clipped_shp_filepath = lut.create_dir(os.path.join(my_dir,  'grid', 'aoi_grid_clipped.shp'))


rain_rasters_dir = create_path('/precipitation')
output_clipped_raster_dir = create_path('/precipitation/clipped')
monthly_rain_shp_dir= create_path('/precipitation/clipped/to_vector')
centroid_filepath = create_path('/buildings/2015/buildings_centroid/buildings_centroid.shp')
grid_filepath = create_path('/grid/grid.shp')
aoi_grid_clipped_shp_filepath = create_path('/grid/aoi_grid_clipped.shp')





# =============================================================================
# 
# =============================================================================
aoi_crs_epsg = {'init' :'epsg:32737'}
aoi_crs_epsg_code = 32737
rain_raster_data_epsg_code = 4326

#readthe shapefile for the area of interest
aoi_shapefile = gpd.read_file(aoi_filepath)


#bbox_aoi2 = lut.get_vector_extent(aoi_shapefile)'
#bbox_aoi = lut.get_vector_extent(aoi_shapefile)
#bbox_aoi = lut.get_raster_extent(bbox_raster_filepath)
bbox_aoi = [38.19986023835, -3.2418059025499986, 38.52486023705, -3.516805901449999]
aoi_polygon =  gpd.read_file(aoi_poly_filepath)
aoi_polygon.crs = aoi_crs_epsg
#bbox_aoi = lut.get_vector_extent(aoi_polygon)



# =============================================================================
# # CLIP ALL THE MONTHLY DATA AND ALSO SUM THEM
# =============================================================================
sum_rain = 0
rain_raster = glob.glob(os.path.join(rain_rasters_dir, '*.tif'))
for i, month_file_path in enumerate(rain_raster, 1):
    print(i)
    filename = os.path.basename(month_file_path)
#    Match the file name, excluding the extension name
    if filename[:-4] == 'annual_rainfall':
        month_name = 'ann'
    else:
        month_number = re.search(r'\d+', filename).group()
        month_name = calendar.month_name[int(month_number)]
    month_abbreviation = month_name[:3]+'_rain'
    output_tif = os.path.join(output_clipped_raster_dir, month_abbreviation + '.tif')
    print(output_tif)
    lut.clip_and_export_raster(month_file_path, output_tif, bbox_aoi)
    
    month_raster = rasterio.open(output_tif).read().astype(float)
    sum_rain += month_raster


cc = sum_rain/12
# =============================================================================
# ['nearest' | 'bilinear' | 'bicubic' | 'spline16' |
#            'spline36' | 'hanning' | 'hamming' | 'hermite' | 'kaiser' |
#            'quadric' | 'catrom' | 'gaussian' | 'bessel' | 'mitchell' |
#            'sinc' | 'lanczos' | 'none' ]
# =============================================================================
show(sum_rain,cmap='RdBu',interpolation="sinc", title="Mean Annual Rainfall")
#show(month_raster,ax =ax, cmap='RdBu',interpolation="bessel", title="Mean Annual Rainfall")
# =============================================================================
# CONVERT THE RASTER FILES INTO VECTOR
# =============================================================================
monthly_rain_clipped=glob.glob(os.path.join(output_clipped_raster_dir, '*.tif'))
for i, month_file in enumerate(monthly_rain_clipped, 1):
    month_field_name = os.path.basename(month_file)[:3] + '_rain'
    output_shp = os.path.join(monthly_rain_shp_dir, month_field_name + '.shp')
    print(month_field_name)
#    month_raster = rasterio.open(month_file)
    polygonized_raster = lut.polygonize(month_file, rain_raster_data_epsg_code, aoi_crs_epsg_code)
    polygonized_raster=polygonized_raster.rename(columns={'grid_value': month_field_name})
    polygonized_raster.to_file(output_shp)
    
#    FOR TEST PURPOSE
    month_rain_data_test = gpd.read_file(output_shp)
    month_rain_data_test.plot(column=month_field_name, cmap="Blues", scheme="equal_interval", k=9, alpha=0.9)



# =============================================================================
# AOI POLYGON
# =============================================================================
# =============================================================================
vertices = gpd.read_file(aoi_vertices_filepath)
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
buildings_shp_unfiltered = gpd.read_file(buildings_filepath)

# calculate area and centroid of the buildings
buildings_shp_unfiltered['area'] = buildings_shp_unfiltered['geometry'].area
print(len(buildings_shp_unfiltered))
# filter roof areas lower than 10sqm or higher than 2000sqm
buildings_shp = buildings_shp_unfiltered.loc[(buildings_shp_unfiltered['area']>10) & (buildings_shp_unfiltered['area']<2000)]
print(len(buildings_shp))
# get the centroid of every building
buildings_shp['centroid']= buildings_shp['geometry'].centroid


buildings_centroid = buildings_shp.copy()
buildings_centroid['geometry'] = buildings_shp['centroid']
buildings_centroid = buildings_centroid.reset_index(drop=True)

#set ID for the filtered buildings. Start from one
buildings_centroid['ID'] =  buildings_centroid.index + 1
del buildings_centroid['centroid']



buildings_centroid.to_file(centroid_filepath)
#buildings_centroid.plot()

# =============================================================================
# 
# =============================================================================






# =============================================================================
# 
# # CREATE A FISHNET/GRID OF 926.1m PIXEL
# =============================================================================
#generating grid by directly providing the bounding box
grid = lut.create_grid(926.1, 926.1, shapefile=buildings_centroid)
#generating grid based on shapefile extent
#grid2 = lut.create_grid(926.1, 926.1, shapefile=aoi_shapefile)

#grid = lut.create_grid(gridHeight=926.1, gridWidth=926.1,shapefile=aoi_shapefile)
#grid.plot()


grid.to_file(grid_filepath)

# =============================================================================
# CLIP THE GRID INTO THE AOI
grid.crs = aoi_crs_epsg
aoi_grid_clipped = gpd.overlay(grid, aoi_polygon_df, how='intersection')

#reset the index of the joined data and use the index values + 1, as the ID of each grid
aoi_grid_clipped['grid_ID'] = aoi_grid_clipped.reset_index(drop=True).index + 1
aoi_grid_clipped.plot()
aoi_grid_clipped.to_file(aoi_grid_clipped_shp_filepath)

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

months_shp_filepaths = glob.glob(os.path.join(monthly_rain_shp_dir,'*.shp'))



# =============================================================================
# AGGREGATE ROOF AREAS BASED ON GRID ID
# =============================================================================



buildings_grouped = buildings_grid.groupby('grid_ID')
buildings_aggr = gpd.GeoDataFrame()
#buildings_aggr['geometry']=None
grid_ID, geom ,area, buildings_count = [], [], [], []
for key, (i, group ) in enumerate(buildings_grouped,1):
    group_geometry = group.iloc[0]['geometry']
    grid_ID.append(key)
    geom.append(group_geometry)
    area.append(group['area'].sum())
    buildings_count.append(len(group))
    print('Aggregating grid', key,  'Total Area=', group['area'].sum(),'with', len(group) ,' buildings')
buildings_aggr['grid_ID'] = grid_ID
buildings_aggr['geometry'] = geom
buildings_aggr['area_sum'] = area
buildings_aggr['buildings_count'] = buildings_count



# =============================================================================
# AGGREGATE RAINFALL DATA
# =============================================================================
#3CREATE FUNCTION TO HELP WITH AGGREGATING THE DATA
#test['geometry'] = test.centroid

def aggregate_grid_rain(new_dataframe, old_dataframe, month_field_name):
    grouped_data = old_dataframe.groupby('grid_ID')
    #buildings_aggr['geometry']=None
    grid_ID_list, geometry_list, total_grid_rain_list , roof_area_list, buildings_count_list =[], [], [], [], []
    for key, (i, group ) in enumerate(grouped_data,1):
        group_geometry = group.iloc[0]['geometry']
        grid_ID_list.append(key)
        geometry_list.append(group_geometry)
        total_grid_rain_list.append(round(group[month_field_name].mean(), 2))
        roof_area_list.append(group['area_sum'].sum())
        buildings_count_list.append(group.buildings_count.mean())
        print('Aggregating', key, month_field_name, group[month_field_name].mean())

    new_dataframe['area_sum'] = roof_area_list
    new_dataframe['geometry'] = geometry_list
    new_dataframe['grid_ID'] =grid_ID_list
    new_dataframe[month_field_name] = total_grid_rain_list
    new_dataframe['buildings_count'] = buildings_count_list
    return new_dataframe


# =============================================================================
# SPATIAL JOIN OF RAINFALL AND ROOF AREAS TO GRID DATA
# =============================================================================
import time
start_time = time.time()



months_shp_filepaths = glob.glob(os.path.join(monthly_rain_shp_dir, '*.shp'))


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
    
buildings_rain_aggr.plot(column='buildings_count' , legend=True)
print("--- %s seconds ---" % (time.time() - start_time))
# =============================================================================
# PLOT THE ROOF AREA AND RAINFALL DATA
# =============================================================================

for column in buildings_rain_aggr.columns[3:]:
    buildings_rain_aggr.plot(column=column, cmap="Blues", scheme="quantiles", k=9, alpha=0.9)
    print(column)
    

# =============================================================================
# #From the fieldwork, the average water consumption per day is 136litres.
# #The lowland and highland has very little difference, 134 to 138   
# =============================================================================
daily_Water_use_per_home = 136
monthly_wateruse_per_home = daily_Water_use_per_home * 30
buildings_rain_aggr['monthly_water_use'] = monthly_wateruse_per_home * buildings_rain_aggr['buildings_count']
buildings_rain_aggr['yearly_water_use'] = daily_Water_use_per_home * 365 * buildings_rain_aggr['buildings_count']

buildings_rain_aggr.plot('area_sum', linewidth=0.03, cmap="YlOrBr", scheme="quantiles", k=19, alpha=0.9)
buildings_rain_aggr.plot('buildings_count', linewidth=0.03, cmap="YlOrBr", scheme="quantiles", k=19, alpha=0.9)

    
# =============================================================================
#   CALCULATE MONTHLY RAINWATER HARVESTING POTENTIALS AND POTENTIAL MINUS 
#   WATER USE PER GRID TO SEE IF IT IS ENOUGH
# =============================================================================
#buildings_rain_aggr = buildings_rain_aggr.fillna(0)
roof_coefficient = 0.7
for column in buildings_rain_aggr.columns:
    if column in ['ann_rain','Apr_rain','Aug_rain','Dec_rain','Feb_rain','Jan_rain','Jul_rain','Jun_rain','Mar_rain','May_rain','Nov_rain','Oct_rain','Sep_rain']:
      print(column)
      roof_area = buildings_rain_aggr['area_sum']
      rainfall = buildings_rain_aggr[column]
      roof_harvesting_potential = (roof_area * rainfall * roof_coefficient)
      rain_pot = round(roof_harvesting_potential, 2)
      buildings_rain_aggr[column + 'POT'] = rain_pot
      if column == 'ann_rain':
        buildings_rain_aggr['ann_pot_vs_use'] = rain_pot - buildings_rain_aggr.yearly_water_use
        buildings_rain_aggr['ann_pot_vs_use_class'] = buildings_rain_aggr.ann_pot_vs_use.apply(lambda x: 'positive' if x>=0 else 'negative')
        continue
  #    1 m2 * 1 mm = 1litre. roof area is m2 and rain is in mm.
      buildings_rain_aggr[column[:3] + '_pot_vs_use'] = rain_pot - buildings_rain_aggr.monthly_water_use
      buildings_rain_aggr[column[:3] + '_pot_vs_use_class'] = buildings_rain_aggr[column[:3] + '_pot_vs_use'].apply(lambda x: 'positive' if x>=0 else 'negative')
   
     

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
# PLOTTING MAPS
# =============================================================================


def organise_colorbar(cbar, vmin, vmax, number_of_ticks=6, cbar_texts_padding=2.5, labelpad=17):
  #    organise the labels of the colorbar
    tick_padding=1.4
    interval = int((vmax-vmin)/(number_of_ticks-1))
    scale_divider = ((vmax-vmin)/interval) 
    labels=[]
    for i in range(vmin, vmax+1, interval):
      labels.append(str(i))
#    add greater than sign to the upper end of the scale
    labels[-1] = '>' + labels[-1]
    cbar.ax.set_yticklabels(labels)
    ticks = ['-'] * len(labels)
    for i, (tick, lab) in enumerate(zip(ticks , labels),0):
      cbar.ax.text(tick_padding, (i) / scale_divider, tick, ha='center', va='center', weight='bold')
      if i == len(labels) -1:
        cbar_texts_padding += 0.75
      cbar.ax.text(cbar_texts_padding, (i) / scale_divider, lab, ha='center', va='center')
#    cbar.ax.get_yaxis().labelpad = labelpad


def colorbar(ax, vmin, vmax, truncate_cbar_texts=True, cbar_title=None, number_of_ticks=6, cbar_label_pad=2, labelpad = 17):
  # add colorbar
    fig = ax.get_figure()
    sm = plt.cm.ScalarMappable(cmap=rain_potential_cmap, norm=plt.Normalize(vmin=vmin, vmax=vmax))
    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="4%", pad=0.05)
    # fake up the array of the scalar mappable....
    sm._A = []
    cbar=fig.colorbar(sm, cax = cax, fraction=0.046)
    cbar.set_label(cbar_title, rotation=270)
    cbar.ax.get_yaxis().labelpad = labelpad
    if truncate_cbar_texts:
      cbar.ax.get_yaxis().set_ticks([])
      organise_colorbar(cbar, vmin, vmax)
    


    
def find_month(column_name):
  month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
  month_abbreviation= column_name[:3]
  print(month_abbreviation)
#  month = filter(lambda x: x.startswith(month_abbreviation), month_list)
  month = [month for month in month_list if month.startswith(month_abbreviation)]
  return ' '.join(month)



def userDefinedClassifer(class_lower_limit, class_upper_limit, class_step):
  breaks = [x for x in range(class_lower_limit, class_upper_limit, class_step)]
  classifier = ps.User_Defined.make(bins=breaks)
  return classifier


def plot_map(dataFrame, column_list, scale_cmaps, vmin, vmax,truncate_cbar_texts, l_limit, h_limit, step, output_fp, main_title, cbar_title, labelpad):
  fig, axes = plt.subplots(4, 3, figsize=(12,12), sharex=True, sharey=True)
#  plt.suptitle('RAINWATER HARVESTING POTENTIAL IN TAITA')
#  vmin, vmax = dataFrame[column_list].min().min(), dataFrame[column_list].max().max()
  classified_df = dataFrame.copy()
  classified_df[column_list] = classified_df[column_list].apply(userDefinedClassifer(l_limit, h_limit, step))
  plt.suptitle(main_title, fontsize=18)
#  plt.tight_layout()
  for i, (ax, column) in enumerate(zip(axes.flatten(), column_list), 1):
    #Join the classes back to the main data.
    month = find_month(column)
#    print(month)
    if not scale_cmaps:
      vmin, vmax = dataFrame[column].min(), dataFrame[column].max()
      map_plot=dataFrame.plot(ax=ax, column=column,linewidth=0.02,scheme="equal_interval", k=9, cmap=rain_potential_cmap,  alpha=0.9)
    map_plot=classified_df.plot(ax=ax, column=column,linewidth=0.02, cmap=rain_potential_cmap,  alpha=0.9)
    print(column)
    ax.grid(b=True, which='minor', color='#D3D3D3', linestyle='-')
    ax.set_aspect('equal')
    
    # Rotate the x-axis labels so they don't overlap
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)  
    map_plot.set_facecolor("#eeeeee")
    minx,miny,maxx,maxy =  dataFrame.total_bounds
    
    # these are matplotlib.patch.Patch properties
    props = dict(boxstyle='round', facecolor='#eaeaea', alpha=0)
    map_plot.text(x=minx+1000,y=maxy-5000, s=u'N \n\u25B2 ', ha='center', fontsize=17, weight='bold', family='Courier new', rotation = 0)
    map_plot.text(x=426000,y=maxy+2000, s=month,  ha='center', fontsize=20, weight='bold', family='Courier new', bbox=props)
    plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
    colorbar(map_plot, vmin, vmax, truncate_cbar_texts, cbar_title, labelpad=labelpad)
    plt.subplots_adjust(top=0.92)
    plt.savefig(output_fp, bbox_inches='tight',dpi=300, pad_inches=0.1)






month_list = ['January', 'February', 'March', 'April', 'May', 'June', 'July',
              'August', 'September', 'October', 'November', 'December']
rain_pot_list = list(map(lambda x: x[:3] + '_rainPOT', month_list))
rain_pot_vs_use_list = list(map(lambda x: x[:3] + '_pot_vs_use', month_list))
rain_pot_vs_use_class_list = list(map(lambda x: x[:3] + '_pot_vs_use_class', month_list))
rain_list =list(map(lambda x: x[:3] + '_rain', month_list))

#Plot for monthly rainfall distribution
rain_potential_cmap = 'Blues'
monthly_main_title = "Monthly Distribution of Rainfall in Taita Region"
monthly_rain_cbar_title = "mm"
monthly_rain_output_fp = r'E:\LIDAR_FINAL\data\plots\jan_dec_rain_distribution_final4.jpg'

class_upper_limit = int(buildings_rain_aggr[rain_list].max().max())
class_lower_limit = int(buildings_rain_aggr[rain_list].min().min())

plot_map(buildings_rain_aggr, rain_list, False, None , None, False, 0, 200, 1,
         monthly_rain_output_fp, main_title= monthly_main_title,  cbar_title= monthly_rain_cbar_title, labelpad=15)



#Plot for monthly rainfall potential distribution
monthly_main_title = "Spatio-temporal Distribution of Roof RainWater Harvesting Potential in Taita"
monthly_rain_cbar_title = "100, 000 litres"
monthly_rain_output_fp = r'E:\LIDAR_FINAL\data\plots\jan_dec_rain_Potential_distribution_final_1.jpg'


rain_potential_cmap = 'RdYlBu'
plot_map(buildings_rain_aggr, rain_pot_list, True, 0 , 5, True, 0, 500000, 1000,
         monthly_rain_output_fp, main_title= monthly_main_title,  cbar_title= monthly_rain_cbar_title, labelpad=30)
buildings_rain_aggr[rain_pot_list].max()






#buildings_rain_aggr.Nov_rain
#rain_potential_cmap = 'RdBu'
#plot_map(buildings_rain_aggr, rain_list[:6],0 , 193,True, 6, 193, 1, r'E:\LIDAR_FINAL\data\plots\jan_jun_rain.jpg')
#plot_map(buildings_rain_aggr, rain_list[6:],0 , 193,False, 6, 193, 1,r'E:\LIDAR_FINAL\data\plots\jan_jun_rain.jpg')
#plot_map(buildings_rain_aggr, rain_pot_list,0 , 5, True, 0, 500000, 1000, r'E:\LIDAR_FINAL\data\plots\jan_jun_RdYlBu__free_labelpadbet.jpg')
#plot_map(buildings_rain_aggr, rain_pot_list[6:], 0, 5,True, 0, 500000, 1000, r'E:\LIDAR_FINAL\data\plots\jul_dec_RdYlBu__free_labelpadbeta.jpg')
# =============================================================================
# 
# =============================================================================
#plot_map(buildings_rain_aggr, 'ann_rain',0 , 5, True, 0, 500000, 1000, r'E:\LIDAR_FINAL\data\plots\annual_tight_potential.jpg')
#buildings_rain_aggr.plot(column='ann_rainPOT', cmap='RdBu', scheme="quantiles", k=10, alpha=0.9,edgecolor='0.6')
#plt.hist(buildings_rain_aggr['Sep_rainPOT'])


# =============================================================================
# Total Annual potential
# =============================================================================
def plot_annual(dataframe, column, map_title, legend_title,cmap, output_fp, categorical):
  minx, miny, maxx, maxy =  buildings_rain_aggr.total_bounds
  fig, ax = plt.subplots(figsize  = (9, 9))
  if categorical:
    map_plot = dataframe.plot(ax =ax,figsize=fig, column=column, categorical=True,linewidth=0.02, cmap=cmap, alpha=0.9,legend = True)
  else:
    map_plot = dataframe.plot(ax =ax,figsize=fig, column=column,scheme='quantiles', k=9,linewidth=0.02, cmap=cmap, alpha=0.9,legend = True)
  ax.grid(b=True, which='minor', color='#D3D3D3', linestyle='-')
  ax.set_aspect('equal')
  map_plot.set_facecolor("#eaeaea")
  map_plot.text(x=minx,y=maxy-6000, s=u'N \n\u25B2 ', ha='center', fontsize=37, weight='bold', family='Courier new', rotation = 0)
  ax.get_legend().set_bbox_to_anchor((1, 0.61))
  #ax.get_legend().set_bbox_to_anchor((1.43, 0.8))
  ax.get_legend().set_title(legend_title)
  ax.get_figure()
  ax.set_aspect('equal')
  plt.xlim(minx-5000, maxx+20000)
  ax.set_title(map_title, fontsize=15)
  #plt.axis('equal')
  #plt.show()
  plt.savefig(output_fp,dpi=300,  bbox_inches='tight', pad_inches=0.1)




cmap='Blues'
map_title='Distribution of Total Annual Rainfall in Taita Region'
legend_title='Rainfall(mm)'
output_fp = r'E:\LIDAR_FINAL\data\plots\total_annual_rain_final_final_4'
plot_annual(buildings_rain_aggr, 'ann_rain', map_title, legend_title,cmap, output_fp, False)


buildings_rain_aggr_ = buildings_rain_aggr.copy()
buildings_rain_aggr_['ann_rainPOT'] = round((buildings_rain_aggr['ann_rainPOT']/1000),0).astype(int)

cmap='RdYlBu'
map_title='Distribution of Annual Roof Rainwater Harvesting in Taita Region'
legend_title='RRWHP (thousand litres)'
output_fp = r'E:\LIDAR_FINAL\data\plots\total_annual_rain_potential_final_final_9'
plot_annual(buildings_rain_aggr_, 'ann_rainPOT', map_title, legend_title,cmap, output_fp, False)




cmap='Oranges'
map_title='Distribution of Areas of Roofs in Taita Region'
legend_title='Area (sqm)'
output_fp = r'E:\LIDAR_FINAL\data\plots\total_roof_areas_final_final_7.jpeg'
plot_annual(buildings_rain_aggr_, 'area_sum', map_title, legend_title,cmap, output_fp, False)



cmap='RdYlBu'
map_title='Comparison of Annual RRWH Potential and Water Use'
legend_title='RRWHP minus Water Use(litres)'
output_fp = r'E:\LIDAR_FINAL\data\plots\annual_pot_vs_use_final_final1.jpeg'
plot_annual(buildings_rain_aggr_, 'ann_pot_vs_use', map_title, legend_title,cmap, output_fp, False)


cmap='RdYlBu'
map_title='Comparison of Annual RRWH Potential and Water Use'
legend_title='RRWHP minus Water Use'
output_fp = r'E:\LIDAR_FINAL\data\plots\annual_pot_vs_use_final_final_class1.jpeg'
plot_annual(buildings_rain_aggr_, 'ann_pot_vs_use_class', map_title, legend_title,cmap, output_fp, True)

# =============================================================================
# RRWHP VS WATER USE
# =============================================================================
#Plot to see if potential meets needs, monthly
monthly_rain_output_fp = r'E:\LIDAR_FINAL\data\plots\monthly_pot_vs_use_distribution_final.jpg'
fig, axes = plt.subplots(4, 3, figsize=(10,12), sharex=True, sharey=True)
plt.suptitle('Comparison of RRWH Potential and Water Use in Taita', fontsize=18)
#  vmin, vmax = dataFrame[column_list].min().min(), dataFrame[column_list].max().max()
#  plt.tight_layout()
for i, (ax, column) in enumerate(zip(axes.flatten(), rain_pot_vs_use_class_list), 1):
  #Join the classes back to the main data.
  month = find_month(column)
#    print(month)
  legend=False
  if i == 3:
    legend=True
  map_plot=buildings_rain_aggr.plot(ax=ax, column=column,linewidth=0.02,legend=legend, cmap='RdYlBu',  alpha=0.9)
  print(column)
  ax.grid(b=True, which='minor', color='#D3D3D3', linestyle='-')
  ax.set_aspect('equal')
  
  # Rotate the x-axis labels so they don't overlap
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)  
  map_plot.set_facecolor("#eeeeee")
  minx,miny,maxx,maxy =  buildings_rain_aggr.total_bounds
  maxx += 2500
  if i==3:
    map_plot.get_legend().set_bbox_to_anchor((1.8, 0.97))
    #ax.get_legend().set_bbox_to_anchor((1.43, 0.8))
    map_plot.get_legend().set_title('RRWHP vs Water Use')
  # these are matplotlib.patch.Patch properties
  props = dict(boxstyle='round', facecolor='#eaeaea', alpha=0)
  map_plot.text(x=minx+1000,y=maxy-5000, s=u'N \n\u25B2 ', ha='center', fontsize=17, weight='bold', family='Courier new', rotation = 0)
  map_plot.text(x=426000,y=maxy+2000, s=month,  ha='center', fontsize=20, weight='bold', family='Courier new', bbox=props)
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=20)
#  plt.tight_layout()
  plt.subplots_adjust(top=0.92)
  plt.savefig(monthly_rain_output_fp, bbox_inches='tight',dpi=300, pad_inches=0.1)
# =============================================================================
# 
# =============================================================================



# =============================================================================
# TOTAL ANNUAL POTENTIAL
# =============================================================================

from matplotlib.pyplot import figure
figure(num=None, figsize=(8, 5), dpi=80, facecolor='#eaeaea', edgecolor='k')
first_letter = [first[:3] for first in rain_pot_list]
plt.bar(first_letter, buildings_rain_aggr[ rain_pot_list].sum(), color='lightblue')
plt.plot(first_letter, buildings_rain_aggr[ rain_pot_list].sum(), 'p-')
plt.ylim(0, buildings_rain_aggr[ rain_pot_list].sum().max() + 100000000)
buildings_rain_aggr[rain_list].mean()
plt.title('Total Monthly Roof Rainwater Harveting Potential, Taita')
plt.xlabel('Months')
plt.ylabel('RRHP\n(100 million litres)')
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.savefig(r'E:\LIDAR_FINAL\data\plots\bar_line_RRWP_months_series2.jpeg', dpi=300, bbox_inches='tight', pad_inches=0.1)



# =============================================================================
# PERCENTAGE OF BUILDINGS THAT RRWH CAN FULFILL THEIR NEEDS
# =============================================================================
#buildings_rain_aggr.to_file(r'E:\LIDAR_FINAL\data\aggregated\buildings_rain_aggr.shp')

percent_buildings_with_positive_RRWHP_list = []
buildings_total_count = buildings_rain_aggr['buildings_count'].sum()
for month_use_class in rain_pot_vs_use_class_list:
  gr = buildings_rain_aggr.groupby(month_use_class)
  buildings_with_net_positive_pot = (gr['buildings_count'].sum()['positive'] * 100) / buildings_total_count
  buildings_with_net_negative_pot = gr['buildings_count'].sum()['negative']
  percent_buildings_with_positive_RRWHP_list.append(buildings_with_net_positive_pot)
  print(percent_buildings_with_positive_RRWHP_list[-1])


  

from matplotlib.pyplot import figure
figure(num=None, figsize=(8, 5), dpi=80, facecolor='#eaeaea', edgecolor='k')
first_letter = [first[:3] for first in rain_pot_list]
plt.bar(first_letter, percent_buildings_with_positive_RRWHP_list, color='lightblue')
plt.plot(first_letter,percent_buildings_with_positive_RRWHP_list , 'p-')
#plt.ylim(0, buildings_rain_aggr[ rain_pot_list].sum().max() + 100000000)
buildings_rain_aggr[rain_list].mean()
plt.title('Percentage of Buildings in Taita that RRWH alone can Meet their Water Use')
plt.xlabel('Months')
plt.ylabel('Percentage of Buildings (%)')
plt.rcParams['axes.facecolor'] = '#ffffff'
plt.savefig(r'E:\LIDAR_FINAL\data\plots\bar_line_pot_vs_use_months1', dpi=300, bbox_inches='tight', pad_inches=0.1)




buildings_rain_aggr.columns
annual_use_class = 'ann_pot_vs_use_class'
annual_group = buildings_rain_aggr.groupby('ann_pot_vs_use_class')
annual_buildings_with_net_positive_pot = (annual_group['buildings_count'].sum()['positive'] * 100) / buildings_total_count

