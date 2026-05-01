"""
NexIA Dashboard — Router principal
Define la navegación de todas las páginas usando st.navigation
"""
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="NexIA Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Definir páginas ───────────────────────────────────────────
inicio = st.Page(
    "inicio.py",
    title="Inicio",
    icon="🧠",
    default=True,
)

pages_nutriflow = [
    st.Page("pages/01_NutriFlow/01_Resumen_Diario.py", title="Resumen Diario", icon="📊"),
    st.Page("pages/01_NutriFlow/02_Evolucion.py", title="Evolución", icon="📈"),
    st.Page("pages/01_NutriFlow/03_Distribucion.py", title="Distribución", icon="🥧"),
    st.Page("pages/01_NutriFlow/04_Datos_Crudos.py", title="Datos Crudos", icon="📋"),
]

pages_futuras = [
    st.Page("pages/_placeholder.py", title="Body Lab", icon="🏋️"),
    st.Page("pages/_placeholder.py", title="Hábitos", icon="✅"),
]

# ── Navegación ────────────────────────────────────────────────
nav = st.navigation(
    {
        "": [inicio],
        "🥗 NutriFlow": pages_nutriflow,
        "🔜 Próximos proyectos": pages_futuras,
    },
    position="sidebar",
)

nav.run()
