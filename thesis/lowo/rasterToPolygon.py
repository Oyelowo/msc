import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd

def polygonize(raster, old_crs, new_crs):
    mask = None
    with rasterio.drivers():
        with rasterio.open(raster) as src:
            image = src.read(1) # first band
            results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v) 
            in enumerate(
                shapes(image, mask=mask, transform=src.affine)))

    geoms = list(results)
    print(shape(geoms[0]['geometry']))

    gpd_polygonized_raster  = gpd.GeoDataFrame.from_features(geoms)
    gpd_polygonized_raster.crs = old_crs
    gpd_polygonized_raster = gpd_polygonized_raster.to_crs(epsg=new_crs)
    return gpd_polygonized_raster

    #gpd_polygonized_raster.to_file('lowo.shp')
