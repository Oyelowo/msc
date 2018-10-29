# =============================================================================
# VALIDATE ROOF AREAS
# =============================================================================

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon

digitized_roof = gpd.read_file(r'E:\LIDAR_FINAL\diigised_Samples_roofs\taita_digitised_roof_samples.shp')
roof_2013 = gpd.read_file(r'E:\LIDAR_FINAL\2013\buildings\buildings_2013.shp')
roof_2015 = gpd.read_file(r'E:\LIDAR_FINAL\data\2015\buildings\buildings_2015_simplified.shp')


digitized_roof['area'] = digitized_roof['geometry'].area
digitized_roof['ID'] = digitized_roof.index + 1

roof_2013['area'] = roof_2013.geometry.area
roof_2013 = roof_2013.loc[(roof_2013['area']>10) & (roof_2013['area']<2000)].reset_index(drop=True)

roof_2015['area'] = roof_2015.geometry.area
roof_2015 = roof_2015.loc[(roof_2015['area']>10) & (roof_2015['area']<2000)].reset_index(drop=True)


roof_2013.plot(column='area', cmap="RdBu", scheme="quantiles", k=1, alpha=0.9)
#del digitized_roof['buildings']
roof_2013.isna().sum()
digitized_roof.isna().sum()

roof_2013['geometry'] = Polygon(roof_2013['geometry'])
digitized_roof['geometry'][1]
roof_2013['geometry'][3]

roof_2013r = roof_2013.loc[6:12,:]
print(roof_2013.loc[12,'geometry'])
roof_2013.loc[14,'geometry'].exterior

for i, v in roof_2013.iterrows():
  print(i, roof_2013.loc[i,'geometry'].exterior)

intersection = gpd.overlay(digitized_roof, roof_2015, how='intersection')

#roof_2013 = roof_2013.dissolve(by='area')

digitized_roof.exterior
roof_2013.exterior

print(roof_2013.geom_type)
