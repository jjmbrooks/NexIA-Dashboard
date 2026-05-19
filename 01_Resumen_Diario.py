"""
Página: Resumen del Día
KPIs con barras de progreso, comidas del día, resumen semanal profesional
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date, get_current_goals
from config import MACRO_COLORS, MACRO_UNITS, MACRO_EMOJIS

st.set_page_config(page_title="NutriFlow · Hoy", page_icon="🥗", layout="wide")

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()
mes_actual = ahora.strftime("%B")
m_esp = {"January": "Enero", "February": "Febrero", "March": "Marzo",
         "April": "Abril", "May": "Mayo", "June": "Junio",
         "July": "Julio", "August": "Agosto", "September": "Septiembre",
         "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
mes_esp = m_esp.get(mes_actual, mes_actual)

DIAS = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}

# ─── Global CSS ───────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding: 1.2rem 1.5rem !important; max-width: 900px !important; }
    .page-title { font-size: 1.3rem; font-weight: 700; color: #e0e0ff; margin-bottom: 0.1rem; }
    .page-subtitle { font-size: 0.8rem; color: #6b6b8d; margin-bottom: 1rem; }
    
    .meta-badge {
        display: inline-block; background: #1a1a3e; border-radius: 20px;
        padding: 0.2rem 0.8rem; font-size: 0.7rem; color: #818cf8;
        border: 1px solid #2d2d5e; margin-bottom: 1rem;
        text-align: center;
    }
    
    .kpi-card {
        background: linear-gradient(135deg, #12122a 0%, #1a1a3e 100%);
        border-radius: 16px; padding: 1rem 0.8rem; text-align: center;
        border: 1px solid #2a2a5e; position: relative; overflow: hidden;
    }
    .kpi-card .emoji { font-size: 1.5rem; }
    .kpi-card .label { font-size: 0.7rem; color: #888; margin-top: 0.1rem; letter-spacing: 0.5px; text-transform: uppercase; }
    .kpi-card .value { font-size: 2rem; font-weight: 800; line-height: 1.1; margin: 0.2rem 0; }
    .kpi-card .value-unit { font-size: 0.8rem; font-weight: 400; color: #6b6b8d; }
    .kpi-card .goal-line { font-size: 0.65rem; color: #555; margin-bottom: 0.3rem; }
    .kpi-card .progress-track {
        background: #0a0a1e; border-radius: 6px; height: 6px;
        margin: 0.3rem 0; overflow: hidden;
    }
    .kpi-card .progress-bar {
        height: 6px; border-radius: 6px; transition: width 0.5s;
    }
    .kpi-card .delta { font-size: 0.7rem; font-weight: 600; margin-top: 0.2rem; }
    .delta-ok { color: #22c55e; }
    .delta-warn { color: #facc15; }
    .delta-over { color: #ef4444; }
    
    .section-title { font-size: 0.9rem; font-weight: 600; color: #aaa; margin: 1.2rem 0 0.5rem 0; letter-spacing: 0.5px; }
    .section-divider { margin: 0.8rem 0; border: none; height: 1px; background: linear-gradient(90deg, transparent, #2a2a5e, transparent); }
    
    .meal-card {
        background: #12122a; border-radius: 12px; padding: 0.7rem 0.9rem;
        margin-bottom: 0.4rem; border: 1px solid #1e1e4a;
        transition: border-color 0.2s;
    }
    .meal-card:hover { border-color: #3a3a7e; }
    .meal-name { font-weight: 600; font-size: 0.85rem; color: #ddd; }
    .meal-desc { font-size: 0.7rem; color: #666; margin-top: 0.1rem; }
    .meal-macro { font-size: 0.7rem; color: #aaa; white-space: nowrap; text-align: right; }
    .meal-time { font-size: 0.65rem; color: #444; }
    
    .week-table { width: 100%; border-collapse: collapse; font-size: 0.75rem; margin-top: 0.3rem; }
    .week-table th { color: #6b6b8d; font-weight: 600; padding: 0.4rem 0.5rem; text-align: center; border-bottom: 1px solid #2a2a5e; font-size: 0.65rem; text-transform: uppercase; letter-spacing: 0.5px; }
    .week-table td { padding: 0.4rem 0.5rem; text-align: center; border-bottom: 1px solid #1a1a3e; }
    .week-table tr:hover td { background: rgba(99, 102, 241, 0.05); }
    .week-table .today td { color: #818cf8; font-weight: 600; }
    .week-table .today td:first-child { color: #facc15; }
    .stAlert, .stSpinner { font-size: 0.8rem !important; }
</style>
""", unsafe_allow_html=True)

