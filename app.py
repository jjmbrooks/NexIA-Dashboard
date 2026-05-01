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
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        margin-bottom: 1rem;
    }
    .proyecto-card:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.15);
        transform: translateY(-3px);
    }
    .proyecto-icon { font-size: 2.8rem; margin-bottom: 0.4rem; }
    .proyecto-nombre { font-size: 1.2rem; font-weight: 600; color: #e0e0ff; margin-bottom: 0.3rem; }
    .proyecto-desc { font-size: 0.85rem; color: #aaaacc; margin-bottom: 0.6rem; }
    .estado-activo { background: #1a3a2a; color: #4ade80; border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.8rem; }
    .estado-proximo { background: #2a2a1a; color: #facc15; border-radius: 20px; padding: 0.2rem 0.8rem; font-size: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.divider()

# ── Tarjetas de proyectos ─────────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

proyectos = [
    {
        "nombre": "Body Lab",
        "icono": "🏋️",
        "desc": "Rendimiento físico, entrenamiento y composición corporal",
        "estado": "Próximamente",
        "estado_cls": "estado-proximo",
    },
    {
        "nombre": "Hábitos",
        "icono": "✅",
        "desc": "Seguimiento de hábitos diarios y consistencia",
        "estado": "Próximamente",
        "estado_cls": "estado-proximo",
    },
    {
        "nombre": "NutriFlow",
        "icono": "🥗",
        "desc": "Registro de alimentación, macros y metas nutricionales",
        "estado": "Activo",
        "estado_cls": "estado-activo",
    },
]

for col, p in zip([col1, col2, col3], proyectos):
    with col:
        st.markdown(f"""
        <div class="proyecto-card">
            <div class="proyecto-icon">{p['icono']}</div>
            <div class="proyecto-nombre">{p['nombre']}</div>
            <div class="proyecto-desc">{p['desc']}</div>
            <span class="{p['estado_cls']}">{p['estado']}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# ── Links rápidos a NutriFlow ─────────────────────────────────
st.subheader("🥗 NutriFlow")
st.markdown("Selecciona un módulo para explorar:")

cols = st.columns(4)
with cols[0]:
    st.page_link("pages/01_Resumen_Diario.py", label="📊 Resumen Diario", use_container_width=True)
with cols[1]:
    st.page_link("pages/02_Evolucion.py", label="📈 Evolución", use_container_width=True)
with cols[2]:
    st.page_link("pages/03_Distribucion.py", label="🥧 Distribución", use_container_width=True)
with cols[3]:
    st.page_link("pages/04_Datos_Crudos.py", label="📋 Datos Crudos", use_container_width=True)
