      import streamlit as st
import folium
from streamlit_folium import st_folium
richieste di importazione
da geopy.geocoders import Nominatim

st.set_page_config(page_title="Pianificatore Viaggi", layout="wide")

st.title ("🗺️ Pianificatore Viaggi in Camper")

if "tappe" not in st.session_state:
    st.session_state.tappe = []

geolocator = Nominatim(user_agent="app_viaggi_camper")

# Sidebar
st.sidebar.header ("📍 Aggiungi Tappa")
consumo = st.sidebar .number_input("Consumo medio (L/ 100 km)", min_value= 1.0 , value= 10.0 , step= 0.5 )
prezzo_carburante = st.sidebar .number_input("Prezzo carburante (€/L)", valore_min= 0,5 , valore= 1.80 , step= 0.05 )

nome_tappa = st.sidebar .text_input("Nome o Indirizzo Tappa")
note_tappa = st.sidebar .text_area("Note / Attività")
km_tappa = st.sidebar .number_input("Km da tappa precedente", min_value= 0.0 , value= 0.0 , step= 10.0 )

if st.sidebar.button ("Inserisci Tappa nell'Itinerario"):
    if nome_tappa:
        try:
            location = geolocator.geocode (nome_tappa)
            if location:
                lat, lon = location.latitude , location.longitude
            else:
                lat, lon = 43.801 , 10.686   # Coordinate di default se non trova la località
                st.sidebar.warning ("Coordinate non trovate, inserita posizione approssimativa.")
           
            st.session_state.tappe.append ({
                "nome": nome_tappa,
                "note": note_tappa,
                "km": km_tappa,
                "lat": lat,
                "lon": lon
            })
            st.sidebar.success (f"Tappa '{nome_tappa}' aggiunta!")
        tranne Eccezione come e:
            st.sidebar.error ("Errore nel recupero delle coordinate.")
    else:
        st.sidebar.error ("Inserisci un nome per la tappa.")

# Layout Principale
col1, col2 = st.colonne ([1,1])

con col1:
    st.subheader ("📋 Lista Tappe e Costi")
   
    totale_km = 0.0
   
    if st.session_state.tappe :
        for idx, tappa in enumerate( st.session_state.tappe ):
            st.markdown (f"**{idx + 1}. {tappa['nome']}** ({tappa['km']} km)")
            if tappa['note']:
                st.caption (f"Note: {tappa['note']}")
            totale_km += tappa['km']
       
        litri_totali = (totale_km / 100 ) * consumo
        costo_totale = litri_totali * prezzo_carburante
       
        st.divider ()
        st.metric ("Chilometri Totali", f"{totale_km:.1f} km")
        st.metric ("Stima Carburante", f"{litri_totali:.1f} L")
        st.metric ("Costo Stimato Carburante", f"{costo_totale:.2f} €")
       
        se st.button ("Svuota Itinerario"):
            st.session_state.tappe = []
            st.rerun ()
    else:
        st.info ("Nessuna tappa inserita. Usa il menu a sinistra per iniziare!")

with col2:
    st.subheader ("🗺️ Mappa del Viaggio")
   
    # Centro mappa su Pescia o sulla prima tappa se presente
    start_lat, start_lon = 43.901 , 10.686
    if st.session_state.tappe :
        start_lat = st.session_state.tappe [0]["lat"]
        start_lon = st.session_state.tappe [0]["lon"]
       
    m = folium.Map (location=[start_lat, start_lon], zoom_start=6)
   
    points = []
    for idx, tappa in enumerate( st.session_state.tappe ):
        coord = [tappa["lat"], tappa["lon"]]
        punti.append (coord)
        folium.Marker (
            coord,
            popup=f"{idx + 1}. {tappa['nome']}",
            tooltip=tappa["nome"]
        ).add_to(m)
       
    if len(points) > 1:
        folium.PolyLine (points, color="blue", weight=3, opacity= 0.8 ).add_to(m)
       
    st_folium(m, width= 600 , height= 450 )                                                                                                                                                             
