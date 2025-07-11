import rasterio
import rasterio.mask

def clip_raster_to_match(input_raster, clip_reference_raster, output_path):
    #Get bounds of the slope raster
    with rasterio.open(clip_reference_raster) as ref:
        bounds = ref.bounds
        crs = ref.crs

    #Create a bounding box geometry manually
    geometry = {
        "type": "Polygon",
        "coordinates": [[
            [bounds.left, bounds.top],
            [bounds.right, bounds.top],
            [bounds.right, bounds.bottom],
            [bounds.left, bounds.bottom],
            [bounds.left, bounds.top]
        ]]
    }

    #Clip the soil raster using rasterio.mask
    with rasterio.open(input_raster) as src:
        out_image, out_transform = rasterio.mask.mask(src, [geometry], crop=True)
        out_meta = src.meta.copy()

    #Update and save the clipped raster
    out_meta.update({
        "driver": "GTiff",
        "height": out_image.shape[1],
        "width": out_image.shape[2],
        "transform": out_transform
    })

    with rasterio.open(output_path, "w", **out_meta) as dest:
        dest.write(out_image)

    #print(f"✅ Soil raster clipped to slope raster: {output_path}")

