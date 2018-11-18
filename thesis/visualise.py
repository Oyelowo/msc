
# Import library and dataset
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import clip_raster as ras


outputdir_2015 = r'E:\LIDAR_FINAL\data\lidar_tiles_info_output\lidar_info_2015.txt'
inputdir_2015 = r'E:\LIDAR_FINAL\data\lidar_tiles_info\2015'

outputdir_2013 = r'E:\LIDAR_FINAL\data\lidar_tiles_info_output\lidar_info_2013.txt'
inputdir_2013 = r'E:\LIDAR_FINAL\data\lidar_tiles_info\2013'

lidar2015_info = ras.get_density_spacing_info(inputdir_2015)
lidar2015_info.to_csv(outputdir_2015)

lidar2013_info = ras.get_density_spacing_info(inputdir_2013)
lidar2013_info.to_csv(outputdir_2013)

sns.boxplot(lidar2013_info['all_returns_density'])
sns.boxplot(lidar2015_info['all_returns_density'])
sns.boxplot(lidar2013_info['all_returns_spacing'])
sns.boxplot(lidar2015_info['all_returns_spacing'])




data = ras.get_density_spacing_info(inputdir_2015)
sns.heatmap(data)
data.describe().to_csv(r'E:\LIDAR_FINAL\data\lidar_tiles_info_output\2015_lidar_info_stat.txt')

def plot_density_spacing(data, year, outut_fp):
  bg_color="#efefef"
  sns.set(rc={'axes.facecolor':bg_color, 'figure.facecolor':bg_color})
  fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
  
  ax11=axes[0, 0]
  ax12=axes[0, 1]
  ax21=axes[1, 0]
  ax22=axes[1, 1]
  
  # fig.tight_layout()
  plt.suptitle('Distribution of point density and spacing of the {year} LIDAR Data'.format(year=year))
  # # Make default histogram of sepal length
  sns.distplot( data['all_returns_density'] , ax=ax11, bins=20 ,rug=True)
  sns.distplot( data['last_returns_density'] , ax=ax12, bins=20, rug=True) 
  sns.distplot( data['all_returns_spacing'] , ax=ax21, bins=20, rug=True)
  sns.distplot( data['last_returns_spacing'] , ax=ax22, bins=20, rug=True)
  # plt.legend()
  ax11.set(xlabel='all returns', ylabel='point density(points/sqm)')
  ax12.set(xlabel='last returns', ylabel='')
  ax21.set(xlabel='all returns', ylabel='point spacing(m)')
  ax22.set(xlabel='last returns', ylabel='')
  plt.tight_layout()
  plt.subplots_adjust(top=0.95)
  plt.savefig(outut_fp)
  

plot_density_spacing(lidar2013_info, '2013', 'E:\LIDAR_FINAL\data\plots/hist_lidar_density_spacing_2013.png')
plot_density_spacing(lidar2015_info, '2015', 'E:\LIDAR_FINAL\data\plots/hist_lidar_density_spacing_2015.png')
# plt.show(block=True)    
   

from itertools import cycle


def plot_density_spacing_2(dataset, year, outut_fp):
  bg_color="#efefef"
  sns.set(rc={'axes.facecolor':bg_color, 'figure.facecolor':bg_color})
  fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))
  
  ax11=axes[0, 0]
  ax12=axes[0, 1]
  ax21=axes[1, 0]
  ax22=axes[1, 1]
  
  # fig.tight_layout()
  plt.suptitle('Comparison of the Distribution of the Point Density and Spacing of the {year} LIDAR Data'.format(year=year))
  # # Make default histogram of sepal length
  for data, year in zip(dataset, cycle(['2013', '2015'])):
    sns.kdeplot( data['all_returns_density'] , ax=ax11, label=year, shade=True)
    sns.kdeplot( data['last_returns_density'] , ax=ax12, label=year, shade=True) 
    sns.kdeplot( data['all_returns_spacing'] , ax=ax21, label=year, shade=True)
    sns.kdeplot( data['last_returns_spacing'] , ax=ax22, label=year, shade=True)
  # plt.legend()
  ax11.set(xlabel='all returns', ylabel='point density(points/sqm)')
  ax12.set(xlabel='last returns', ylabel='')
  ax21.set(xlabel='all returns', ylabel='point spacing(m)')
  ax22.set(xlabel='last returns', ylabel='')
  plt.tight_layout()
  plt.subplots_adjust(top=0.95)
  plt.savefig(outut_fp)
  
plot_density_spacing_2([lidar2013_info, lidar2015_info],'2013 and 2015', 'E:\LIDAR_FINAL\data\plots/hist_lidar_density_spacing_combined.png')
  
  
# Control the number of bins
def plot_table(data, outut_fp):
  fig, ax = plt.subplots()
  
  # hide axes
  fig.patch.set_visible(False)
  ax.axis('off')
  ax.axis('tight')
  
  ax.table(cellText=data.describe().round(decimals=2).values, colLabels=data.describe().columns, loc='center')
  
  fig.tight_layout()
  plt.savefig(outut_fp)

# plt.show()

plot_table(lidar2013_info, 'E:\LIDAR_FINAL\data\plots/stat_table_lidar_density_spacing_2013.png')

