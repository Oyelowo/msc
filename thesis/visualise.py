
# Import library and dataset
import seaborn as sns
import matplotlib.pyplot as plt
from lowo.extract_lidar_info import get_density_spacing_info as ex
import pandas as pd
data = pd.read_csv('./lidar_info_extracted.csv')

# skip the first two column
data=data.iloc[:, 2:] 
# ex()

import sys
sys.path
from rasterToPolygon import polygonize

data.describe().to_csv('output_data/2015_lidar_info_stat.csv')
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))

ax11=axes[0, 0]
ax12=axes[0, 1]
ax21=axes[1, 0]
ax22=axes[1, 1]

# fig.tight_layout()
plt.suptitle('Distribution of point density and spacing of the 2015 LIDAR Data')
# # Make default histogram of sepal length
sns.distplot( data['all_returns_density'] , ax=ax11, bins=20 )
sns.distplot( data['last_returns_density'] , ax=ax12, bins=20) 
sns.distplot( data['all_returns_spacing'] , ax=ax21, bins=20)
sns.distplot( data['last_returns_spacing'] , ax=ax22, bins=20)
# plt.legend()
ax11.set(xlabel='all returns', ylabel='point density(points/sqm)')
ax12.set(xlabel='last returns', ylabel='')
ax21.set(xlabel='all returns', ylabel='point spacity(points/sqm)')
ax22.set(xlabel='last returns', ylabel='')
plt.savefig('./output_data/spacing_density2015.png')
 
# plt.show(block=True)    
   
# Control the number of bins

fig, ax = plt.subplots()

# hide axes
fig.patch.set_visible(False)
ax.axis('off')
ax.axis('tight')

ax.table(cellText=data.describe().round(decimals=2).values, colLabels=data.describe().columns, loc='center')

fig.tight_layout()
# plt.savefig('./output_data/stat_2015.png')

# plt.show()


