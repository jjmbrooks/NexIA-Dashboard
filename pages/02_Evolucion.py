"""
Página: Evolución Temporal
Gráficos de línea con consumo diario y medias móviles
"""
import streamlit as st
import pandas as pd
from nutriflow_data import load_food_data, parse_date
from config import METAS_MENSUALES, MACRO_COLORS
from charts import line_chart

st.set_page_config(page_title="Evolución", page_icon="📈", layout="wide")
st.title("📈 Evolución Temporal")

with st.spinner("Cargando datos..."):
    records = load_food_data()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

# Agregar por día
daily = df.groupby("fecha").sum(numeric_only=True).reset_index()
daily = daily.sort_values("fecha")

mes = st.selectbox("Mes", ["Abril 2026", "Marzo 2026", "Febrero 2026", "Todo"])
meses_filtro = {"Abril 2026": 4, "Marzo 2026": 3, "Febrero 2026": 2, "Todo": 0}
if mes != "Todo":
    m = meses_filtro[mes]
    daily = daily[daily["fecha"].apply(lambda d: d.month == m)]

meta = METAS_MENSUALES.get("Abril", {})

col1, col2 = st.columns(2)
with col1:
    fig = line_chart(daily, "calorias", "Calorías Diarias", MACRO_COLORS["calorias"], meta.get("calorias"))
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = line_chart(daily, "proteina", "Proteína Diaria", MACRO_COLORS["proteina"], meta.get("proteina"))
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = line_chart(daily, "carbos", "Carbohidratos Diarios", MACRO_COLORS["carbos"], meta.get("carbos"))
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = line_chart(daily, "grasas", "Grasas Diarias", MACRO_COLORS["grasas"], meta.get("grasas"))
    st.plotly_chart(fig, use_container_width=True)
