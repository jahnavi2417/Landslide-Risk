import subprocess
import os

def calculate_slope(input_dem_path, output_slope_path):
    gdal_path = r"C:\Program Files\QGIS 3.44.0\bin\gdaldem.exe"
    
    # Ensure paths are in absolute form
    input_dem_path = os.path.abspath(input_dem_path)
    output_slope_path = os.path.abspath(output_slope_path)

    try:
        subprocess.run([gdal_path, "slope", input_dem_path, output_slope_path, "-of", "GTiff"], check=True)
        print(f"Slope file created at: {output_slope_path}")
    except subprocess.CalledProcessError as e:
        print("Error while running gdaldem:", e)
