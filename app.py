"""
NutriFlow Dashboard — NexIA
Dashboard de seguimiento nutricional con conexión a Google Sheets
"""
import streamlit as st

st.set_page_config(
    page_title="NutriFlow Dashboard",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🥗 NutriFlow Dashboard")
st.markdown("Dashboard de seguimiento nutricional — NexIA")
st.divider()

st.info("Selecciona una sección en el menú lateral para comenzar.")
