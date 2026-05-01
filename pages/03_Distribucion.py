"""
Página: Distribución de Comidas
Qué % de cada macro viene de cada comida
"""
import streamlit as st
import pandas as pd
from nutriflow_data import load_food_data, parse_date
from charts import meal_distribution

st.set_page_config(page_title="Distribución", page_icon="🥧", layout="wide")
st.title("🥧 Distribución por Comida")

with st.spinner("Cargando datos..."):
    records = load_food_data()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

# Filtro de período
max_date = df["fecha"].max()
min_date = df["fecha"].min()
date_range = st.date_input("Período", [min_date, max_date], min_value=min_date, max_value=max_date)
if len(date_range) == 2:
    df = df[(df["fecha"] >= date_range[0]) & (df["fecha"] <= date_range[1])]

# Agrupar por tipo de comida
by_meal = df.groupby("comida").sum(numeric_only=True).reset_index()

col1, col2 = st.columns(2)
with col1:
    fig = meal_distribution(by_meal, "calorias", "Distribución de Calorías")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = meal_distribution(by_meal, "proteina", "Distribución de Proteína")
    st.plotly_chart(fig, use_container_width=True)

col1, col2 = st.columns(2)
with col1:
    fig = meal_distribution(by_meal, "carbos", "Distribución de Carbohidratos")
    st.plotly_chart(fig, use_container_width=True)
with col2:
    fig = meal_distribution(by_meal, "grasas", "Distribución de Grasas")
    st.plotly_chart(fig, use_container_width=True)
