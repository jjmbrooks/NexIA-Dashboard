"""
Página: Resumen del Día
Arriba: 5 KPIs en 2 columnas (pantalla completa)
Abajo: comidas del día + resumen semanal con días lun-dom
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

# Días de la semana en español
DIAS_ES = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}

# Últimos 7 días con etiquetas de día
siete_dias = hoy - timedelta(days=7)
df_week = df[df["fecha"] >= siete_dias]
daily = df_week.groupby("fecha").sum(numeric_only=True).reset_index()
daily["etiqueta"] = daily["fecha"].apply(lambda d: DIAS_ES[d.weekday()])
# Ordenar cronológico
daily = daily.sort_values("fecha")

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding: 0.6rem 0.8rem 0.3rem !important; max-width: 480px !important; }
    .element-container { margin-bottom: 0 !important; }

    /* Fecha arriba */
    .fecha { font-size: 0.8rem; color: #aaa; text-align: center; margin-bottom: 5px; }
    .fecha span { color: #facc15; font-weight: 700; }

    /* Tarjeta KPI */
    .kpi {
        background: #1a1a2e; border-radius: 14px; padding: 10px 6px;
        text-align: center; border: 1px solid #2a2a4a; margin-bottom: 7px;
    }
    .kpi .emoji { font-size: 1.4rem; line-height: 1; }
    .kpi .label { font-size: 0.65rem; color: #888; margin-top: 1px; }
    .kpi .valor { font-size: 1.6rem; font-weight: 800; line-height: 1.1; margin: 1px 0; }
    .kpi .valor span { font-size: 0.75rem; font-weight: 400; color: #666; }
    .kpi .delta { font-size: 0.6rem; line-height: 1; }
    .kpi .delta.pos { color: #4ade80; }
    .kpi .delta.neg { color: #f87171; }

    /* Comidas */
    .seccion-tit { font-size: 0.75rem; font-weight: 600; color: #aaa; margin: 10px 0 4px 0; letter-spacing: 0.3px; }
    .comida {
        background: #16213e; border-radius: 8px; padding: 5px 8px;
        margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;
    }
    .comida .nom { font-weight: 600; font-size: 0.72rem; color: #ddd; }
    .comida .dsc { font-size: 0.55rem; color: #666; }
    .comida .mac { font-size: 0.6rem; text-align: right; white-space: nowrap; color: #bbb; }

    /* Tabla semanal */
    .semana-tabla { font-size: 0.65rem; width: 100%; border-collapse: collapse; margin-top: 4px; }
    .semana-tabla th { color: #888; font-weight: 600; padding: 3px 4px; text-align: center; border-bottom: 1px solid #2a2a4a; font-size: 0.6rem; }
    .semana-tabla td { padding: 3px 4px; text-align: center; border-bottom: 1px solid #1e1e3a; font-size: 0.6rem; }
    .semana-tabla tr:hover { background: #1e1e3a; }
    .semana-tabla .hoy { color: #facc15; font-weight: 700; }

    hr { margin: 4px 0 !important; border-color: #2a2a4a; }
    h1, h2, h3 { display: none !important; }
    .stAlert { margin-bottom: 4px !important; font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================================
# SECCIÓN 1: MACROS (ocupa la pantalla sin scroll)
# ==================================================================
st.markdown(f'<div class="fecha">📊 <span>{hoy.strftime("%d %B %Y")}</span></div>', unsafe_allow_html=True)

# Fila 1: Calorías | Proteína
c1, c2 = st.columns(2, gap="small")
with c1:
    d = cal - meta['calorias']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f'<div class="kpi"><div class="emoji">🔥</div><div class="label">Calorías</div><div class="valor">{cal:.0f}<span> / {meta["calorias"]:.0f}</span></div><div class="delta {cls}">{"+" if d >= 0 else ""}{d:.0f}</div></div>', unsafe_allow_html=True)
with c2:
    d = pro - meta['proteina']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f'<div class="kpi"><div class="emoji">💪</div><div class="label">Proteína</div><div class="valor">{pro:.0f}<span>g / {meta["proteina"]:.0f}</span></div><div class="delta {cls}">{"+" if d >= 0 else ""}{d:.0f}g</div></div>', unsafe_allow_html=True)

# Fila 2: Carbohidratos | Grasas
c1, c2 = st.columns(2, gap="small")
with c1:
    d = car - meta['carbos']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f'<div class="kpi"><div class="emoji">🌾</div><div class="label">Carbohidratos</div><div class="valor">{car:.0f}<span>g / {meta["carbos"]:.0f}</span></div><div class="delta {cls}">{"+" if d >= 0 else ""}{d:.0f}g</div></div>', unsafe_allow_html=True)
with c2:
    d = gra - meta['grasas']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f'<div class="kpi"><div class="emoji">🧈</div><div class="label">Grasas</div><div class="valor">{gra:.0f}<span>g / {meta["grasas"]:.0f}</span></div><div class="delta {cls}">{"+" if d >= 0 else ""}{d:.0f}g</div></div>', unsafe_allow_html=True)

# Fila 3: Fibra (centrada)
c1, c2, c3 = st.columns([1, 2, 1])
with c2:
    d = fib - meta['fibra']
    cls = "pos" if d >= 0 else "neg"
    st.markdown(f'<div class="kpi"><div class="emoji">🧵</div><div class="label">Fibra</div><div class="valor">{fib:.0f}<span>g / {meta["fibra"]:.0f}</span></div><div class="delta {cls}">{"+" if d >= 0 else ""}{d:.0f}g</div></div>', unsafe_allow_html=True)

# ==================================================================
# SECCIÓN 2: COMIDAS DEL DÍA (con scroll debajo)
# ==================================================================
if comidas_hoy > 0:
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f'<div class="seccion-tit">🥘 Comidas ({comidas_hoy})</div>', unsafe_allow_html=True)
    for _, row in df_hoy.iterrows():
        rcal = row.get('calorias', 0)
        rpro = row.get('proteina', 0)
        rcar = row.get('carbos', 0)
        rgra = row.get('grasas', 0)
        desc = row.get('descripcion', '')
        st.markdown(f"""
        <div class="comida">
            <div>
                <div class="nom">{row['comida']}</div>
                <div class="dsc">{desc[:40]}{'…' if len(desc) > 40 else ''}</div>
            </div>
            <div class="mac">🔥{rcal:.0f} 💪{rpro:.0f} 🌾{rcar:.0f} 🧈{rgra:.0f}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("🥗 Aún sin registros hoy")

# ==================================================================
# SECCIÓN 3: RESUMEN SEMANAL (con etiquetas Lun-Dom)
# ==================================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="seccion-tit">📅 Últimos 7 días</div>', unsafe_allow_html=True)

if not daily.empty:
    # Construir tabla HTML
    rows_html = ""
    for _, r in daily.iterrows():
        es_hoy = r["fecha"] == hoy
        cls_fila = 'class="hoy"' if es_hoy else ""
        rows_html += f"""<tr>
            <td {cls_fila}>{r['etiqueta']}</td>
            <td>{r['calorias']:.0f}</td>
            <td>{r['proteina']:.0f}</td>
            <td>{r['carbos']:.0f}</td>
            <td>{r['grasas']:.0f}</td>
            <td>{r['fibra']:.0f}</td>
        </tr>"""

    st.markdown(f"""
    <table class="semana-tabla">
        <tr>
            <th>Día</th><th>🔥</th><th>💪</th><th>🌾</th><th>🧈</th><th>🧵</th>
        </tr>
        {rows_html}
    </table>
    """, unsafe_allow_html=True)
else:
    st.caption("Sin datos en los últimos 7 días")
