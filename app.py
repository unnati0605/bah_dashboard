import streamlit as st
import folium
from streamlit_folium import st_folium

from raster_utils import load_raster, get_pixel_value
from recommendation import irrigation_recommendation

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Smart Irrigation Advisory System",
    page_icon="🌾",
    layout="wide"
)

# =====================================================
# LOAD RASTERS
# =====================================================

eta_ds, eta = load_raster("data/ETa_mandya_seasonal_mm.tif")
rain_ds, rainfall = load_raster("data/Rainfall_Mandya_mm.tif")
wd_ds, water_deficit = load_raster("data/WaterDeficit_Mandya.tif")

# =====================================================
# HEADER
# =====================================================

st.title("🌾 Smart Irrigation Advisory System")
st.markdown("### Mandya District, Karnataka")

st.write("""
This dashboard provides irrigation recommendations using:

- 🌱 Actual Evapotranspiration (ETa)
- 🌧️ CHIRPS Rainfall
- 💧 Water Deficit
""")

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.header("Farmer Inputs")

crop = st.sidebar.selectbox(
    "🌱 Select Crop",
    ["Sugarcane", "Paddy", "Ragi"]
)

date = st.sidebar.date_input("📅 Select Date")

layer = st.sidebar.radio(
    "🗺️ Select Layer",
    ["ETa", "Rainfall", "Water Deficit"]
)

# =====================================================
# KPI ROW
# =====================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Crop", crop)

with col2:
    st.metric("Layer", layer)

with col3:
    st.metric("Date", str(date))

st.divider()

# =====================================================
# MAIN LAYOUT
# =====================================================

left, right = st.columns([3, 1])

# =====================================================
# MAP
# =====================================================

with left:

    st.subheader("🗺️ Interactive Map")

    m = folium.Map(
        location=[12.52, 76.90],
        zoom_start=10,
        tiles="OpenStreetMap"
    )

    folium.Marker(
        [12.52, 76.90],
        popup="Mandya District",
        tooltip="Mandya"
    ).add_to(m)

    map_data = st_folium(
        m,
        width=900,
        height=550
    )

# =====================================================
# RIGHT PANEL
# =====================================================

with right:

    st.subheader("📍 Selected Location")

    if map_data and map_data.get("last_clicked"):

        lat = map_data["last_clicked"]["lat"]
        lon = map_data["last_clicked"]["lng"]

        try:

            eta_value = get_pixel_value(eta_ds, lat, lon)
            rain_value = get_pixel_value(rain_ds, lat, lon)
            wd_value = get_pixel_value(wd_ds, lat, lon)

            st.success("Location Selected")

            st.write(f"Latitude : {lat:.6f}")
            st.write(f"Longitude : {lon:.6f}")

            st.divider()

            st.subheader("📊 Pixel Information")

            # ETa
            if eta_value == eta_ds.nodata:
                st.warning("🌱 No ETa data available.")
            else:
                st.metric("🌱 ETa", f"{eta_value:.2f} mm")

            # Rainfall
            if rain_value == rain_ds.nodata:
                st.warning("🌧️ No Rainfall data available.")
            else:
                st.metric("🌧️ Rainfall", f"{rain_value:.2f} mm")

            # Water Deficit
            if wd_value == wd_ds.nodata:
                st.warning("💧 No Water Deficit data available.")
            else:
                st.metric("💧 Water Deficit", f"{wd_value:.2f} mm")

            st.divider()

            # =====================================================
            # IRRIGATION RECOMMENDATION
            # =====================================================

            st.subheader("🚜 Irrigation Recommendation")

            status, advice = irrigation_recommendation(
                crop,
                eta_value,
                rain_value,
                wd_value
            )

            st.success(status)
            st.write(advice)

        except Exception as e:

            st.error("Selected point is outside the raster extent.")
            st.code(str(e))

    else:

        st.info("Click anywhere on the map to get irrigation advice.")