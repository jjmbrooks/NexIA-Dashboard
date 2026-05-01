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

st.markdown("""
<style>
    .proyecto-card {
        background: #1a1c2e;
        border: 1px solid #2a2d4e;
        border-radius: 16px;
        padding: 2rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        cursor: pointer;
        text-decoration: none !important;
        display: block;
        margin-bottom: 0.5rem;
    }
    .proyecto-card:hover {
        border-color: #6366f1 !important;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.2);
        transform: translateY(-4px);
    }
    .proyecto-card.activo {
        border-color: #4ade80;
    }
    .proyecto-card.activo:hover {
        border-color: #6366f1 !important;
    }
    .proyecto-icon { font-size: 3rem; display: block; margin-bottom: 0.4rem; }
    .proyecto-nombre { font-size: 1.2rem; font-weight: 700; color: #e0e0ff; display: block; margin-bottom: 0.3rem; }
    .proyecto-desc { font-size: 0.8rem; color: #999abb; display: block; margin-bottom: 0.6rem; line-height: 1.3; }
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
# Usamos page_link SOLO para NutriFlow (ruta real).
# Body Lab y Hábitos son HTML placeholder (no funcionales aún).

col1, col2, col3 = st.columns(3, gap="medium")

# Body Lab — HTML placeholder
with col1:
    st.markdown("""
    <div class="proyecto-card">
        <span class="proyecto-icon">🏋️</span>
        <span class="proyecto-nombre">Body Lab</span>
        <span class="proyecto-desc">Rendimiento físico, entrenamiento y composición corporal</span>
        <span class="badge badge-wait">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

# Hábitos — HTML placeholder
with col2:
    st.markdown("""
    <div class="proyecto-card">
        <span class="proyecto-icon">✅</span>
        <span class="proyecto-nombre">Hábitos</span>
        <span class="proyecto-desc">Seguimiento de hábitos diarios y consistencia</span>
        <span class="badge badge-wait">Próximamente</span>
    </div>
    """, unsafe_allow_html=True)

# NutriFlow — page_link funcional
with col3:
    st.page_link(
        "pages/01_Resumen_Diario.py",
        label="🥗 NutriFlow — Activo",
        help="Registro de alimentación, macros y metas nutricionales. Haz clic para abrir.",
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
