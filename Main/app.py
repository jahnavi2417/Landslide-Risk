import streamlit as st
import rasterio
import numpy as np
import matplotlib.pyplot as plt

#importing all the functions
from calculate_slope import calculate_slope
from reclassify_slope import reclassify_slope
from clip_soil import clip_raster_to_match
from risk_map import generate_landslide_risk
from align_raster import align_soil_to_slope


st.title("🌍 Landslide Risk Mapping Tool")

#soil raster path
SOIL_FILE = "Main/Data/Soil_reclassified.tif"  

#user uploads DEM 
uploaded_dem = st.file_uploader("📤 Upload DEM (.tif)", type="tif")

if uploaded_dem:
    #save DEM 
    with open("Main/Uploads/user_dem.tif", "wb") as f:
        f.write(uploaded_dem.read())

    st.success("✅ DEM uploaded successfully!")

    st.info("Generating the landslide risk map...")
    
    #generating slope from DEM
    dem_path = "Main/Uploads/user_dem.tif"
    slope_path = "Main/Data/slope.tif"
    calculate_slope(dem_path, slope_path)

    #reclassifying slope
    slope_reclass_path = "Main/Data/slope_reclass.tif"
    reclassify_slope(slope_path, slope_reclass_path)

    #aligning soil raster 
    soil_path = "Main/Data/Soil_reclassified.tif"
    soil_aligned_path = "Main/Data/soil_aligned.tif"
    align_soil_to_slope(slope_reclass_path, soil_path, soil_aligned_path)

    #clipping soil raster to slope raster 
    clip_raster_to_match(
        input_raster="Main/Data/soil_aligned.tif",
        clip_reference_raster="Main/Data/slope_reclass.tif",
    output_path="Main/Data/soil_clipped.tif"
    )

    #generationg landslide risk map
    generate_landslide_risk(
        slope_path="Main/Data/slope_reclass.tif",
        soil_path="Main/Data/soil_clipped.tif",
        output_path=r"Main/Outputs/risk_map.tif"
    )

    #print("All processes completed successfully.")

    #st.success("✅ Landslide risk map generation started! This may take a few minutes...")

    # Display the risk map
    with rasterio.open("Main/Outputs/risk_map.tif") as src:
        risk = src.read(1)

    st.success("✅ Landslide risk map generated successfully!")

    #displaying the risk map
    st.subheader("🗺️ Landslide Risk Map")
    fig, ax = plt.subplots()
    img=ax.imshow(risk, cmap="OrRd")
    ax.set_title("Landslide Risk Map")
    ax.axis("off")
    # Add colorbar (legend)
    cbar = fig.colorbar(img, ax=ax, ticks=[1, 2, 3])
    cbar.ax.set_yticklabels(['Low', 'Moderate', 'High'])  # Labels for the ticks
    cbar.set_label('Risk Level')
    st.pyplot(fig)

    # Download button for the risk map
    with open("Main/Outputs/risk_map.tif", "rb") as f:
        st.download_button("⬇️ Download Risk Map", f, file_name="risk_map.tif")
