# =============================================================================
# Validate rainfall data from CHELSA
# =============================================================================
        
import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
import geopandas as gpd
rain_dir = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain"
rain_dir_all = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain\Precipitation\*.XLSX"
buildings_rain_aggr = gpd.read_file(r'E:\LIDAR_FINAL\data\aggregated\buildings_rain_aggr.shp')

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



from datetime import datetime

stations = all_data['station'].unique().tolist()

#stations.remove('Mwatate_Ar112509')

min_temp, max_temp = all_data.rain_mm.min()-20, all_data.rain_mm.max() + 20
fig, axes = plt.subplots(3, 2, figsize=(10,12), sharex=True, sharey=True)
#  plt.suptitle('RAINWATER HARVESTING POTENTIAL IN TAITA')
#  vmin, vmax = dataFrame[column_list].min().min(), dataFrame[column_list].max().max()
for i, (ax, station) in enumerate(zip(axes.flatten(), stations), 1):
  sub_data = all_data.loc[all_data['station']==station]
  ax.plot(sub_data.Date, sub_data.rain_mm, lw = 1.5)
  # Figure title
  fig.suptitle('Seasonal Rainfall observations - Taita-Taveta')
  ax.text(datetime(2012, 2, 15), 380, station)
  ax.grid()
  ax.set_ylim(min_temp, max_temp)
  # Axis labels
  if i in [1, 3, 5]:
    ax.set_ylabel('Rainfall [mm]')
  if i in [5, 6]:
    ax.set_xlabel('Date')


         
monthly_agg_data = pd.DataFrame(columns=["station", "month", "rain_mm"])
i=0
for station in stations:
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
for i, (ax, station) in enumerate(zip(axes.flatten(), stations), 1):
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
         
         


# plt.plot(agg_data.Date, agg_data.rain_mm)
#merged_df = pd.merge(agg_data, agg_data,  on='Date', how='outer')
#
#
#
#
#start_dates = '1/1/2011'
#end_dates = '1/1/2018'
#[pd.date_range(start, end, freq='M') for start, end in zip(start_dates, end_dates)] 
#
#
#data["Rain_(mm)"].max()
#plt.plot(data['Date'], data["Rain_(mm)"])

all_data = pd.read_excel(os.path.join(rain_dir, 'Taita_prec&temp_summary_statistics.xls.XLSX')) 







import pandas as pd
from shapely.geometry import Point
import geopandas as gpd

stations = pd.read_csv(r'E:\LIDAR_FINAL\data\rainfall_data_field\stations_locations\stations.csv')
stations = gpd.GeoDataFrame(stations)
stations = stations.iloc[:,:5]
stations_list = [Point(x, y) for x,y in zip(stations.x, stations.y)]
stations_list[0]
stations['geometry'] = stations_list
stations.plot()
print(stations.crs)
stations.crs = {'init' :'epsg:32737'}


kl = buildings_rain_aggr.plot()
stations.plot(ax=kl, c='red')

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
months_rain_pot = get_column_names_lists('POT', "ann")

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


import numpy as np

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

rmse_val = rmse(joined.model_rain_mm, joined.rain_mm)
print("rms error is: " + str(rmse_val))


from scipy.stats import linregress
rain_stat = linregress(joined.model_rain_mm.tolist(), joined.rain_mm.tolist())
rain_stat.rvalue**2
x,y = joined.model_rain_mm.tolist(), joined.rain_mm.tolist()


import seaborn as sns;sns.set(color_codes=True)
from scipy import stats

def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2
  
x=np.array(x) 
y=np.array(y)
sns.jointplot(x, y, kind="reg", stat_func=r2)
