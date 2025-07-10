import rasterio
import numpy as np
from rasterio.enums import Resampling

def generate_landslide_risk(slope_path, soil_path, output_path):
    # Read slope raster
    with rasterio.open(slope_path) as slope_src:
        slope = slope_src.read(1)
        profile = slope_src.profile

    # Read soil raster and match shape
    with rasterio.open(soil_path) as soil_src:
        soil = soil_src.read(
            1,
            out_shape=(1, slope.shape[0], slope.shape[1]),
            resampling=Resampling.nearest
        )[0]

    # Calculate weighted risk score
    risk_score = slope * 0.5 + soil * 0.5

    # Reclassify risk
    risk = np.select(
        [risk_score < 1.5, risk_score < 2.5],
        [1, 2],  # 1 = Low, 2 = Medium
        default=3  # 3 = High
    )

    # Update profile and save
    profile.update(dtype=rasterio.uint8, nodata=0)

    with rasterio.open(output_path, "w", **profile) as dst:
        dst.write(risk.astype(rasterio.uint8), 1)

    #print(f"✅ Landslide risk map created: {output_path}")

