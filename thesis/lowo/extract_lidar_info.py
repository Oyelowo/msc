import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import re



filepath = r'C:\Users\oyeda\Desktop\msc\thesis\lidar_text_info\*.txt'



def get_density_spacing_info(input_dir=None, output_path_file=None):
    dirname=os.path.dirname(os.path.abspath(__file__))
    current_dir=os.getcwd()
    # print(current_dir)
    filename=os.path.join(current_dir, 'lidar_tiles_info/*.txt')
    if(input_dir):
        filename = os.path.join(input_dir, '/*.txt')

    # filename = os.path.join(input_path, '/*.txt') or os.path.join(dirname, 'lidar_tiles_info/*.txt')
    list_of_files = glob.glob(filename) 
    lidar_info = pd.DataFrame()
    lidar_info['tilesNumber']= None

    for i, file in enumerate(list_of_files, 1):
        dataset=pd.read_csv(file, delimiter="\t")

    # get the point density and point spacing which are on line 39 and 40 respectively
        density= str(dataset[39: 40])
        spacing = str(dataset[40:41])

    # extract all and last return densities. Do same for spacing. There are two values for each
        all_returns_density, last_returns_density = re.findall("\d+\.\d+", density)
        all_returns_spacing, last_returns_spacing = re.findall("\d+\.\d+", spacing)

    # Insert the values into the dataframe
        lidar_info.loc[i, 'tilesNumber']=int(i)
        lidar_info.loc[i, 'all_returns_density']=all_returns_density
        lidar_info.loc[i, 'last_returns_density']=last_returns_density 
        lidar_info.loc[i, 'all_returns_spacing']=all_returns_spacing
        lidar_info.loc[i, 'last_returns_spacing']=last_returns_spacing

    if not output_path_file:
        output_path_file = os.path.join(current_dir, 'lidar_info_extracted.csv')
    lidar_info.to_csv(output_path_file)
    return lidar_info