# ─── Carga de datos ─────────────────────────────────────
with st.spinner("Cargando datos..."):
    records = load_food_data()

if not records:
    st.error("No se pudieron cargar los datos del sheet.")
    st.stop()

meta = get_current_goals()
meta_label = f"Meta {mes_esp}: {meta.get('calorias', '?')} kcal"
meta_label += f" · P{meta.get('proteina', '?')}g / C{meta.get('carbos', '?')}g / G{meta.get('grasas', '?')}g"

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

# Últimos 7 días
siete_dias = hoy - timedelta(days=7)
df_week = df[df["fecha"] >= siete_dias]
daily = df_week.groupby("fecha").sum(numeric_only=True).reset_index()
daily["etiqueta"] = daily["fecha"].apply(lambda d: DIAS[d.weekday()])
daily = daily.sort_values("fecha")

# ==================================================================
# ENCABEZADO
# ==================================================================
col_head, col_badge = st.columns([0.7, 0.3])
with col_head:
    st.markdown(f'<div class="page-title">🥗 NutriFlow</div>', unsafe_allow_html=True)
DIAS_NOMBRE = {0: "lunes", 1: "martes", 2: "miércoles", 3: "jueves", 4: "viernes", 5: "sábado", 6: "domingo"}
MESES = {1: "enero", 2: "febrero", 3: "marzo", 4: "abril", 5: "mayo", 6: "junio",
         7: "julio", 8: "agosto", 9: "septiembre", 10: "octubre", 11: "noviembre", 12: "diciembre"}
dia_nombre = DIAS_NOMBRE.get(hoy.weekday(), "")
mes_nombre = MESES.get(hoy.month, "")
st.markdown(f'<div class="page-subtitle">{dia_nombre}, {hoy.day} de {mes_nombre} de {hoy.year}</div>', unsafe_allow_html=True)
with col_badge:
    st.markdown(f'<div class="meta-badge">{meta_label}</div>', unsafe_allow_html=True)

# ==================================================================
# KPIS EN GRID 3+2
# ==================================================================
def render_kpi(emoji, label, value, goal, unit, color):
    pct = min(value / goal * 100, 100) if goal > 0 else 0
    delta = value - goal
    if delta <= 0:
        cls = "delta-ok"
        sign = ""
    elif delta <= goal * 0.1:
        cls = "delta-warn"
        sign = "+"
    else:
        cls = "delta-over"
        sign = "+"
    return f"""
    <div class="kpi-card">
        <div class="emoji">{emoji}</div>
        <div class="label">{label}</div>
        <div class="value">{value:.0f}<span class="value-unit">/{goal:.0f}{unit}</span></div>
        <div class="progress-track"><div class="progress-bar" style="width:{pct}%;background:{color};"></div></div>
        <div class="delta {cls}">{sign}{delta:.0f}{unit}</div>
    </div>"""

# Row 1: 3 KPIs (calorías, proteína, carbos)
cols = st.columns(3, gap="small")
KPIS = [
    ("🔥", "Calorías", cal, meta.get("calorias", 2000), "kcal", MACRO_COLORS["calorias"]),
    ("💪", "Proteína", pro, meta.get("proteina", 90), "g", MACRO_COLORS["proteina"]),
    ("🌾", "Carbohidratos", car, meta.get("carbos", 250), "g", MACRO_COLORS["carbos"]),
]
for i, (emoji, label, val, goal, unit, color) in enumerate(KPIS):
    with cols[i]:
        st.markdown(render_kpi(emoji, label, val, goal, unit, color), unsafe_allow_html=True)

