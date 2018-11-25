# =============================================================================
# VALIDATE ROOF AREAS
# =============================================================================

import geopandas as gpd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon,Point

# =============================================================================
# IMPORT DATA
# =============================================================================
digitized_roof = gpd.read_file(r'E:\LIDAR_FINAL\data\building_digitised\digitizedb_bbox.shp')
#digitized_roof = gpd.read_file(r'E:\LIDAR_FINAL\diigised_Samples_roofs\building\buildings\new_buildings.shp')
roof_2013_all = gpd.read_file(r'E:\LIDAR_FINAL\data\buildings\2013\roof_polygons\buildings_2013_projected_regularized.shp')
roof_2015_all = gpd.read_file(r'E:\LIDAR_FINAL\data\buildings\2015\roof_polygons\buildings_2015_simplified.shp')
aoi = gpd.read_file(r'E:\LIDAR_FINAL\diigised_Samples_roofs\aoi_roof_samples.shp')



# =============================================================================
# GET THE BOUDING BOX OF THE DIGITISED ROOFS AND MAKE THE AOI OUT OF IT
# =============================================================================
xmin, ymin, xmax, ymax = digitized_roof.total_bounds
coords = [[xmin, ymin], [xmin, ymax],[xmax, ymax],[xmax, ymin]]
pp = Polygon([[point[0], point[1]] for point in coords])
aoi = gpd.GeoDataFrame(gpd.GeoSeries(pp), columns=['geometry'])
aoi.plot()


# =============================================================================
# SELECT ONLY ROOFS WITHIN THE AOI
# =============================================================================
aoi_boundary = aoi.loc[0].geometry
type(aoi_boundary)
roof_2013_all = roof_2013_all[roof_2013_all.geometry.within(aoi_boundary)]
roof_2013_all.plot()
roof_2015_all = roof_2015_all[roof_2015_all.geometry.within(aoi_boundary)]
roof_2015_all.plot()
len(roof_2013_all)
len(roof_2015_all)
len(digitized_roof)


# =============================================================================
# GET AREA AND CREATE ID FOR EACH POLYGON OF THE DIGITISED ROOFS
# =============================================================================
try:
  del digitized_roof['buildings']
  del digitized_roof['id']
  del digitized_roof['fid']
except:
  pass
digitized_roof['area'] = digitized_roof['geometry'].area
digitized_roof['digi_ID'] = digitized_roof.index + 1


# =============================================================================
# FILTER TOO SMALL OR TOO BIG POLYGONS
# =============================================================================
lower_limit, upper_limit = 10, 2000
roof_2013_all['area'] = roof_2013_all.geometry.area
roof_2013 = roof_2013_all.loc[(roof_2013_all['area']>lower_limit) & (roof_2013_all['area']<upper_limit)].reset_index(drop=True)

roof_2015_all['area'] = roof_2015_all.geometry.area
roof_2015 = roof_2015_all.loc[(roof_2015_all['area']>lower_limit) & (roof_2015_all['area']<upper_limit)].reset_index(drop=True)


# =============================================================================
# Check the data
# =============================================================================
roof_2013.plot(column='area', cmap="RdBu", scheme="quantiles", alpha=0.9)
#del digitized_roof['buildings']
roof_2013.isna().sum()
digitized_roof.isna().sum()

digitized_roof['geometry'][1]
roof_2013['geometry'][3]

roof_2013r = roof_2013.loc[6:12,:]
print(roof_2013.loc[12,'geometry'])





# =============================================================================
# poly1 = digitized_roof.copy()
# poly2 = roof_2013.copy()
# data = []
# for index, orig in poly1.iterrows():
#     for index2, ref in poly2.iterrows():      
#         if ref['geometry'].intersects(orig['geometry']): 
#          owdspd=orig['id']
#          data.append({'geometry':ref['geometry'].intersection(orig['geometry']),'wdspd':owdspd})
#     print(index)
# 
# m = gpd.GeoDataFrame(data)
# m.loc[m['wdspd']==15]
# 
# kkn = m.groupby('wdspd')
# len(kkn)
# 
# ((500 - 412) * 100)/ 500
# =============================================================================


