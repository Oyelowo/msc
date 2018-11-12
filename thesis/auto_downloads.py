# Script for downloading the precipitation data from Chesla

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