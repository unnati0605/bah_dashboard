import rasterio


def load_raster(path):
    """
    Load a GeoTIFF raster.

    Parameters:
        path (str): Path to the raster file.

    Returns:
        dataset : Rasterio dataset object
        image   : First band of the raster as a NumPy array
    """
    dataset = rasterio.open(path)
    image = dataset.read(1)
    return dataset, image


def get_pixel_value(dataset, latitude, longitude):
    """
    Get the raster value at a given latitude and longitude.

    Parameters:
        dataset : Rasterio dataset
        latitude : float
        longitude : float

    Returns:
        float : Pixel value
    """
    row, col = dataset.index(longitude, latitude)

    band = dataset.read(1)

    return band[row, col]