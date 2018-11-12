



import os
import urllib

def get_filename(url):
    """
    Parses filename from given url
    """
    if url.find('/'):
        return url.rsplit('/', 1)[1]

# Filepaths
outdir = r"E:\LIDAR_FINAL\data\rain_validation"
url_list=[]
for year in range(2011, 2014):
  for month in range(1, 13):
    if month < 10:
      month = '0' + str(month)
    url_list.append("https://www.wsl.ch/lud/chelsa/data/timeseries/prec/CHELSA_prec_{y}_{m}_V1.2.1.tif".format(y=year, m=month))    
    print(year,':', month)
print(url_list[0])
# File locations

url_list = url_list[1:]
# Create folder if it does no exist
if not os.path.exists(outdir):
    os.makedirs(outdir)
# Download files
for url in url_list:
    # Parse filename
    fname = get_filename(url)
    outfp = os.path.join(outdir, fname)
    # Download the file if it does not exist already
    if not os.path.exists(outfp):
        print("Downloading", fname)
        r = urllib.request.urlretrieve(url, outfp)
        


# =============================================================================
# 
# =============================================================================
        
import glob
import pandas as pd
import matplotlib.pyplot as plt
import os
rain_dir = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain"
rain_dir_all = r"E:\LIDAR_FINAL\data\rainfall_data_field\rain\Precipitation\*.XLSX"

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
  return df

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
  agg_data['station'] = station_name
  plt.plot(agg_data.Date, agg_data.rain_mm)
  all_data = all_data.append(agg_data)
#  merged_df = pd.merge(merged_df, agg_data,  on='Date', how='outer')
  print(agg_data.head(5))
  print(i)




plt.plot(agg_data.Date, agg_data.rain_mm)
merged_df = pd.merge(agg_data, agg_data,  on='Date', how='outer')




start_dates = '1/1/2011'
end_dates = '1/1/2018'
[pd.date_range(start, end, freq='M') for start, end in zip(start_dates, end_dates)] 


data["Rain_(mm)"].max()
plt.plot(data['Date'], data["Rain_(mm)"])

all_data = pd.read_excel(os.path.join(rain_dir, 'Taita_prec&temp_summary_statistics.xls.XLSX')) 
