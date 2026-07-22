import streamlit as st
import folium
from streamlit_folium import st_folium
import requests
from geopy.geocoders import Nominatim

st.set_page_config(page_title="Pianificatore Viaggi Camper", layout="wide", page_icon="🚐")

st.title("🚐 Pianificatore Viaggi & Itinerari Camper")

if "tappe" not in st.session_state:
    st.session_state.tappe = []

    geolocator = Nominatim(user_agent="camper_app_poi")

    # Sidebar
    st.sidebar.header("⚙️ Impostazioni Veicolo")
    consumo = st.sidebar.number_input("Consumo medio (L/100km)", value=10.5, step=0.5)
    prezzo_carburante = st.sidebar.number_input("Prezzo Carburante (€/L)", value=1.75, step=0.05)

    st.sidebar.markdown("---")
    st.sidebar.header("➕ Aggiungi Tappa & POI")
    citta = st.sidebar.text_input("Città / Località")
    tipo_sosta = st.sidebar.selectbox("Tipo Sosta", ["Sosta Libera", "Area Sosta", "Campeggio", "Punto Camper"])
    costo_sosta = st.sidebar.number_input("Costo Sosta (€)", value=0.0, step=1.0)

    # Categoria Punti di Interesse per la tappa
    poi_principali = st.sidebar.text_area("🏛️ Punti di Interesse / Attrazioni (separati da virgola)",
                                           placeholder="Es. Centro storico, Parco naturale, Spiaggia")

                                           if st.sidebar.button("Inserisci Tappa nell'Itinerario"):
                                               if citta:
                                                       st.session_state.tappe.append({
                                                                   "citta": citta,
                                                                               "tipo_sosta": tipo_sosta,
                                                                                           "costo_sosta": costo_sosta,
                                                                                                       "poi": poi_principali
                                                                                                               })
                                                                                                                       st.sidebar.success(f"Tappa {citta} aggiunta!")

                                                                                                                       # Schede
                                                                                                                       tab_mappa, tab_poi, tab_budget = st.tabs(["🗺️ Mappa & Itinerario", "📍 Punti di Interesse (POI)", "💰 Budget"])

                                                                                                                       with tab_mappa:
                                                                                                                           if len(st.session_state.tappe) > 0:
                                                                                                                                   coords = []
                                                                                                                                           for t in st.session_state.tappe:
                                                                                                                                                       loc = geolocator.geocode(t["citta"])
                                                                                                                                                                   if loc:
                                                                                                                                                                                   coords.append((loc.latitude, loc.longitude, t))

                                                                                                                                                                                           if coords:
                                                                                                                                                                                                       m = folium.Map(location=[coords[0][0], coords[0][1]], zoom_start=6)
                                                                                                                                                                                                                  
                                                                                                                                                                                                                              # Segnaposto Tappe e POI
                                                                                                                                                                                                                                          for idx, (lat, lon, info) in enumerate(coords):
                                                                                                                                                                                                                                                          # Marker Tappa principale
                                                                                                                                                                                                                                                                          folium.Marker(
                                                                                                                                                                                                                                                                                              [lat, lon],
                                                                                                                                                                                                                                                                                                                  popup=f"<b>Tappa {idx+1}: {info['citta']}</b><br>Sosta: {info['tipo_sosta']}",
                                                                                                                                                                                                                                                                                                                                      icon=folium.Icon(color="red", icon="home")
                                                                                                                                                                                                                                                                                                                                                      ).add_to(m)

                                                                                                                                                                                                                                                                                                                                                                  st_folium(m, width=900, height=500)

                                                                                                                                                                                                                                                                                                                                                                  with tab_poi:
                                                                                                                                                                                                                                                                                                                                                                      st.subheader("📍 Dettaglio Punti di Interesse per Tappa")
                                                                                                                                                                                                                                                                                                                                                                          if len(st.session_state.tappe) > 0:
                                                                                                                                                                                                                                                                                                                                                                                  for t in st.session_state.tappe:
                                                                                                                                                                                                                                                                                                                                                                                              with st.expander(f"📌 Attrazioni e POI a: {t['citta']}"):
                                                                                                                                                                                                                                                                                                                                                                                                              st.write(f"**Tipologia Sosta:** {t['tipo_sosta']}")
                                                                                                                                                                                                                                                                                                                                                                                                                              st.write(f"**Da visitare / Note:** {t['poi'] if t['poi'] else 'Nessun POI specificato'}")
                                                                                                                                                                                                                                                                                                                                                                                                                                  else:
                                                                                                                                                                                                                                                                                                                                                                                                                                          st.info("Aggiungi delle tappe per visualizzare la lista dei Punti di Interesse.")

                                                                                                                                                                                                                                                                                                                                                                                                                                          with tab_budget:
                                                                                                                                                                                                                                                                                                                                                                                                                                              st.subheader("Riepilogo Costi")
                                                                                                                                                                                                                                                                                                                                                                                                                                                  if len(st.session_state.tappe) > 0:
                                                                                                                                                                                                                                                                                                                                                                                                                                                          tot_soste = sum(t["costo_sosta"] for t in st.session_state.tappe)
                                                                                                                                                                                                                                                                                                                                                                                                                                                                  st.write(f"**Totale Soste:** {tot_soste:.2f} €")
