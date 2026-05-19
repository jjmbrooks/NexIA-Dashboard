"""
Página: Datos Crudos
Tabla interactiva con todos los registros — diseño profesional
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from nutriflow_data import load_food_data, parse_date

st.set_page_config(page_title="NutriFlow · Datos", page_icon="📋", layout="wide")

CDMX = ZoneInfo("America/Mexico_City")
hoy = datetime.now(CDMX).date()

st.markdown("""
<style>
    .block-container { padding: 1.2rem 1.5rem !important; max-width: 1100px !important; }
    h1 { font-size: 1.3rem !important; margin-bottom: 0.3rem !important; }
</style>
""", unsafe_allow_html=True)

st.title("📋 Registros de Alimentación")

with st.spinner("Cargando datos..."):
    records = load_food_data()

if not records:
    st.error("No se pudieron cargar los datos.")
    st.stop()

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

fecha_limite = max(df["fecha"]) - timedelta(days=dias)
df_filtered = df[df["fecha"] >= fecha_limite]

if tipo != "Todos":
    df_filtered = df_filtered[df_filtered["comida"] == tipo]

if buscar:
    df_filtered = df_filtered[df_filtered["descripcion"].str.contains(buscar, case=False, na=False)]

st.dataframe(
    df_filtered[["fecha_hora", "comida", "descripcion", "calorias", "proteina", "carbos", "grasas", "fibra"]],
    use_container_width=True,
    hide_index=True,
    column_config={
        "fecha_hora": st.column_config.TextColumn("Fecha/Hora", width="small"),
        "comida": st.column_config.TextColumn("Comida", width="small"),
        "descripcion": st.column_config.TextColumn("Descripción", width="large"),
        "calorias": st.column_config.NumberColumn("🔥 kcal", format="%.0f", width="small"),
        "proteina": st.column_config.NumberColumn("💪 Prot", format="%.1f", width="small"),
        "carbos": st.column_config.NumberColumn("🌾 Carbs", format="%.1f", width="small"),
        "grasas": st.column_config.NumberColumn("🧈 Grasas", format="%.1f", width="small"),
        "fibra": st.column_config.NumberColumn("🧵 Fibra", format="%.1f", width="small"),
    },
    height=500,
)

# Stats rápidos
total_cal = df_filtered["calorias"].sum()
total_dias = df_filtered["fecha"].nunique()
avg_cal = total_cal / total_dias if total_dias > 0 else 0

st.caption(f"📊 {len(df_filtered)} registros · {total_dias} días · promedio {avg_cal:.0f} kcal/día · total {total_cal:.0f} kcal")
