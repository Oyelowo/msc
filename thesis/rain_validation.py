# =============================================================================
# Validate rainfall data from CHELSA
# =============================================================================
        
import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
import geopandas as gpd
from datetime import datetime
from shapely.geometry import Point
from scipy.stats import linregress
import seaborn as sns
from scipy import stats
from pathlib import Path
import clip_raster as ras

my_dir = r'E:\LIDAR_FINAL\data'


ras.create_dir(my_dir)

def create_path(sub_dir='', my_dir=my_dir):
  return ras.create_dir(Path(my_dir + sub_dir))

rain_dir = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain"
rain_dir_all = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain\Precipitation\*.XLSX"
buildings_rain_aggr = gpd.read_file(r'E:\LIDAR_FINAL\data\aggregated\buildings_rain_aggr.shp')
stations_filepath = r'E:\LIDAR_FINAL\data\rainfall_data_field\stations_locations\stations.csv'

rain_fp_list = glob.glob(rain_dir_all)

def aggregateDataByMonth(data):
  data.index = pd.to_datetime(data['Date'])
  data = data.groupby(pd.Grouper(freq="M"))
  df =pd.DataFrame()
  df['Date'] =None
  for key, group in data:
    df.loc[key, 'Date'] = key
    df.loc[key, 'rain_mm'] = group['Rain_(mm)'].sum()
#    print(key,'\n \n', group)
  return df.reset_index(drop=True)

#merged_df=pd.DataFrame(columns=['Date', 'rain_mm', 'station'])
#merged_df['Date']=None
all_data = pd.DataFrame(columns=['Date', 'rain_mm', 'station'])
for i, rain_data in enumerate(rain_fp_list[2:]):
  data = pd.read_excel(rain_data)
  header_index = data.loc[data['ID']=='Date'].index.values[0]
  data = pd.read_excel(rain_data, skiprows=header_index+1, parse_dates=["Date"])
  data = data[['Date', 'Rain_(mm)']]
  agg_data = aggregateDataByMonth(data)
  station_name = rain_data.split('\\')[-1].split('.')[0]
  agg_data['station'] = station_name.split('_Ar')[0]
  all_data = all_data.append(agg_data)
#  merged_df = pd.merge(merged_df, agg_data,  on='Date', how='outer')
  print(agg_data.head(5))
  print(i)



stations_names_list = all_data['station'].unique().tolist()

#stations_list.remove('Mwatate_Ar112509')
plt.rcParams.update({'font.size': 22})
min_temp, max_temp = all_data.rain_mm.min()-20, all_data.rain_mm.max() + 20
fig, axes = plt.subplots(3, 2, figsize=(14,14), sharex=True)
for i, (ax, station) in enumerate(zip(axes.flatten(), stations_names_list), 1):
  sub_data = all_data.loc[all_data['station']==station]
  ax.plot(sub_data.Date, sub_data.rain_mm, lw = 1.5, c='blue')
  # Figure title
  fig.suptitle('Measured Rainfall in Taita Region')
  if station == 'Taita_RS': 
    station = "Taita Research Station" 
  else:
    station += ' Weather Station'
  ax.set_title(station, fontsize=20)
  ax.grid(color='grey', linestyle='-', linewidth=1, alpha=0.4)
  ax.set_ylim(min_temp, max_temp)
#  ax.set_facecolor('white')
  ax.tick_params(axis='both', which='major', labelsize=15)
  # Axis labels
  if i in [1, 3, 5]:
    ax.set_ylabel('Rainfall [mm]', fontsize=20)
  if i in [5, 6]:
    ax.set_xlabel('Date', fontsize=20)
plt.tight_layout()
plt.subplots_adjust(top=0.92)
plt.savefig(r'E:\LIDAR_FINAL\data\plots\stations_rain_timeseries.jpeg',  bbox_inches='tight', pad_inches=0.1)



         
monthly_agg_data = pd.DataFrame(columns=["station", "month", "rain_mm"])
i=0
for station in stations_names_list:
  sub_data = all_data.loc[all_data['station']==station]
  sub_data["month"] = sub_data.Date.astype(str).str.slice(5,7)
  grouped = sub_data.groupby('month')
  for key, group in grouped:
    i+=1
    monthly_agg_data.loc[i, "station"] =station
    monthly_agg_data.loc[i, "month"] = key
    monthly_agg_data.loc[i, "rain_mm"] = group.rain_mm.mean()
    print(monthly_agg_data.station)

         
