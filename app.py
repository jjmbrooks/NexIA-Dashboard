"""
NexIA Dashboard — Inicio
Pantalla principal con tarjetas de proyectos clickeables
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

# ── CSS personalizado para tarjetas tipo link ─────────────────
st.markdown("""
<style>
    /* Tarjeta link inline — reemplaza st.page_link */
    .card-link {
        display: block;
        background: #1a1c2e;
        border: 1px solid #2a2d4e;
        border-radius: 16px;
        padding: 2rem 1rem;
        text-align: center;
        text-decoration: none !important;
        transition: all 0.25s ease;
        margin-bottom: 0.5rem;
        cursor: pointer;
        color: inherit;
    }
    .card-link:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.2);
        transform: translateY(-4px);
    }
    .card-link.activa {
        border-color: #4ade80;
    }
    .card-link.activa:hover {
        border-color: #6366f1 !important;
    }
    .card-icon { font-size: 3rem; display: block; margin-bottom: 0.3rem; }
    .card-nombre { font-size: 1.2rem; font-weight: 700; color: #e0e0ff; display: block; margin-bottom: 0.3rem; }
    .card-desc { font-size: 0.8rem; color: #999abb; display: block; margin-bottom: 0.6rem; line-height: 1.3; }
    .badge {
        display: inline-block;
        border-radius: 20px;
        padding: 0.2rem 0.9rem;
        font-size: 0.75rem;
        font-weight: 600;
    }
    .badge-ok { background: #1a3a2a; color: #4ade80; }
    .badge-wait { background: #2a2a1a; color: #facc15; }

    /* Seccion de links rapidos */
    .quick-link {
        margin: 0.3rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.divider()

# ── Tarjetas como page_links ──────────────────────────────────
# Streamlit no deja customizar el HTML de page_link,
# asi que usamos page_link con etiqueta descriptiva.

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.page_link(
        "pages/01_Resumen_Diario.py",
        label="🏋️ Body Lab",
        help="Rendimiento físico, entrenamiento y composición corporal — Próximamente",
        disabled=True,
        use_container_width=True,
    )

with col2:
    st.page_link(
        "pages/01_Resumen_Diario.py",
        label="✅ Hábitos",
        help="Seguimiento de hábitos diarios y consistencia — Próximamente",
        disabled=True,
        use_container_width=True,
    )

with col3:
    st.page_link(
        "pages/01_Resumen_Diario.py",
        label="🥗 NutriFlow",
        help="Registro de alimentación, macros y metas nutricionales — Activo",
        use_container_width=True,
    )

st.divider()

# ── Links rápidos a módulos de NutriFlow ──────────────────────
st.subheader("🥗 NutriFlow — módulos")

cols = st.columns(4, gap="small")
with cols[0]:
    st.page_link("pages/01_Resumen_Diario.py", label="📊 Resumen Diario", use_container_width=True)
with cols[1]:
    st.page_link("pages/02_Evolucion.py", label="📈 Evolución", use_container_width=True)
with cols[2]:
    st.page_link("pages/03_Distribucion.py", label="🥧 Distribución", use_container_width=True)
with cols[3]:
    st.page_link("pages/04_Datos_Crudos.py", label="📋 Datos Crudos", use_container_width=True)