# =============================================================================
# INTERSECTING THE DIGITISED AND THE BUILDINGS EXTRACTED FROM LIDAR
# =============================================================================
#poly1_c = poly1[['geometry', 'ID']]
#digi_geom, digi_ID, poly1_area = digitized_roof['geometry'], digitized_roof['ID'], digitized_roof['area']
#roof_2013_geom, roof_2013_area = roof_2013['geometry'], roof_2013['area']
#roof_2015_geom, roof_2015_area = roof_2015['geometry'], roof_2015['area']
#
#digi_zip_list = list(zip(digi_geom, digi_ID, poly1_area))
#roof_2013_zip_list = list(zip(roof_2013_geom, roof_2013_area))
#roof_2015_zip_list = list(zip(roof_2015_geom, roof_2015_area))
#
#digi_intersect_roof_2013=[]
#digi_intersect_roof_2015=[]
#for i, (orig_geom, orig_ID, orig_area) in enumerate(digi_zip_list):
#  for ref_geom, ref_area in roof_2013_zip_list:
#    if ref_geom.intersection(orig_geom):
#      geom = ref_geom.intersection(orig_geom)
#      digi_intersect_roof_2013.append({'geometry': geom, 'digi_ID': orig_ID, 'digi_area':orig_area, 'lidar_area': ref_area})
#      
#  for ref_geom, ref_area in roof_2015_zip_list:
#    if ref_geom.intersection(orig_geom):
#      geom = ref_geom.intersection(orig_geom)
#      digi_intersect_roof_2015.append({'geometry': geom, 'digi_ID': orig_ID,'digi_area':orig_area, 'lidar_area': ref_area})
#  print('Checking:', orig_ID)
#      
#digi_inter_roof13_df = gpd.GeoDataFrame(digi_intersect_roof_2013)
#digi_inter_roof15_df = gpd.GeoDataFrame(digi_intersect_roof_2015)



digi_inter_roof13_df = gpd.sjoin(digitized_roof, roof_2013,how='inner',lsuffix='digi', rsuffix='lidar')
digi_inter_roof15_df = gpd.sjoin(digitized_roof, roof_2015,how='inner', lsuffix='digi', rsuffix='lidar')


# =============================================================================
# ACCURACY ANALYSIS: ERROR OF OMISSION
# =============================================================================
digi_roofs_count = len(digitized_roof)

#2013
digi_inter_roof13_df_grouped = digi_inter_roof13_df.groupby('digi_ID')
correct_roof2013_count = len(digi_inter_roof13_df_grouped)
omission_roof_2013 = ((digi_roofs_count - correct_roof2013_count) *100)/ digi_roofs_count


#2015
digi_inter_roof15_df_grouped = digi_inter_roof15_df.groupby('digi_ID')
correct_roof2015_count = len(digi_inter_roof15_df_grouped)
omission_roof_2015 = ((digi_roofs_count - correct_roof2015_count) *100)/ digi_roofs_count

accuracy_statements = [
    'In 2013, {0} roofs were correctly extracted out of {1} roofs. \n'.format(correct_roof2013_count, digi_roofs_count),   
    'In 2013, {0} roofs were omitted out of {1} roofs. \n'.format(digi_roofs_count -correct_roof2013_count, digi_roofs_count),
     'Percentage of omitted buildings in 2013 is {:.2f}%. \n'.format(omission_roof_2013),
     'Percentage accurately extracted in 2013 is {:.2f}%. \n\n'.format(100-omission_roof_2013),
      
      
      'In 2015, {0} roofs were rightly extracted out of {1} roofs'.format(correct_roof2015_count, digi_roofs_count),
       'In 2015, {} roofs were omitted out of {} roofs. \n'.format(digi_roofs_count -correct_roof2015_count, digi_roofs_count),
      'Percentage of omitted buildings in 2015 is {:.2f}%. \n'.format(round(omission_roof_2015,2)),
      'Percentage accurately extracted in 2015 is {:.2f}%. \n\n'.format(100-omission_roof_2015)
      ]
      

print(*accuracy_statements)
# =============================================================================
# ERROR OF COMMISSION
# =============================================================================
#2013
#digi_inter_roof13_df_grouped = digi_inter_roof13_df.groupby('digi_ID')
correct_roof2013_count = len(digi_inter_roof13_df)
all_roofs_2013_count = len(roof_2013)
falsely_extracted_2013 = (all_roofs_2013_count - correct_roof2013_count)
commission_roof_2013 = (falsely_extracted_2013 *100)/ all_roofs_2013_count

#print('In 2013, {0} roofs were wrongly extracted out of {1} roofs'.format(correct_roof2013_count, digi_roofs_count))
#print('The error of commission for 2013 extraction is {0}%'.format(commission_roof_2013))
#print('Accuracy is {0}%'.format(100-commission_roof_2013))

#2015
#digi_inter_roof15_df_grouped = digi_inter_roof15_df.groupby('digi_ID')
correct_roof2015_count = len(digi_inter_roof15_df)
all_roofs_2015_count = len(roof_2015)
falsely_extracted_2015 = (all_roofs_2015_count - correct_roof2015_count)
commission_roof_2015 = (falsely_extracted_2015 *100)/ all_roofs_2015_count


