import rasterio
from rasterio.features import shapes
from shapely.geometry import shape
import geopandas as gpd


def polygonize(raster_filepath, old_crs, new_epsg_code):
    mask = None
    with rasterio.drivers():
        with rasterio.open(raster_filepath) as original_raster:
            image = original_raster.read(1) # first band
            results = (
            {'properties': {'grid_value': value}, 'geometry': geometry}
            for index, (geometry, value) in enumerate(shapes(image, mask=mask, transform=original_raster.affine)))

    geoms = list(results)
    print(shape(geoms[0]['geometry']))

    gpd_polygonized_raster  = gpd.GeoDataFrame.from_features(geoms)
    gpd_polygonized_raster.crs = old_crs
    gpd_polygonized_raster = gpd_polygonized_raster.to_crs(new_epsg_code)
    return gpd_polygonized_raster

    #gpd_polygonized_raster.to_file('lowo.shp')




# =============================================================================
# def polygonize(raster_fp, old_crs, new_crs_number):
#     mask = None
#     with rasterio.drivers():
#         with rasterio.open(raster_fp) as src:
#             image = src.read(1) # first band
#             results = (
#             {'properties': {'raster_val': v}, 'geometry': s}
#             for i, (s, v) in enumerate(shapes(image, mask=mask, transform=src.affine)))
# 
#     geoms = list(results)
#     print(shape(geoms[0]['geometry']))
# 
#     gpd_polygonized_raster  = gpd.GeoDataFrame.from_features(geoms)
#     gpd_polygonized_raster.crs = old_crs
#     gpd_polygonized_raster = gpd_polygonized_raster.to_crs(new_crs_number)
#     return gpd_polygonized_raster
# =============================================================================