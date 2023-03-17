import pyproj
import rasterio

def translate_coordinates(coord):
    # Define the EPSG 32641 and EPSG 4326 coordinate reference systems
    crs_32641 = pyproj.CRS("EPSG:32641")
    crs_4326 = pyproj.CRS("EPSG:4326")

    # Create a transformer object to convert from EPSG 32641 to EPSG 4326
    transformer = pyproj.Transformer.from_crs(crs_32641, crs_4326, always_xy=True)

    # Transform the input coordinate from EPSG 32641 to EPSG 4326
    lon, lat = transformer.transform(coord[0], coord[1])

    # Return the transformed coordinate as a tuple in EPSG 4326 format
    return (lat, lon)
'''
([330000.0, 6424000.0, 0.0 ],
 [ 330000.0, 6425000.0, 0.0 ],
 [ 331000.0, 6425000.0, 0.0 ],
 [ 331000.0, 6424000.0, 0.0 ]
 )
'''
to_translate_pairs = ([(), ()],
                      [(), ()],)
coords_4326_lu = translate_coordinates((330000.0, 6425000.0))
coords_4326_rd = translate_coordinates((331000.0, 6424000.0))
print(coords_4326_lu)
print(coords_4326_rd)



dataset = rasterio.open('images/img_20230317154818.png', 'r')
bands = [1, 2, 3]
data = dataset.read(bands)
transform = rasterio.transform.from_bounds(330000.0, 6424000.0, 331000.0,6425000.0, data.shape[1], data.shape[2])
crs = {'init': 'epsg:32641'}

with rasterio.open('images/test_365.tif', 'w', driver='GTiff',
                   width=data.shape[1], height=data.shape[2],
                   count=3, dtype=data.dtype, nodata=0,
                   transform=transform, crs=crs) as dst:
    dst.write(data, indexes=bands)