#print('In 2013, {0} roofs were rightly extracted out of {1} roofs extracted'.format(all_roofs_2015_count, digi_roofs_count))
#print('The error of commission for 2015 extraction is {0}%'.format(round(commission_roof_2015,2)))
#print('Accuracy is {0}%'.format(100-commission_roof_2015))


  
accuracy_statements2 = ['In 2013, {0} roofs were falsely extracted(false positive) out of {1} roofs extracted. \n'.format(falsely_extracted_2013 , all_roofs_2013_count),
      'The percentage of falsely extracted is {:.2f}%. \n\n'.format(commission_roof_2013),
      
      
      'In 2015, {0} roofs were falsely extracted(false positive) out of {1} roofs extracted. \n'.format(falsely_extracted_2015 , all_roofs_2015_count),
      'The percentage of falsely extracted is {:.2f}%. \n'.format(commission_roof_2015)
      ]


statement = '\n'
for sentence in accuracy_statements:
  statement += sentence

for sentence in accuracy_statements2:
  statement += sentence
  
type(statement)
print(statement)
print(*accuracy_statements, *accuracy_statements2)

#accuracy_metrics = str(*accuracy_statements, *accuracy_statements2)
with open(r"E:\LIDAR_FINAL\data\plots\Output.txt", "w") as text_file:
    text_file.write(statement)




# =============================================================================
# ACCURACY: AREA, RMSE, MAE, AND SCATTERPLOT
# =============================================================================
roof_13_agg=gpd.GeoDataFrame()
roof_13_agg['geometry'] = None
for key, group in digi_inter_roof13_df_grouped:
  roof_13_agg.loc[key,'ID'] = key
  roof_13_agg.loc[key,'digi_area'] = group['area_digi'].unique()
  roof_13_agg.loc[key,'lidar_area'] =  group['area_lidar'].sum()
  roof_13_agg.loc[key,'one_to_N_rel'] = len(group['area_lidar'])
  print('Aggregating: ', key)


from pandas.plotting import scatter_matrix
import scipy
import numpy as np
roof_13_agg[23:25].plot()

roof_13_agg.iloc[:,2:4].corr()
scatter_matrix(roof_13_agg.iloc[:,2:4].corr())
roof_13_agg_ = roof_13_agg.loc[(roof_13_agg['one_to_N_rel']==1) & (roof_13_agg.lidar_area<500)]
x, y = roof_13_agg_.digi_area, roof_13_agg_.lidar_area
slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
r_value **2 * 100

plt.scatter(x,y)
plt.plot(np.unique(x), np.poly1d(np.polyfit(x, y, 1))(np.unique(x)))



import seaborn as sns
from scipy import stats
def r2(x, y):
    return stats.pearsonr(x, y)[0] ** 2

ax = sns.jointplot(x, y, kind="reg", stat_func=r2, logx=True, truncate=True, space=0.1)
plt.subplots_adjust(top=0.9)
ax.fig.suptitle('ARoof Areas of Extracted vs Digitised', fontsize=20) # can also get the figure from plt.gcf()
output_fp = r'E:\LIDAR_FINAL\data\plots\digi_vs_lidar2'
plt.savefig(output_fp,  bbox_inches='tight',dpi=300, pad_inches=0.1)



list(roof_13_agg.one_to_N_rel.astype(int)).count(1)

from collections import Counter
c = Counter(list(roof_13_agg.one_to_N_rel.astype(int)))
one_to_N_counts = c.items()

plt.hist(roof_13_agg.one_to_N_rel)
plt.ylabel('Number of Buildings')
plt.xlabel('One to N relationships')
plt.title('One Digitized  Roof to N number of Extracted Roof area to relationships')
plt.ylim(0, 1500)
for item in one_to_N_counts:
  plt.text(item[0]-0.05, item[1]+14, s=item[1])
plt.savefig( r'E:\LIDAR_FINAL\data\plots\one_to_N_relationship', bbox_inches='tight',dpi=300, pad_inches=0.1)


((x-y)/x) *100

roof_13_agg_.mean()
digi_inter_roof13_df_grouped['area_lidar'].agg(lambda x: print(x.mean()))


import numpy as np

def rmse(predictions, targets):
    return np.sqrt(((predictions - targets) ** 2).mean())

rmse_val = rmse(x, y)
print("rms error is: " + str(rmse_val))


def smape(A, F):
    return 100/len(A) * np.sum(2 * np.abs(F - A) / (np.abs(A) + np.abs(F)))
  
print(smape(x,y))


