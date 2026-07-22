pip install streamlit folium streamlit-folium geopy requests pyngrok -q
import streamlit as st
from streamlit_folium import st_folium
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Camper Travel Planner", layout="wide")

st.title("🧭 Camper Travel Planner")

if "stops" not in st.session_state:
    st.session_state.stops = []

    geolocator = Nominatim(user_agent="app_viaggi_camper")

    # Sidebar
    st.sidebar.header("📍 Add Stop")
    fuel_consumption = st.sidebar.number_input("Average consumption (L/ 100 km)", min_value=1.0, max_value=50.0, value=10.0, step=0.5)
    fuel_price = st.sidebar.number_input("Fuel Price (€/L)", min_value=0.5, max_value=5.0, value=1.80, step=0.05)
