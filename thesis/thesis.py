
# Import library and dataset
import seaborn as sns
import matplotlib.pyplot as plt
from lowo.extract_lidar_info import get_density_spacing_info as ex
import pandas as pd
data = pd.read_csv('./lidar_info_extracted.csv')

# ex()

# # Make default histogram of sepal length
sns.distplot( data['all_returns_density'] )

data.describe().to_csv('output_data/2015_lidar_info.csv')
# plt.show()
 
# Control the number of bins
sns.distplot( data['all_returns_density'] , bins=20 )
# plt.show()


