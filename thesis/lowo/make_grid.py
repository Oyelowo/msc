import geopandas as gpd
from shapely.geometry import Polygon
import numpy as np


def create_grid(gridHeight, gridWidth, bbox, shapefile, grid_filepath, geometry_field='geometry', export=True):
    '''
    bbox:
    '''
    if bbox:
        [minx, maxy , maxx, miny] = bbox
    else:
        shapefile=gpd.read_file(shapefile)
        minx,miny,maxx,maxy =  shapefile[geometry_field].total_bounds

    rows = int(np.ceil((maxy-miny) /  gridHeight))
    cols = int(np.ceil((maxx-minx) / gridWidth))
    XleftOrigin = minx
    XrightOrigin = minx + gridWidth
    YtopOrigin = maxy
    YbottomOrigin = maxy- gridHeight

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
    if export and grid_filepath:
        grid.to_file(grid_filepath) 
    return grid

