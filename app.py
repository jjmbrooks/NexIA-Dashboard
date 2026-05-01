"""
NexIA Dashboard — Inicio
Pantalla principal con tarjetas de todos los proyectos
"""
import streamlit as st

st.set_page_config(
    page_title="NexIA Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Estilo personalizado ──────────────────────────────────────
st.markdown("""
<style>
    .proyecto-card {
        background: #1a1c2e;
        border: 1px solid #2a2d4e;
        border-radius: 16px;
        padding: 1.8rem 1.5rem;
        text-align: center;
        transition: all 0.25s ease;
        cursor: default;
    }
    .proyecto-card:hover {
        border-color: #6366f1;
        box-shadow: 0 4px 24px rgba(99, 102, 241, 0.15);
        transform: translateY(-3px);
    }
    .proyecto-icon {
        font-size: 2.8rem;
        margin-bottom: 0.4rem;
    }
    .proyecto-nombre {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e0e0ff;
        margin-bottom: 0.3rem;
    }
    .proyecto-estado {
        font-size: 0.8rem;
        color: #8888aa;
        border-radius: 20px;
        display: inline-block;
        padding: 0.2rem 0.8rem;
    }
    .estado-activo {
        background: #1a3a2a;
        color: #4ade80;
    }
    .estado-proximo {
        background: #2a2a1a;
        color: #facc15;
    }
    .estado-planeado {
        background: #2a1a2a;
        color: #c084fc;
    }
</style>
""", unsafe_allow_html=True)

# ── Encabezado ────────────────────────────────────────────────
st.title("🧠 NexIA Dashboard")
st.caption("Centro de monitoreo inteligente — Brooks · 2026")

# ── Proyectos ─────────────────────────────────────────────────
proyectos = [
    {
        "icon": "🥗",
        "nombre": "Body Lab",
        "descripcion": "Rendimiento físico, entrenamiento y composición corporal",
        "estado": "Próximamente",
        "estado_cls": "estado-proximo",
    },
    {
        "icon": "🏋️",
        "nombre": "Hábitos",
        "descripcion": "Seguimiento de hábitos diarios y consistencia",
        "estado": "Próximamente",
        "estado_cls": "estado-proximo",
    },
    {
        "icon": "🥗",
        "nombre": "NutriFlow",
        "descripcion": "Registro de alimentación, macros y metas nutricionales",
        "estado": "Activo",
        "estado_cls": "estado-activo",
    },
]

# Orden alfabético
proyectos.sort(key=lambda p: p["nombre"])

# Grid de tarjetas
cols = st.columns(len(proyectos), gap="medium")

for col, p in zip(cols, proyectos):
    with col:
        st.markdown(f"""
        <div class="proyecto-card">
            <div class="proyecto-icon">{p['icon']}</div>
            <div class="proyecto-nombre">{p['nombre']}</div>
            <div style="font-size:0.85rem;color:#aaaacc;margin-bottom:0.6rem;">
                {p['descripcion']}
            </div>
            <span class="proyecto-estado {p['estado_cls']}">{p['estado']}</span>
        </div>
        """, unsafe_allow_html=True)

st.divider()

st.markdown("""
**Selecciona un proyecto en el menú lateral** para explorar sus módulos.

- 🥗 **NutriFlow** — Resumen Diario, Evolución, Distribución, Datos Crudos
- 🏋️ **Body Lab** — *Próximamente*
- ✅ **Hábitos** — *Próximamente*
""")
