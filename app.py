"""
NexIA Dashboard — Entrypoint principal
"""
import streamlit as st

# Páginas
inicio = st.Page("inicio.py", title="Inicio", icon="🧠", default=True)
resumen = st.Page("01_Resumen_Diario.py", title="Resumen Diario", icon="📊")
evolucion = st.Page("02_Evolucion.py", title="Evolución", icon="📈")
distribucion = st.Page("03_Distribucion.py", title="Distribución", icon="🥧")
datos = st.Page("04_Datos_Crudos.py", title="Datos Crudos", icon="📋")

nav = st.navigation(
    {
        "": [inicio],
        "🥗 NutriFlow": [resumen, evolucion, distribucion, datos],
    }
)

st.set_page_config(page_title="NexIA Dashboard", page_icon="🧠", layout="wide")
nav.run()
