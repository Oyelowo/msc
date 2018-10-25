import fiona
import matplotlib.pyplot as plt
import geopandas as gpd
import shapely



shapefile=r'E:\LIDAR_FINAL\2015\buildings\buildings_2015.shp'

shp = r'C:\Users\oyeda\Desktop\THESIS\BuildingBoundary\building_mask_2m_edit_Sentinel.shp'
# buildings_data = pd.read_csv()

# shape = fiona.open(shp)


data = gpd.read_file(shp)
#data=data[0:20].copy()
print(type(data))

# points = gpd.read_file('points.shp')


# print(data.head())
# data.plot()
# plt.show()

data['geometry'] = data['geometry'].simplify(1.5, preserve_topology=True)
data.plot()
plt.show()
# geometry=data['geometry'].head()
# print('geometry', geometry)

data['area2']= data['geometry'].area
#for i, row in data.iterrows():
#    polygon_area= row['geometry'].area
#   data.loc[i, 'area']=polygon_area
#    print('polygon area of ',i, 'is',round(polygon_area, 2))
data.to_file("taita_test.shp")