import calendar
monthly_agg_data['month_name'] = monthly_agg_data['month'].astype(int).apply(lambda x: calendar.month_abbr[x])
         
min_temp, max_temp = monthly_agg_data.rain_mm.min()-20, monthly_agg_data.rain_mm.max() + 30
fig, axes = plt.subplots(3, 2, figsize=(10,12), sharex=True, sharey=True)
#  plt.suptitle('RAINWATER HARVESTING POTENTIAL IN TAITA')
#  vmin, vmax = dataFrame[column_list].min().min(), dataFrame[column_list].max().max()
for i, (ax, station) in enumerate(zip(axes.flatten(), stations_names_list), 1):
  sub_data = monthly_agg_data.loc[monthly_agg_data['station']==station]
  ax.plot(sub_data.month_name, sub_data.rain_mm, lw = 1.5)
  # Figure title
  fig.suptitle('Seasonal Rainfall observations - Taita-Taveta')
  ax.text(2, max_temp-20, station)
  ax.grid()
  ax.set_ylim(min_temp, max_temp)
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
  # Axis labels
  if i== 1 or i==3 or i==5:
    ax.set_ylabel('Rainfall [mm]')
  if i== 5 or i==6:
    ax.set_xlabel('Date')

         



stations = pd.read_csv(stations_filepath)
stations = gpd.GeoDataFrame(stations)
stations = stations.iloc[:,:5]
stations_list = [Point(x, y) for x,y in zip(stations.x, stations.y)]
stations_list[0]
stations['geometry'] = stations_list
stations.plot()
print(stations.crs)
stations.crs = {'init' :'epsg:32737'}



def plot_station(dataframe, column, map_title, legend_title,cmap, output_fp):
  minx, miny, maxx, maxy =  buildings_rain_aggr.total_bounds
  fig, ax = plt.subplots(figsize  = (7, 7))
  buildings_rain_aggr.plot(ax=ax, column='ann_rain', cmap='Blues', alpha=0.8)
  map_plot = dataframe.plot(ax =ax,figsize=fig, column=column, s=100, alpha=1, legend = True)
  ax.grid(b=True, which='minor', color='#D3D3D3', linestyle='-')
  ax.set_aspect('equal')
#  map_plot.set_facecolor("#ffffff")
  map_plot.text(x=minx+3000,y=maxy-4000, s=u'N \n\u25B2 ', ha='center', fontsize=37, weight='bold', family='Courier new', rotation = 0)
  ax.get_legend().set_bbox_to_anchor((1, 0.44))
#  ax.get_legend().set_bbox_to_anchor((1.23, 0.9))
  ax.get_legend().set_title(legend_title)
  ax.get_figure()
  ax.set_aspect('equal')
  plt.xlim(minx-1000, maxx+1000)
  ax.set_title(map_title, fontsize=15)
  #plt.axis('equal')
  #plt.show()
  plt.savefig(output_fp,  bbox_inches='tight', pad_inches=0.1)



cmap='Blues'
map_title=' in Taita Region'
legend_title='Weather Stations'
output_fp = r'E:\LIDAR_FINAL\data\plots\weather_stations_3'
plot_station(stations, 'Location', map_title, legend_title,cmap, output_fp)




fig, ax = plt.subplots(figsize  = (9, 5))
buildings_rain_aggr.plot(ax=ax)
stations.plot(ax=ax, c='red', column='Location', legend=True)
plt.xlim(400000, 480000)
plt.ylim(9610000, 9645000)

buildings_rain_aggr.crs = stations.crs
len(stations)
ground_stations_rain_model = gpd.sjoin(stations, buildings_rain_aggr, how='inner', op='intersects')
ground_stations_rain_model.Location

stations_abbr = [station.split(',')[0].split(' ')[0] for station in ground_stations_rain_model.Location]
wundayi_index = stations_abbr.index('Wundanyi')
stations_abbr[wundayi_index] = 'Taita_RS'

ground_stations_rain_model['station'] = stations_abbr

def get_column_names_lists(ending, except_this):
  return [month for month in ground_stations_rain_model.columns if month.endswith(ending) and not month.startswith(except_this)]
months_rain = get_column_names_lists('rain', 'ann')
months_rain_pot = get_column_names_lists('PO', "ann")

