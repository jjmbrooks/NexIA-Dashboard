"""
Página: Datos Crudos
Tabla interactiva con todos los registros
"""
import streamlit as st
import pandas as pd
from nutriflow_data import load_food_data, parse_date

st.set_page_config(page_title="Datos", page_icon="📋", layout="wide")
st.title("📋 Registros de Alimentación")

with st.spinner("Cargando datos..."):
    records = load_food_data()

df = pd.DataFrame(records)
df["fecha"] = df["fecha_hora"].apply(parse_date)
df = df.dropna(subset=["fecha"])

# Filtros
col1, col2, col3 = st.columns(3)
with col1:
    dias = st.number_input("Últimos N días", min_value=1, max_value=365, value=30)
with col2:
    tipos = ["Todos"] + sorted(df["comida"].unique().tolist())
    tipo = st.selectbox("Tipo de comida", tipos)
with col3:
    buscar = st.text_input("Buscar en descripción", "")

# Aplicar filtros
fecha_limite = df["fecha"].max() - pd.Timedelta(days=dias)
df_filtered = df[df["fecha"] >= fecha_limite]

if tipo != "Todos":
    df_filtered = df_filtered[df_filtered["comida"] == tipo]

if buscar:
    df_filtered = df_filtered[df_filtered["descripcion"].str.contains(buscar, case=False, na=False)]

# Mostrar
st.dataframe(
    df_filtered[["fecha_hora", "comida", "descripcion", "calorias", "proteina", "carbos", "grasas", "fibra"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "fecha_hora": "Fecha/Hora",
        "calorias": st.column_config.NumberColumn("Cal", format="%.0f"),
        "proteina": st.column_config.NumberColumn("Prot", format="%.1f"),
        "carbos": st.column_config.NumberColumn("Carbs", format="%.1f"),
        "grasas": st.column_config.NumberColumn("Grasas", format="%.1f"),
        "fibra": st.column_config.NumberColumn("Fibra", format="%.1f"),
    }
)

st.caption(f"Mostrando {len(df_filtered)} de {len(df)} registros")
