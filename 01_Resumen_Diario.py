"""
Página: Resumen del Día
Solo macros: 5 KPIs en 2 columnas, una pantalla de celular
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date
from config import METAS_MENSUALES

st.set_page_config(page_title="Resumen Diario", page_icon="📊", layout="wide")

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()

mes_actual = ahora.strftime("%B")
mes_esp = {"January": "Enero", "February": "Febrero", "March": "Marzo",
           "April": "Abril", "May": "Mayo", "June": "Junio",
           "July": "Julio", "August": "Agosto", "September": "Septiembre",
           "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}.get(mes_actual, mes_actual)
meta = METAS_MENSUALES.get(mes_esp, METAS_MENSUALES["Abril"])

with st.spinner("Cargando datos..."):
    records = load_food_data()

if not records:
    st.error("No se pudieron cargar los datos.")
    st.stop()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

df_hoy = df[df["fecha"] == hoy]
comidas_hoy = len(df_hoy)
sum_hoy = df_hoy.sum(numeric_only=True)
cal = sum_hoy.get('calorias', 0)
pro = sum_hoy.get('proteina', 0)
car = sum_hoy.get('carbos', 0)
gra = sum_hoy.get('grasas', 0)
fib = sum_hoy.get('fibra', 0)

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding: 0.8rem 1rem 0.4rem !important; max-width: 480px !important; }
    .element-container { margin-bottom: 0 !important; }

    /* Fecha arriba */
    .fecha { font-size: 0.85rem; color: #aaa; text-align: center; margin-bottom: 6px; font-weight: 500; }
    .fecha span { color: #facc15; font-weight: 700; }

    /* Tarjeta KPI */
    .kpi {
        background: #1a1a2e; border-radius: 14px; padding: 10px 6px;
        text-align: center; border: 1px solid #2a2a4a; margin-bottom: 8px;
    }
    .kpi .emoji { font-size: 1.4rem; line-height: 1; }
    .kpi .label { font-size: 0.7rem; color: #888; margin-top: 1px; }
    .kpi .valor { font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin: 2px 0; }
    .kpi .valor span { font-size: 0.75rem; font-weight: 400; color: #666; }
    .kpi .delta { font-size: 0.6rem; line-height: 1; }
    .kpi .delta.pos { color: #4ade80; }
    .kpi .delta.neg { color: #f87171; }
    .kpi .delta.meta { color: #888; }

    .stAlert { margin-bottom: 4px !important; font-size: 0.75rem !important; }
    hr { display: none !important; }
    h1 { display: none !important; }
    #ocultar { display: none; }
</style>
""", unsafe_allow_html=True)

# ─── FECHA ───────────────────────────────────────────────────────
comidas_text = f"{comidas_hoy} comida{'s' if comidas_hoy != 1 else ''}" if comidas_hoy > 0 else "Sin registros"
st.markdown(f'<div class="fecha">📊 <span>{hoy.strftime("%d %B %Y")}</span> · {comidas_text}</div>', unsafe_allow_html=True)

# ─── FILA 1: 🔥 CALORÍAS | 💪 PROTEÍNA ─────────────────────────
c1, c2 = st.columns(2, gap="small")

with c1:
    d = cal - meta['calorias']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="emoji">🔥</div>
        <div class="label">Calorías</div>
        <div class="valor">{cal:.0f}<span> / {meta['calorias']:.0f}</span></div>
        <div class="delta {cls}">{'+' if d >= 0 else ''}{d:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    d = pro - meta['proteina']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="emoji">💪</div>
        <div class="label">Proteína</div>
        <div class="valor">{pro:.0f}<span>g / {meta['proteina']:.0f}</span></div>
        <div class="delta {cls}">{'+' if d >= 0 else ''}{d:.0f}g</div>
    </div>
    """, unsafe_allow_html=True)

# ─── FILA 2: 🌾 CARBOHIDRATOS | 🧈 GRASAS ──────────────────────
c1, c2 = st.columns(2, gap="small")

with c1:
    d = car - meta['carbos']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="emoji">🌾</div>
        <div class="label">Carbohidratos</div>
        <div class="valor">{car:.0f}<span>g / {meta['carbos']:.0f}</span></div>
        <div class="delta {cls}">{'+' if d >= 0 else ''}{d:.0f}g</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    d = gra - meta['grasas']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="emoji">🧈</div>
        <div class="label">Grasas</div>
        <div class="valor">{gra:.0f}<span>g / {meta['grasas']:.0f}</span></div>
        <div class="delta {cls}">{'+' if d >= 0 else ''}{d:.0f}g</div>
    </div>
    """, unsafe_allow_html=True)

# ─── FILA 3: 🧵 FIBRA (centrada, ocupa las 2 columnas) ────────
st.markdown("""<div id="ocultar"></div>""", unsafe_allow_html=True)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    d = fib - meta['fibra']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="emoji">🧵</div>
        <div class="label">Fibra</div>
        <div class="valor">{fib:.0f}<span>g / {meta['fibra']:.0f}</span></div>
        <div class="delta {cls}">{'+' if d >= 0 else ''}{d:.0f}g</div>
    </div>
    """, unsafe_allow_html=True)
