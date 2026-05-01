"""
NexIA Dashboard — Inicio
"""
import streamlit as st

st.title("🧠 NexIA Dashboard")
st.caption("Centro de monitoreo inteligente — Brooks · 2026")

st.divider()

col1, col2, col3 = st.columns(3, gap="large")

with col1:
    st.subheader("🏋️ Body Lab")
    st.write("Rendimiento físico, entrenamiento")
    st.write("y composición corporal")
    st.button("Próximamente", disabled=True, key="btn_bodylab", use_container_width=True)

with col2:
    st.subheader("✅ Hábitos")
    st.write("Seguimiento de hábitos diarios")
    st.write("y consistencia")
    st.button("Próximamente", disabled=True, key="btn_habitos", use_container_width=True)

with col3:
    st.subheader("🥗 NutriFlow")
    st.write("Registro de alimentación, macros")
    st.write("y metas nutricionales")
    st.page_link("01_Resumen_Diario.py", label="Abrir NutriFlow",
                 use_container_width=True)

st.divider()

st.subheader("🥗 Módulos de NutriFlow")

resumen, evolucion, distribucion, datos = st.columns(4, gap="small")
with resumen:
    st.page_link("01_Resumen_Diario.py", label="📊 Resumen Diario",
                 use_container_width=True)
with evolucion:
    st.page_link("02_Evolucion.py", label="📈 Evolución",
                 use_container_width=True)
with distribucion:
    st.page_link("03_Distribucion.py", label="🥧 Distribución",
                 use_container_width=True)
with datos:
    st.page_link("04_Datos_Crudos.py", label="📋 Datos Crudos",
                 use_container_width=True)
