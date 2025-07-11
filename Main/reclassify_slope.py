import rasterio
import numpy as np

def reclassify_slope(input_slope_path, output_path):
    with rasterio.open(input_slope_path) as src:
        slope_data = src.read(1)
        profile = src.profile

        #reclassification logic
        reclass_data = np.zeros_like(slope_data)
        reclass_data[(slope_data >= 0) & (slope_data < 15)] = 1
        reclass_data[(slope_data >= 15) & (slope_data < 30)] = 2
        reclass_data[(slope_data >= 30) & (slope_data < 45)] = 3
        reclass_data[slope_data >= 45] = 4

        #save the result
        profile.update(
            dtype=rasterio.uint8,
            nodata=0  #valid nodata for uint8
        )
        with rasterio.open(output_path, 'w', **profile) as dst:
            dst.write(reclass_data.astype(rasterio.uint8), 1)

    #print(f"Reclassified slope saved at: {output_path}")
    return output_path
