import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np


points=gpd.read_file(shp)
xmin,ymin,xmax,ymax =  points.total_bounds
gridWidth = 2000
gridHeight = 1000
rows = int(np.ceil((ymax-ymin) /  gridHeight))
cols = int(np.ceil((xmax-xmin) / gridWidth))
XleftOrigin = xmin
XrightOrigin = xmin + gridWidth
YtopOrigin = ymax
YbottomOrigin = ymax- gridHeight
polygons = []
for i in range(cols):
    Ytop = YtopOrigin
    Ybottom =YbottomOrigin
    for j in range(rows):
        polygons.append(Polygon([(XleftOrigin, Ytop), (XrightOrigin, Ytop), (XrightOrigin, Ybottom), (XleftOrigin, Ybottom)])) 
        Ytop = Ytop - gridHeight
        Ybottom = Ybottom - gridHeight
    XleftOrigin = XleftOrigin + gridWidth
    XrightOrigin = XrightOrigin + gridWidth

grid = gpd.GeoDataFrame({'geometry':polygons})
grid.to_file("grid.shp")

grid.plot()
