# =============================================================================
# VALIDATE ROOF AREAS
# =============================================================================

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point

digitized_roof = gpd.read_file(r'E:\LIDAR_FINAL\diigised_Samples_roofs\building\buildings\new_buildings.shp')
roof_2013 = gpd.read_file(r'E:\LIDAR_FINAL\2013\buildings\buildings_2013_projected_regularized.shp')
roof_2015 = gpd.read_file(r'E:\LIDAR_FINAL\data\2015\buildings\buildings_2015_simplified.shp')
aoi = gpd.read_file(r'E:\LIDAR_FINAL\diigised_Samples_roofs\aoi_roof_samples.shp')


del digitized_roof['buildings']


bbox = roof_2013.total_bounds
digitized_roof['area'] = digitized_roof['geometry'].area
digitized_roof['ID'] = digitized_roof.index + 1

# =============================================================================
# GET THE BOUDING BOX OF THE DIGITISED ROOFS AND MAKE THE AOI OUT OF IT
# =============================================================================
xmin, ymin, xmax, ymax = digitized_roof.total_bounds
coords = [[xmin, ymin], [xmin, ymax],[xmax, ymax],[xmax, ymin]]
pp = Polygon([[point[0], point[1]] for point in coords])
aoi = gpd.GeoDataFrame(gpd.GeoSeries(pp), columns=['geometry'])
aoi.plot()







roof_2013['area'] = roof_2013.geometry.area
roof_2013 = roof_2013.loc[(roof_2013['area']>10) & (roof_2013['area']<2000)].reset_index(drop=True)

roof_2015['area'] = roof_2015.geometry.area
roof_2015 = roof_2015.loc[(roof_2015['area']>10) & (roof_2015['area']<2000)].reset_index(drop=True)


roof_2013.plot(column='area', cmap="RdBu", scheme="quantiles", alpha=0.9)
#del digitized_roof['buildings']
roof_2013.isna().sum()
digitized_roof.isna().sum()

roof_2013['geometry'] = roof_2013['geometry']
digitized_roof['geometry'][1]
roof_2013['geometry'][3]

roof_2013r = roof_2013.loc[6:12,:]
print(roof_2013.loc[12,'geometry'])
roof_2013.loc[14,'geometry'].exterior

poly1 = digitized_roof.copy()
poly2 = roof_2013.copy()
data = []
for index, orig in poly1.iterrows():
    for index2, ref in poly2.iterrows():      
        if ref['geometry'].intersects(orig['geometry']): 
         owdspd=orig['id']
         data.append({'geometry':ref['geometry'].intersection(orig['geometry']),'wdspd':owdspd})
    print(index)
data

m = gpd.GeoDataFrame(data)
m[0:5].plot()
m.loc[m['wdspd']==15]


kkn = m.groupby('wdspd')
len(kkn)

((500 - 412) * 100)/ 500



len(data)
for geom in data: 
   print(geom)
   
len(data)

poly1.columns
#poly1_c = poly1[['geometry', 'ID']]
poly1_geom, poly1_ID = poly1['geometry'], poly1['ID']
poly2_geom, poly2_ID = poly2['geometry'], poly2['ID']
list(zip(poly1_geom, poly1_ID))

h = gpd.GeoDataFrame()
for i, (orig_geom, orig_ID) in enumerate(zip(poly1_geom, poly1_ID)):   
   print(orig_ID)


intersection = gpd.overlay(digitized_roof, roof_2015, how='intersection')

#roof_2013 = roof_2013.dissolve(by='area')

digitized_roof.exterior
roof_2013.exterior

print(roof_2013.geom_type)
