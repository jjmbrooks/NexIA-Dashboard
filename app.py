"""
NexIA Dashboard — Entrypoint principal
"""
import streamlit as st

# Páginas
inicio = st.Page("inicio.py", title="Inicio", icon="🧠", default=True)

# NutriFlow
resumen = st.Page("01_Resumen_Diario.py", title="Resumen Diario", icon="📊")
evolucion = st.Page("02_Evolucion.py", title="Evolución", icon="📈")
distribucion = st.Page("03_Distribucion.py", title="Distribución", icon="🥧")
datos = st.Page("04_Datos_Crudos.py", title="Datos Crudos", icon="📋")

# Body Lab
bl_resumen = st.Page("05_Resumen_BodyLab.py", title="Resumen Diario", icon="🏋️")
bl_evolucion = st.Page("06_Evolucion_BodyLab.py", title="Evolución", icon="📈")
bl_distribucion = st.Page("07_Distribucion_BodyLab.py", title="Distribución", icon="🥧")

nav = st.navigation(
    {
        "": [inicio],
        "🥗 NutriFlow": [resumen, evolucion, distribucion, datos],
        "🏋️ Body Lab": [bl_resumen, bl_evolucion, bl_distribucion],
    }
)

st.set_page_config(page_title="NexIA Dashboard", page_icon="🧠", layout="wide")
nav.run()
