
# Import library and dataset
import seaborn as sns
import matplotlib.pyplot as plt
from lowo.extract_lidar_info import get_density_spacing_info as ex
import pandas as pd
data = pd.read_csv('./lidar_info_extracted.csv')

# skip the first column
data=data.iloc[:, 2:] 
# ex()



data.describe().to_csv('output_data/2015_lidar_info.csv')
print(data)
fig, axes = plt.subplots(nrows=2, ncols=2, figsize=(12,8))


# # Make default histogram of sepal length
sns.distplot( data['all_returns_density'] , ax=axes[0, 0])
sns.distplot( data['last_returns_density'] , ax=axes[0, 1]) 
sns.distplot( data['all_returns_spacing'] , ax=axes[1, 0])
sns.distplot( data['last_returns_spacing'] , ax=axes[1, 1])

plt.show() 
 
# Control the number of bins
sns.distplot( data['all_returns_density'] , bins=20 )
# plt.show()


