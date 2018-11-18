import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re



#filepath = r'C:\Users\oyeda\Desktop\msc\thesis\lidar_text_info\*.txt'




def get_density_spacing_info(input_dir):
    filepaths = os.path.join(input_dir, '*.txt')
    list_of_files = glob.glob(filepaths) 
    lidar_info = pd.DataFrame(columns=['tilesNumber'])
    for i, file in enumerate(list_of_files, 1):
        with open(file, 'r') as f:
            text_lines = f.readlines()

    # get the point density and point spacing which are on line 39 and 40 respectively
        for line in text_lines:
          line=line.strip()
    # extract all and last return densities. Do same for spacing. There are two values for each
          if line.startswith('point density'):
            all_returns_density, last_returns_density = re.findall("\d+\.\d+", line)
          elif line.startswith('spacing'):
            all_returns_spacing, last_returns_spacing = re.findall("\d+\.\d+", line)
    # Insert the values into the dataframe
        lidar_info= lidar_info.append({
            'tilesNumber':int(i), 
            'last_returns_density':float(last_returns_density),
            'all_returns_density': float(all_returns_density), 
            'all_returns_spacing': float(all_returns_spacing), 
            'last_returns_spacing': float(last_returns_spacing) 
          }, 
          ignore_index=True)
    return lidar_info
  
  

import clip_raster as ras
outputdir_2015 = r'E:\LIDAR_FINAL\data\lidar_tiles_info_output\lidar_info_2015.txt'
inputdir_2015 = r'E:\LIDAR_FINAL\data\lidar_tiles_info\2015'

outputdir_2013 = r'E:\LIDAR_FINAL\data\lidar_tiles_info_output\lidar_info_2013.txt'
inputdir_2013 = r'E:\LIDAR_FINAL\data\lidar_tiles_info\2013'

lidar2015_info = ras.get_density_spacing_info(inputdir_2015)
lidar2015_info.to_csv(outputdir_2015)

lidar2013_info = ras.get_density_spacing_info(inputdir_2013)
lidar2013_info.to_csv(outputdir_2013)
