"""
NEXIA DASHBOARD — Inicio
Landing profesional con resumen general
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date, get_current_goals
from bodylab_data import load_activity_data, load_weight_data

st.set_page_config(page_title="NEXIA DASHBOARD", page_icon="🧠", layout="wide")

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()

st.markdown("""
<style>
    .block-container { padding: 1.5rem 2rem !important; max-width: 1000px !important; }
    .hero-title { font-size: 1.8rem; font-weight: 800; background: linear-gradient(135deg, #818cf8, #6366f1); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 0.2rem; }
    .hero-sub { font-size: 0.85rem; color: #6b6b8d; margin-bottom: 1.5rem; }
    .module-card {
        background: linear-gradient(135deg, #12122a 0%, #1a1a3e 100%);
        border-radius: 16px; padding: 1.2rem; text-align: center;
        border: 1px solid #2a2a5e; transition: all 0.3s;
        height: 100%;
    }
    .module-card:hover { border-color: #6366f1; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(99,102,241,0.1); }
    .module-card .icon { font-size: 2rem; }
    .module-card .name { font-size: 1rem; font-weight: 700; color: #e0e0ff; margin: 0.5rem 0 0.2rem 0; }
    .module-card .desc { font-size: 0.75rem; color: #888; margin-bottom: 0.8rem; }
    .mini-stat {
        background: #0a0a1e; border-radius: 10px; padding: 0.6rem;
        margin-top: 0.5rem;
    }
    .mini-stat .val { font-size: 1.2rem; font-weight: 700; color: #d0d0f0; }
    .mini-stat .lb { font-size: 0.6rem; color: #555; text-transform: uppercase; letter-spacing: 0.5px; }
    .dashboard-link { text-decoration: none; }
    .divider { margin: 1.5rem 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #2a2a5e, transparent); }
    .welcome { font-size: 0.9rem; color: #aaa; margin-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────
st.markdown(f'<div class="hero-title">🧠 NEXIA DASHBOARD</div>', unsafe_allow_html=True)
st.markdown(f'<div class="hero-sub">Centro de monitoreo inteligente · Brooks · {hoy.strftime("%d %B %Y")}</div>', unsafe_allow_html=True)

# ─── Módulos principales ──────────────────────────────────
col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    # Cargar mini stats de NutriFlow
    try:
        nf_records = load_food_data()
        nf_df = pd.DataFrame(nf_records)
        nf_df["fecha"] = nf_df["fecha_hora"].apply(parse_date)
        nf_hoy = nf_df[nf_df["fecha"] == hoy]
        nf_cal = nf_hoy["calorias"].sum()
        meta = get_current_goals()
        nf_pct = f"{nf_cal/meta.get('calorias',1)*100:.0f}%" if meta.get('calorias',0) > 0 else "—"
    except:
        nf_cal = 0
        nf_pct = "—"
    
    st.markdown(f"""
    <a href="/01_Resumen_Diario" target="_self" class="dashboard-link">
        <div class="module-card">
            <div class="icon">🥗</div>
            <div class="name">NutriFlow</div>
            <div class="desc">Registro de alimentación y metas nutricionales</div>
            <div class="mini-stat">
                <div class="val">{nf_cal:.0f}</div>
                <div class="lb">kcal hoy · {nf_pct} de meta</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col2:
    # Mini stats Body Lab
    try:
        bl_records = load_activity_data()
        bl_df = pd.DataFrame(bl_records)
        bl_hoy = bl_df[bl_df["fecha"] == hoy] if "fecha" in bl_df.columns else pd.DataFrame()
        bl_cal = bl_hoy["calorias"].sum() if not bl_hoy.empty else 0
        bl_ej = len(bl_hoy)
        # Último peso
        try:
            w = load_weight_data()
            peso = w[-1]["peso_kg"] if w else "—"
        except:
            peso = "—"
    except:
        bl_cal = 0
        bl_ej = 0
        peso = "—"
    
    st.markdown(f"""
    <a href="/05_Resumen_BodyLab" target="_self" class="dashboard-link">
        <div class="module-card">
            <div class="icon">🏋️</div>
            <div class="name">Body Lab</div>
            <div class="desc">Rendimiento físico, peso y composición</div>
            <div class="mini-stat">
                <div class="val">{bl_cal:.0f} · {peso}</div>
                <div class="lb">kcal hoy · {bl_ej} ejercicios · peso kg</div>
            </div>
        </div>
    </a>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="module-card" style="opacity:0.5;">
        <div class="icon">✅</div>
        <div class="name">Hábitos</div>
        <div class="desc">Seguimiento de hábitos diarios y consistencia</div>
        <div class="mini-stat">
            <div class="val">🔄</div>
            <div class="lb">Próximamente</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Separador ─────────────────────────────────────────────
st.markdown('<hr class="divider">', unsafe_allow_html=True)
st.markdown('<div class="welcome">📊 Acceso rápido</div>', unsafe_allow_html=True)

# ─── Links NutriFlow ──────────────────────────────────────
st.markdown("**🥗 NutriFlow**")
nf_links = st.columns(4, gap="small")
with nf_links[0]:
    st.page_link("01_Resumen_Diario.py", label="📊 Resumen Diario", use_container_width=True)
with nf_links[1]:
    st.page_link("02_Evolucion.py", label="📈 Evolución", use_container_width=True)
with nf_links[2]:
    st.page_link("03_Distribucion.py", label="🥧 Distribución", use_container_width=True)
with nf_links[3]:
    st.page_link("04_Datos_Crudos.py", label="📋 Datos Crudos", use_container_width=True)

st.markdown("**🏋️ Body Lab**")
bl_links = st.columns(3, gap="small")
with bl_links[0]:
    st.page_link("05_Resumen_BodyLab.py", label="🏋️ Resumen Diario", use_container_width=True)
with bl_links[1]:
    st.page_link("06_Evolucion_BodyLab.py", label="📈 Evolución", use_container_width=True)
with bl_links[2]:
    st.page_link("07_Distribucion_BodyLab.py", label="🥧 Distribución", use_container_width=True)
