"""
NexIA Dashboard — Inicio
"""
import streamlit as st

st.set_page_config(page_title="NexIA Dashboard", page_icon="🧠", layout="wide")

st.title("🧠 NexIA Dashboard")
st.caption("Centro de monitoreo inteligente — Brooks · 2026")

st.divider()

col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("🏋️ Body Lab")
    st.caption("Rendimiento físico, entrenamiento y composición corporal")
    st.button("Próximamente", disabled=True, use_container_width=True)

with col2:
    st.subheader("✅ Hábitos")
    st.caption("Seguimiento de hábitos diarios y consistencia")
    st.button("Próximamente", disabled=True, use_container_width=True)

with col3:
    st.subheader("🥗 NutriFlow")
    st.caption("Registro de alimentación, macros y metas nutricionales")
    st.page_link("pages/01_Resumen_Diario.py", label="Abrir NutriFlow", use_container_width=True)

st.divider()
st.subheader("🥗 Módulos de NutriFlow")

cols = st.columns(4)
with cols[0]:
    st.page_link("pages/01_Resumen_Diario.py", label="📊 Resumen Diario", use_container_width=True)
with cols[1]:
    st.page_link("pages/02_Evolucion.py", label="📈 Evolución", use_container_width=True)
with cols[2]:
    st.page_link("pages/03_Distribucion.py", label="🥧 Distribución", use_container_width=True)
with cols[3]:
    st.page_link("pages/04_Datos_Crudos.py", label="📋 Datos Crudos", use_container_width=True)