# Row 2: 2 KPIs (grasas, fibra)
cols2 = st.columns(2, gap="small")
KPIS2 = [
    ("🧈", "Grasas", gra, meta.get("grasas", 48), "g", MACRO_COLORS["grasas"]),
    ("🧵", "Fibra", fib, meta.get("fibra", 25), "g", MACRO_COLORS["fibra"]),
]
for i, (emoji, label, val, goal, unit, color) in enumerate(KPIS2):
    with cols2[i]:
        st.markdown(render_kpi(emoji, label, val, goal, unit, color), unsafe_allow_html=True)

# ==================================================================
# COMIDAS DEL DÍA
# ==================================================================
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)

if comidas_hoy > 0:
    st.markdown(f'<div class="section-title">🥘 Comidas de hoy ({comidas_hoy})</div>', unsafe_allow_html=True)
    for _, row in df_hoy.iterrows():
        rcal = row.get('calorias', 0)
        rpro = row.get('proteina', 0)
        rcar = row.get('carbos', 0)
        rgra = row.get('grasas', 0)
        desc = row.get('descripcion', '')
        comida = row.get('comida', '')
        hora = row.get('fecha_hora', '')[-5:] if len(row.get('fecha_hora', '')) >= 5 else ''

        st.markdown(f"""
        <div class="meal-card">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div style="flex:1;">
                    <div class="meal-name">{comida}</div>
                    <div class="meal-desc">{desc[:80]}{'…' if len(desc) > 80 else ''}</div>
                    <div class="meal-time">{hora}</div>
                </div>
                <div class="meal-macro">
                    🔥{rcal:.0f}  💪{rpro:.0f}g  🌾{rcar:.0f}g  🧈{rgra:.0f}g
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("🥗 Aún sin registros hoy")

# ==================================================================
# RESUMEN SEMANAL
# ==================================================================
st.markdown('<hr class="section-divider">', unsafe_allow_html=True)
st.markdown(f'<div class="section-title">📅 Últimos 7 días</div>', unsafe_allow_html=True)

if not daily.empty:
    rows_html = ""
    for _, r in daily.iterrows():
        es_hoy = r["fecha"] == hoy
        cls = 'class="today"' if es_hoy else ""
        rows_html += f"""<tr {cls}>
            <td>{r['etiqueta']}</td>
            <td>{r['calorias']:.0f}</td>
            <td>{r['proteina']:.0f}</td>
            <td>{r['carbos']:.0f}</td>
            <td>{r['grasas']:.0f}</td>
            <td>{r['fibra']:.0f}</td>
        </tr>"""

    st.markdown(f"""
    <table class="week-table">
        <tr><th>Día</th><th>🔥kcal</th><th>💪P</th><th>🌾C</th><th>🧈G</th><th>🧵F</th></tr>
        {rows_html}
    </table>
    """, unsafe_allow_html=True)

    # Promedio semanal
    avg = daily.mean(numeric_only=True)
    meta_cal = meta.get("calorias", 0)
    avg_cal_pct = avg.get('calorias', 0) / meta_cal * 100 if meta_cal > 0 else 0
    cal_status = "✅" if avg_cal_pct <= 100 else "⚠️"
    
    st.caption(f"📊 Promedio semanal: {avg.get('calorias', 0):.0f} kcal/día ({avg_cal_pct:.0f}% de meta {cal_status}) · "
               f"P{avg.get('proteina', 0):.0f}g · C{avg.get('carbos', 0):.0f}g · G{avg.get('grasas', 0):.0f}g")
else:
    st.caption("Sin datos en los últimos 7 días")
