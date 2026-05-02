"""
Página: Resumen del Día
Diseño completo en 2 columnas — todo en una pantalla de celular
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

# Tabla 7 días
siete_dias = hoy - timedelta(days=7)
df_week = df[df["fecha"] >= siete_dias]
daily = df_week.groupby("fecha").sum(numeric_only=True).reset_index()
daily["fecha_str"] = daily["fecha"].apply(lambda d: d.strftime("%d/%m"))

# ─── CSS COMPACTO ────────────────────────────────────────────────
st.markdown("""
<style>
    /* Compact root */
    .block-container { padding: 0.6rem 0.8rem 0.3rem !important; max-width: 480px !important; }
    .element-container, .stMarkdown { margin-bottom: 0 !important; }
    .stApp header { display: none !important; }

    /* Global small font */
    * { font-size: 0.78rem !important; }

    /* Title bar */
    .title-row {
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 6px;
    }
    .title-row .date { font-size: 0.85rem !important; font-weight: 700; color: #eee; }
    .title-row .meals { font-size: 0.7rem !important; color: #888; }

    /* KPI badge (ultra compact) */
    .kpi {
        background: #1a1a2e; border-radius: 8px; padding: 5px 6px;
        text-align: center; border: 1px solid #2a2a4a; margin-bottom: 5px;
    }
    .kpi .v { font-size: 1rem !important; font-weight: 700; line-height: 1.2; }
    .kpi .l { font-size: 0.55rem !important; color: #888; line-height: 1; }
    .kpi .d { font-size: 0.5rem !important; line-height: 1; }
    .kpi .d.pos { color: #4ade80; }
    .kpi .d.neg { color: #f87171; }

    /* Meal card */
    .meal {
        background: #16213e; border-radius: 6px; padding: 3px 6px;
        margin-bottom: 3px; display: flex; justify-content: space-between; align-items: center;
    }
    .meal .n { font-weight: 600; font-size: 0.65rem !important; color: #ddd; }
    .meal .dsc { font-size: 0.5rem !important; color: #666; }
    .meal .mac { font-size: 0.6rem !important; text-align: right; white-space: nowrap; }

    /* 7-day table wrapper */
    .week-table table {
        font-size: 0.6rem !important;
    }
    .week-table td, .week-table th {
        padding: 2px 4px !important;
        font-size: 0.6rem !important;
    }

    /* Status row */
    .status-line {
        font-size: 0.6rem !important; color: #888; text-align: center;
        margin: 4px 0;
    }

    hr { margin: 4px 0 !important; }
    h1, h2, h3 { display: none !important; }
    .stAlert { margin-bottom: 4px !important; font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── TÍTULO ──────────────────────────────────────────────────────
st.markdown(f"""
<div class="title-row">
    <span class="date">📊 {hoy.strftime('%d %b')}</span>
    <span class="meals">{comidas_hoy} comida{"s" if comidas_hoy != 1 else ""}</span>
</div>
""", unsafe_allow_html=True)

# ─── GRILLA 2 COLUMNAS PRINCIPAL ─────────────────────────────────
c_left, c_right = st.columns(2, gap="small")

with c_left:
    # Fila 1: Calorías
    delta_cal = cal - meta['calorias']
    cls = "pos" if delta_cal >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="l">🔥 Calorías</div>
        <div class="v">{cal:.0f}</div>
        <div class="d {cls}">{'+' if delta_cal >= 0 else ''}{delta_cal:.0f} / {meta['calorias']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Comidas del día
    if comidas_hoy > 0:
        st.markdown('<div class="status-line">🥘 Comidas</div>', unsafe_allow_html=True)
        for _, row in df_hoy.iterrows():
            rcal = row.get('calorias', 0)
            rpro = row.get('proteina', 0)
            rcar = row.get('carbos', 0)
            rgra = row.get('grasas', 0)
            desc = row.get('descripcion', '')
            st.markdown(f"""
            <div class="meal">
                <div>
                    <div class="n">{row['comida']}</div>
                    <div class="dsc">{desc[:35]}{'…' if len(desc) > 35 else ''}</div>
                </div>
                <div class="mac">🔥{rcal:.0f} 💪{rpro:.0f} 🌾{rcar:.0f} 🧈{rgra:.0f}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("🥗 Sin registros hoy")

with c_right:
    # Proteína
    delta_pro = pro - meta['proteina']
    cls = "pos" if delta_pro >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="l">💪 Proteína</div>
        <div class="v">{pro:.0f}g</div>
        <div class="d {cls}">{'+' if delta_pro >= 0 else ''}{delta_pro:.0f} / {meta['proteina']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Carbohidratos
    delta_car = car - meta['carbos']
    cls = "pos" if delta_car >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="l">🌾 Carbohidratos</div>
        <div class="v">{car:.0f}g</div>
        <div class="d {cls}">{'+' if delta_car >= 0 else ''}{delta_car:.0f} / {meta['carbos']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Grasas
    delta_gra = gra - meta['grasas']
    cls = "pos" if delta_gra >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="l">🧈 Grasas</div>
        <div class="v">{gra:.0f}g</div>
        <div class="d {cls}">{'+' if delta_gra >= 0 else ''}{delta_gra:.0f} / {meta['grasas']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

    # Fibra
    delta_fib = fib - meta['fibra']
    cls = "pos" if delta_fib >= 0 else "neg"
    st.markdown(f"""
    <div class="kpi">
        <div class="l">🧵 Fibra</div>
        <div class="v">{fib:.0f}g</div>
        <div class="d {cls}">{'+' if delta_fib >= 0 else ''}{delta_fib:.0f} / {meta['fibra']:.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# ─── ÚLTIMOS 7 DÍAS (ancho completo debajo de las columnas) ─────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="status-line">📅 Últimos 7 días</div>', unsafe_allow_html=True)

daily_display = daily.rename(columns={
    "fecha_str": "D", "calorias": "🔥", "proteina": "💪",
    "carbos": "🌾", "grasas": "🧈", "fibra": "🧵"
})
cols_order = [c for c in ["D", "🔥", "💪", "🌾", "🧈", "🧵"] if c in daily_display.columns]
daily_display = daily_display[cols_order]
st.dataframe(daily_display, use_container_width=True, hide_index=True, height=120)
