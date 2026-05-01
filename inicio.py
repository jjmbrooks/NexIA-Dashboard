"""
NexIA Dashboard — Inicio
Pantalla principal con tarjetas de proyectos clickeables
"""
import streamlit as st

st.title("🧠 NexIA Dashboard")
st.caption("Centro de monitoreo inteligente — Brooks · 2026")

st.divider()

# ── Tarjetas de proyectos (clickeables) ───────────────────────

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div style="background:#1a1c2e;border:1px solid #2a2d4e;border-radius:16px;padding:1.8rem 1.5rem;text-align:center;">
        <div style="font-size:2.8rem;margin-bottom:0.4rem;">🏋️</div>
        <div style="font-size:1.2rem;font-weight:600;color:#e0e0ff;margin-bottom:0.3rem;">Body Lab</div>
        <div style="font-size:0.85rem;color:#aaaacc;margin-bottom:0.6rem;">Rendimiento físico, entrenamiento y composición corporal</div>
        <span style="background:#2a2a1a;color:#facc15;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.8rem;">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="background:#1a1c2e;border:1px solid #2a2d4e;border-radius:16px;padding:1.8rem 1.5rem;text-align:center;">
        <div style="font-size:2.8rem;margin-bottom:0.4rem;">✅</div>
        <div style="font-size:1.2rem;font-weight:600;color:#e0e0ff;margin-bottom:0.3rem;">Hábitos</div>
        <div style="font-size:0.85rem;color:#aaaacc;margin-bottom:0.6rem;">Seguimiento de hábitos diarios y consistencia</div>
        <span style="background:#2a2a1a;color:#facc15;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.8rem;">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="background:#1a1c2e;border:1px solid #6366f1;border-radius:16px;padding:1.8rem 1.5rem;text-align:center;">
        <div style="font-size:2.8rem;margin-bottom:0.4rem;">🥗</div>
        <div style="font-size:1.2rem;font-weight:600;color:#e0e0ff;margin-bottom:0.3rem;">NutriFlow</div>
        <div style="font-size:0.85rem;color:#aaaacc;margin-bottom:0.6rem;">Registro de alimentación, macros y metas nutricionales</div>
        <span style="background:#1a3a2a;color:#4ade80;border-radius:20px;padding:0.2rem 0.8rem;font-size:0.8rem;">Activo</span>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ── Links rápidos a NutriFlow ─────────────────────────────────
st.subheader("🥗 NutriFlow")
st.markdown("Selecciona un módulo para explorar:")

cols = st.columns(4)
with cols[0]:
    st.page_link("pages/01_NutriFlow/01_Resumen_Diario.py", label="📊 Resumen Diario")
with cols[1]:
    st.page_link("pages/01_NutriFlow/02_Evolucion.py", label="📈 Evolución")
with cols[2]:
    st.page_link("pages/01_NutriFlow/03_Distribucion.py", label="🥧 Distribución")
with cols[3]:
    st.page_link("pages/01_NutriFlow/04_Datos_Crudos.py", label="📋 Datos Crudos")

st.divider()

# ── Sidebar info ──────────────────────────────────────────────
st.sidebar.success("Usa el menú de navegación para explorar los proyectos.")
