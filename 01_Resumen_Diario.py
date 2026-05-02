"""
Página: Resumen del Día
Muestra los macros del día actual vs metas
Diseño compacto 2 columnas, optimizado para móvil
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date, timedelta
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date
from config import METAS_MENSUALES

st.set_page_config(page_title="Resumen Diario", page_icon="📊", layout="wide")

# Zona horaria CDMX
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

# CSS compacto para móvil
st.markdown("""
<style>
    /* Compactar todo */
    .block-container { padding-top: 1rem !important; padding-bottom: 0.5rem !important; }
    .element-container { margin-bottom: 0 !important; }
    div[data-testid="column"] > div { padding: 0 2px !important; }

    /* Tarjetas métricas compactas */
    .kpi-card {
        background: #1a1a2e;
        border-radius: 10px;
        padding: 6px 10px;
        margin-bottom: 6px;
        text-align: center;
        border: 1px solid #2a2a4a;
    }
    .kpi-card .emoji { font-size: 1.1rem; }
    .kpi-card .label { font-size: 0.65rem; color: #888; margin: 0; line-height: 1.2; }
    .kpi-card .value { font-size: 1.15rem; font-weight: 700; margin: 0; line-height: 1.3; }
    .kpi-card .delta { font-size: 0.6rem; margin: 0; line-height: 1.1; }
    .kpi-card .delta.pos { color: #4ade80; }
    .kpi-card .delta.neg { color: #f87171; }
    .kpi-card .delta.ok { color: #888; }

    /* Título comprimido */
    h1 { font-size: 1.2rem !important; margin-bottom: 6px !important; padding-bottom: 0 !important; }

    /* Info de comidas */
    .meal-row {
        display: flex;
        justify-content: space-between;
        background: #16213e;
        border-radius: 8px;
        padding: 5px 10px;
        margin-bottom: 4px;
        font-size: 0.7rem;
    }
    .meal-row .meal-name { font-weight: 600; color: #ddd; }
    .meal-row .meal-cal { color: #facc15; }
    .meal-row .meal-p { color: #60a5fa; }
    .meal-row .meal-c { color: #fb923c; }
    .meal-row .meal-f { color: #f472b6; }
    .meal-row .meal-desc { font-size: 0.6rem; color: #888; }

    .section-title { font-size: 0.75rem; font-weight: 600; color: #aaa; margin: 8px 0 4px 0 !important; padding: 0 !important; text-transform: uppercase; letter-spacing: 0.5px; }

    /* Ocultar divider */
    hr { margin: 6px 0 !important; }
</style>
""", unsafe_allow_html=True)

# === TÍTULO COMPACTO ===
st.markdown(f"<h1>📊 {hoy.strftime('%d %b %Y')}</h1>", unsafe_allow_html=True)

# === FILA 1: CALORÍAS + PROTEÍNA ===
c1, c2 = st.columns(2)
with c1:
    delta_cal = cal - meta['calorias']
    cls = "pos" if delta_cal >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="emoji">🔥</div>
        <div class="label">Calorías</div>
        <div class="value">{cal:.0f} <span style="font-size:0.7rem;color:#888">/ {meta['calorias']:.0f}</span></div>
        <div class="delta {cls}">{'+' if delta_cal >= 0 else ''}{delta_cal:.0f} vs meta</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    delta_pro = pro - meta['proteina']
    cls = "pos" if delta_pro >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="emoji">💪</div>
        <div class="label">Proteína</div>
        <div class="value">{pro:.0f} <span style="font-size:0.7rem;color:#888">/ {meta['proteina']:.0f}g</span></div>
        <div class="delta {cls}">{'+' if delta_pro >= 0 else ''}{delta_pro:.0f}g vs meta</div>
    </div>
    """, unsafe_allow_html=True)

# === FILA 2: CARBOHIDRATOS + GRASAS ===
c1, c2 = st.columns(2)
with c1:
    delta_car = car - meta['carbos']
    cls = "pos" if delta_car >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="emoji">🌾</div>
        <div class="label">Carbohidratos</div>
        <div class="value">{car:.0f} <span style="font-size:0.7rem;color:#888">/ {meta['carbos']:.0f}g</span></div>
        <div class="delta {cls}">{'+' if delta_car >= 0 else ''}{delta_car:.0f}g vs meta</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    delta_gra = gra - meta['grasas']
    cls = "pos" if delta_gra >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="emoji">🧈</div>
        <div class="label">Grasas</div>
        <div class="value">{gra:.0f} <span style="font-size:0.7rem;color:#888">/ {meta['grasas']:.0f}g</span></div>
        <div class="delta {cls}">{'+' if delta_gra >= 0 else ''}{delta_gra:.0f}g vs meta</div>
    </div>
    """, unsafe_allow_html=True)

# === FILA 3: FIBRA (sola, centrada) ===
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    delta_fib = fib - meta['fibra']
    cls = "pos" if delta_fib >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi-card">
        <div class="emoji">🧵</div>
        <div class="label">Fibra</div>
        <div class="value">{fib:.0f} <span style="font-size:0.7rem;color:#888">/ {meta['fibra']:.0f}g</span></div>
        <div class="delta {cls}">{'+' if delta_fib >= 0 else ''}{delta_fib:.0f}g vs meta</div>
    </div>
    """, unsafe_allow_html=True)

# === COMIDAS DEL DÍA ===
if comidas_hoy > 0:
    st.markdown(f'<div class="section-title">🥘 Comidas ({comidas_hoy})</div>', unsafe_allow_html=True)
    for _, row in df_hoy.iterrows():
        nombre = row['comida']
        desc = row.get('descripcion', '')
        rcal = row.get('calorias', 0)
        rpro = row.get('proteina', 0)
        rcar = row.get('carbos', 0)
        rgra = row.get('grasas', 0)
        st.markdown(f"""
        <div class="meal-row">
            <div>
                <div class="meal-name">{nombre}</div>
                <div class="meal-desc">{desc[:50]}{'...' if len(desc) > 50 else ''}</div>
            </div>
            <div style="text-align:right">
                <span class="meal-cal">🔥{rcal:.0f}</span>
                <span class="meal-p"> 💪{rpro:.0f}</span>
                <span class="meal-c"> 🌾{rcar:.0f}</span>
                <span class="meal-f"> 🧈{rgra:.0f}</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("🥗 Aún sin registros hoy")

# === ÚLTIMOS 7 DÍAS (compacto) ===
st.markdown('<div class="section-title">📅 Últimos 7 días</div>', unsafe_allow_html=True)
siete_dias = hoy - timedelta(days=7)
df_week = df[df["fecha"] >= siete_dias]
daily = df_week.groupby("fecha").sum(numeric_only=True).reset_index()
daily["fecha"] = daily["fecha"].apply(lambda d: d.strftime("%d/%m"))
daily = daily.rename(columns={
    "fecha": "Día", "calorias": "🔥Cal", "proteina": "💪Prot",
    "carbos": "🌾Carb", "grasas": "🧈Gras", "fibra": "🧵Fib"
})
st.dataframe(daily, use_container_width=True, hide_index=True, height=180)
