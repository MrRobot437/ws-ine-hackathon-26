import streamlit as st

from src.map_participation import read_data, read_map, create_figure_map
from src.general_data import read_general_data
from src.panel_general_info import status_panel
from src.evolution_view import detail_view
from src.evolution_data import read_evolution, national_series, read_municipalities


st.set_page_config(layout="wide")
st.markdown(
    "<style>[data-testid='stMainBlockContainer']{padding-top:3rem;padding-bottom:1rem}</style>",
    unsafe_allow_html=True,
)

@st.cache_data
def load():
    """Funcion carga de datos"""
    df = read_data()
    nacional = df["Si votó"].sum() / df["Registros totales"].sum() * 100 # Porcentaje del total nacional

    # Evolution - Federal 2009–2024
    nombres = dict(zip(df["Entidad"], df["Estado"]))
    evol = read_evolution(nombres)
    mun = read_municipalities(nombres)
    return df, read_map(), nacional, read_general_data(), evol, national_series(evol), mun

def on_selecting():
    """Se ejecuta únicamente cuando el usuario hace clic en el mapa"""
    puntos = st.session_state["mapa"].selection.points
    st.session_state["estado"] = puntos[0]["location"] if puntos else None


datos, mapa, nacional, circuitos, evol, nacional_federal, mun = load()
estado = st.session_state.get("estado") # Diccionario que sobrevive a las ejecuciones de Streamlit
vista = st.session_state.get("vista", "mapa")

if vista == "evolucion" and estado:
    detail_view(evol, estado, nacional_federal, mun, datos)
    st.stop()

fig = create_figure_map(datos, mapa)

# Si hay un estado seleccionado, muestra el mapa y el panel; de lo contrario, muestra solo el mapa.
if estado:
    col_mapa, col_panel = st.columns([2, 1])
else:
    col_mapa, col_panel = st.container(), None

with col_mapa:
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={
            "displayModeBar": False,
            "scrollZoom": True,
        },
        on_select=on_selecting,
        selection_mode="points",
        key="mapa",
    )

if col_panel is not None:
    with col_panel:
        status_panel(datos, estado, nacional, evol)
