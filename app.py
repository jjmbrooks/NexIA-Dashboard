"""
NexIA Dashboard — Inicio
Pantalla principal con tarjetas HTML + botones de navegación
"""
import streamlit as st

st.set_page_config(
    page_title="NexIA Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🧠 NexIA Dashboard")
st.caption("Centro de monitoreo inteligente — Brooks · 2026")

st.markdown("""
<style>
    .proyecto-card {
        background: #1a1c2e;
        border: 1px solid #2a2d4e;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        display: block;
        margin-bottom: 0.5rem;
    }
    .proyecto-card.activo {
        border-color: #4ade80;
    }
    .proyecto-icon { font-size: 3rem; margin-bottom: 0.4rem; }
    .proyecto-nombre { font-size: 1.2rem; font-weight: 700; color: #e0e0ff; margin-bottom: 0.3rem; }
    .proyecto-desc { font-size: 0.8rem; color: #999abb; margin-bottom: 0.6rem; line-height: 1.3; }
    .badge {
        display: inline-block;
        border-radius: 20px;
        padding: 0.2rem 0.9rem;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-ok { background: #1a3a2a; color: #4ade80; }
    .badge-wait { background: #2a2a1a; color: #facc15; }
</style>
""", unsafe_allow_html=True)

st.divider()

# ── Tarjetas de proyectos ─────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown("""
    <div class="proyecto-card">
        <div class="proyecto-icon">🏋️</div>
        <div class="proyecto-nombre">Body Lab</div>
        <div class="proyecto-desc">Rendimiento físico, entrenamiento y composición corporal</div>
        <span class="badge badge-wait">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="proyecto-card">
        <div class="proyecto-icon">✅</div>
        <div class="proyecto-nombre">Hábitos</div>
        <div class="proyecto-desc">Seguimiento de hábitos diarios y consistencia</div>
        <span class="badge badge-wait">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="proyecto-card activo">
        <div class="proyecto-icon">🥗</div>
        <div class="proyecto-nombre">NutriFlow</div>
        <div class="proyecto-desc">Registro de alimentación, macros y metas nutricionales</div>
        <span class="badge badge-ok">Activo</span>
    </div>
    """, unsafe_allow_html=True)
    # Botón debajo de la tarjeta
    if st.button("🥗 Ir a NutriFlow", key="btn_nutriflow", use_container_width=True):
        st.switch_page("pages/01_Resumen_Diario.py")

st.divider()

# ── Links rápidos a módulos de NutriFlow ──────────────────────
st.subheader("🥗 NutriFlow — módulos")

if st.button("📊 Resumen Diario", key="link_resumen", use_container_width=True):
    st.switch_page("pages/01_Resumen_Diario.py")

cols = st.columns(3, gap="small")
with cols[0]:
    if st.button("📈 Evolución", key="link_evo", use_container_width=True):
        st.switch_page("pages/02_Evolucion.py")
with cols[1]:
    if st.button("🥧 Distribución", key="link_dist", use_container_width=True):
        st.switch_page("pages/03_Distribucion.py")
with cols[2]:
    if st.button("📋 Datos Crudos", key="link_datos", use_container_width=True):
        st.switch_page("pages/04_Datos_Crudos.py")
