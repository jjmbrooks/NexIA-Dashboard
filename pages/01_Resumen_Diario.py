"""
Página: Resumen del Día
Muestra los macros del día actual vs metas
"""
import streamlit as st
import pandas as pd
from datetime import datetime, date
from nutriflow_data import load_food_data, parse_date
from config import METAS_MENSUALES, MACRO_LABELS, MACRO_COLORS, MACRO_UNITS

st.set_page_config(page_title="Resumen Diario", page_icon="📊", layout="wide")
st.title("📊 Resumen Diario")

mes_actual = datetime.now().strftime("%B")
mes_esp = {"April": "Abril", "May": "Mayo", "June": "Junio"}.get(mes_actual, mes_actual)
meta = METAS_MENSUALES.get(mes_esp, METAS_MENSUALES["Abril"])

with st.spinner("Cargando datos de NutriFlow..."):
    records = load_food_data()

if not records:
    st.error("No se pudieron cargar los datos. El snapshot de datos no está disponible.")
    st.stop()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

hoy = date.today()
df_hoy = df[df["fecha"] == hoy]

comidas_hoy = len(df_hoy)
sum_hoy = df_hoy.sum(numeric_only=True)

# KPIs
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("Calorías", f"{sum_hoy.get('calorias', 0):.0f} kcal",
              delta=f"{sum_hoy.get('calorias', 0) - meta['calorias']:.0f} vs meta")
with col2:
    st.metric("Proteína", f"{sum_hoy.get('proteina', 0):.0f}g",
              delta=f"{sum_hoy.get('proteina', 0) - meta['proteina']:.0f} vs meta")
with col3:
    st.metric("Carbohidratos", f"{sum_hoy.get('carbos', 0):.0f}g",
              delta=f"{sum_hoy.get('carbos', 0) - meta['carbos']:.0f} vs meta")
with col4:
    st.metric("Grasas", f"{sum_hoy.get('grasas', 0):.0f}g",
              delta=f"{sum_hoy.get('grasas', 0) - meta['grasas']:.0f} vs meta")
with col5:
    st.metric("Fibra", f"{sum_hoy.get('fibra', 0):.0f}g",
              delta=f"{sum_hoy.get('fibra', 0) - meta['fibra']:.0f} vs meta")

st.divider()

# Comidas del día
if comidas_hoy > 0:
    st.subheader(f"Comidas de hoy ({comidas_hoy})")
    for _, row in df_hoy.iterrows():
        with st.expander(f"{row['comida']} — {row.get('calorias', 0):.0f} kcal"):
            cols = st.columns(5)
            cols[0].metric("Cal", f"{row.get('calorias', 0):.0f}")
            cols[1].metric("Proteína", f"{row.get('proteina', 0):.1f}g")
            cols[2].metric("Carbs", f"{row.get('carbos', 0):.1f}g")
            cols[3].metric("Grasas", f"{row.get('grasas', 0):.1f}g")
            cols[4].metric("Fibra", f"{row.get('fibra', 0):.1f}g")
            st.caption(f"{row['descripcion']}")
else:
    st.info("Aún no hay registros para hoy.")

# Últimos 7 días
st.divider()
st.subheader("Últimos 7 días")
df_week = df[df["fecha"] >= pd.Timestamp.now() - pd.Timedelta(days=7)]
daily = df_week.groupby("fecha").sum(numeric_only=True).reset_index()
st.dataframe(daily, use_container_width=True, hide_index=True)
