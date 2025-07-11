import subprocess
import rasterio

def align_soil_to_slope(slope_path, input_soil, aligned_output):
    #Align soil raster to slope raster using gdalwarp with automated extent & resolution.
    gdalwarp_path = r"C:\Program Files\QGIS 3.44.0\bin\gdalwarp.exe"

    with rasterio.open(slope_path) as src:
        bounds = src.bounds
        res_x, res_y = src.res

    subprocess.run([
        gdalwarp_path,
        "-r", "near",
        "-t_srs", "EPSG:4326",
        "-te", str(bounds.left), str(bounds.bottom), str(bounds.right), str(bounds.top),
        "-tr", str(res_x), str(res_y),
        "-overwrite",
        input_soil,
        aligned_output
    ])
    #print(f"✅ Soil raster aligned to slope raster: {aligned_output}")

