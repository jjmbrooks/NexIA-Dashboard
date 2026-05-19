"""
Página: Evolución Temporal
Gráficos de línea con consumo diario y medias móviles, metas dinámicas desde el sheet
"""
import streamlit as st
import pandas as pd
from datetime import datetime
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date, load_goals
from config import MACRO_COLORS, MACRO_LABELS, MACRO_UNITS
from charts import line_chart

st.set_page_config(page_title="NutriFlow · Evolución", page_icon="📈", layout="wide")

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)

# Cargar datos
with st.spinner("Cargando datos..."):
    records = load_food_data()

if not records:
    st.error("No se pudieron cargar los datos.")
    st.stop()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

# Agrupar por día
daily = df.groupby("fecha").sum(numeric_only=True).reset_index()
daily = daily.sort_values("fecha")

# Selector de mes
mes_actual = ahora.strftime("%B")
mapeo = {"January": "Enero", "February": "Febrero", "March": "Marzo",
         "April": "Abril", "May": "Mayo", "June": "Junio",
         "July": "Julio", "August": "Agosto", "September": "Septiembre",
         "October": "Octubre", "November": "Noviembre", "December": "Diciembre"}
mes_esp = mapeo.get(mes_actual, mes_actual)

# Cargar metas desde el sheet
all_goals = load_goals()
meses_disponibles = sorted(all_goals.keys(), key=lambda m: list(mapeo.values()).index(m) if m in mapeo.values() else 99)

opciones_mes = [f"{m} 2026" for m in meses_disponibles]
opciones_mes.append("Todo")

mes_idx = 0
for i, opt in enumerate(opciones_mes):
    if mes_esp in opt:
        mes_idx = i
        break

mes = st.selectbox("Periodo", opciones_mes, index=mes_idx)

# CSS compacto
st.markdown("""
<style>
    .block-container { padding: 1.2rem 1.5rem !important; max-width: 1100px !important; }
    h1 { font-size: 1.3rem !important; margin-bottom: 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("📈 Evolución Temporal")

# Filtro por mes
if mes != "Todo":
    mes_nombre = mes.split()[0]
    meta = all_goals.get(mes_nombre, {})
    meses_num = {v: k for k, v in mapeo.items()}
    mes_ing = meses_num.get(mes_nombre, mes_nombre)
    meses_ing_num = {"January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
                     "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12}
    m_num = meses_ing_num.get(mes_ing, 0)
    df_filtrado = daily[daily["fecha"].apply(lambda d: d.month == m_num)]
    st.caption(f"📊 Metas {mes_nombre}: {meta.get('calorias','?')} kcal · P{meta.get('proteina','?')}g · C{meta.get('carbos','?')}g · G{meta.get('grasas','?')}g")
else:
    df_filtrado = daily
    meta = {}

# Gráficos
METRICS = [
    ("calorias", "Calorías Diarias", MACRO_COLORS["calorias"]),
    ("proteina", "Proteína Diaria (g)", MACRO_COLORS["proteina"]),
    ("carbos", "Carbohidratos Diarios (g)", MACRO_COLORS["carbos"]),
    ("grasas", "Grasas Diarias (g)", MACRO_COLORS["grasas"]),
    ("fibra", "Fibra Diaria (g)", MACRO_COLORS["fibra"]),
]

rows = [st.columns(2) for _ in range((len(METRICS) + 1) // 2)]
for i, (col_key, title, color) in enumerate(METRICS):
    row_idx = i // 2
    col_idx = i % 2
    with rows[row_idx][col_idx]:
        fig = line_chart(df_filtrado, col_key, title, color,
                         meta.get(col_key) if meta else None)
        st.plotly_chart(fig, use_container_width=True)