stations_rain_model_df = pd.DataFrame(columns=[ 'station', 'month', 'model_rain_mm','rain_pot'])
for i, row in ground_stations_rain_model.iterrows():
  monthly_rain = row[months_rain]
  months_list = [month[0:3] for month in monthly_rain.index]
  monthly_rain_pot = row[months_rain_pot].tolist()
  month, rain, rain_pot = monthly_rain.index, monthly_rain, monthly_rain_pot
  data = {'station': row.station, 'month': months_list, 'model_rain_mm': monthly_rain, 'rain_pot':rain_pot, 'x':row.x,'y':row.y,'z':row.z}
  each_station = pd.DataFrame(data)
  stations_rain_model_df = pd.concat([each_station, stations_rain_model_df], sort=False)





stations_rain_model_df.columns
monthly_agg_data.columns
joined = pd.merge(stations_rain_model_df, monthly_agg_data, left_on=['station','month'], right_on=['station', 'month_name'])
joined.columns
joined['rain_err'] = joined['rain_mm']- joined['model_rain_mm']
import numpy as np

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

rmse_val = rmse(joined.model_rain_mm, joined.rain_mm)
print("rms error is: " + str(rmse_val))



rain_stat = linregress(joined.model_rain_mm.tolist(), joined.rain_mm.tolist())
r2 = rain_stat.rvalue**2
measured_rain, modelled_rain = joined.rain_mm.tolist() , joined.model_rain_mm.tolist()




def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
print(r2(measured_rain, modelled_rain))
x=np.array(measured_rain) 
y=np.array(modelled_rain)

x = pd.Series(measured_rain, name="measured rain")
y = pd.Series(modelled_rain, name="modelled rain")
ax = sns.jointplot(x, y, kind="reg", stat_func=r2, logx=True, truncate=True, space=0.1)
plt.title('YOUR TITLE HERE')







sns.set(color_codes=True)
discontinued_station = 'Mwatate'
if discontinued_station in stations_names_list:
  stations_names_list.remove(discontinued_station)
  
min_rain, max_rain = joined.rain_mm.min()-20, joined.rain_mm.max() + 30
fig, axes = plt.subplots(3, 2, figsize=(10,12), sharex=True, sharey=True)
for i, (ax, station) in enumerate(zip(axes.flatten(), stations_names_list), 1):
  sub_data = joined.loc[joined['station']==station].sort_values(by='month_y')
  ax.plot(sub_data.month_name, sub_data.rain_mm, lw = 1.5, color = 'blue', label= 'measured')
  ax.plot(sub_data.month_name, sub_data.model_rain_mm, lw = 1.5, color='red', label= 'modelled')
  ax.legend()
  # Figure title
  fig.suptitle('Seasonal Rainfall observations - Taita-Taveta')
  ax.text(2, max_temp-20, station)
  ax.grid(b=True, which='major', color='#dddddd', linestyle='-')
  ax.set_ylim(min_temp, max_temp)
  plt.setp(ax.xaxis.get_majorticklabels(), rotation=90)
  # Axis labels
  if i== 1 or i==3 or i==5:
    ax.set_ylabel('Rainfall [mm]')
  if i== 5 or i==6:
    ax.set_xlabel('Date')
  plt.tight_layout()
  plt.subplots_adjust(top=0.95)










#
#import numpy as np
#import pandas as pd
#import seaborn as sns
#sns.set(style="white")
#
## Generate a random correlated bivariate dataset
#mean = [0, 0]
#cov = [(1, .5), (.5, 1)]
#x1 = pd.Series(x, name="$X_1$")
#x2 = pd.Series(y, name="$X_2$")
#
## Show the joint distribution using kernel density estimation
#g = sns.jointplot(x1, x2, kind="kde", height=7, space=0)


# =============================================================================
# 
# 
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# 
# sns.set(style="dark")
# rs = np.random.RandomState(50)
# 
# # Set up the matplotlib figure
# f, axes = plt.subplots(3, 3, figsize=(9, 9), sharex=True, sharey=True)
# 
# # Rotate the starting point around the cubehelix hue circle
# for ax, s in zip(axes.flat, np.linspace(0, 3, 10)):
# 
#     # Create a cubehelix colormap to use with kdeplot
#     cmap = sns.cubehelix_palette(start=s, light=1, as_cmap=True)
# 
#     # Generate and plot a random bivariate dataset
# #    x, y = rs.randn(2, 50)
#     sns.kdeplot(x, y, cmap=cmap, shade=True, cut=5, ax=ax)
# #    ax.set(xlim=(-3, 3), ylim=(-3, 3))
# 
# f.tight_layout()
# =============================================================================
