"""
Body Lab — Distribución y Datos Crudos
Distribución Fuerza vs Cardio, top ejercicios, tabla completa
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bodylab_data import load_activity_data

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()

with st.spinner("Cargando datos..."):
    records = load_activity_data()

if not records:
    st.error("No se pudieron cargar los datos.")
    st.stop()

df = pd.DataFrame(records)
df = df.dropna(subset=["fecha"])

CSS = """
<style>
    .block-container { padding: 0.6rem 0.8rem 0.3rem !important; max-width: 500px !important; }
    .element-container { margin-bottom: 0 !important; }
    div[data-testid="column"] { display: none !important; }
    .page-titulo { font-size: 1.1rem; font-weight: 700; color: #e0e0ff; text-align: center; margin-bottom: 2px; }
    .subtit { font-size: 0.85rem; font-weight: 600; color: #aaa; margin: 16px 0 8px 0; letter-spacing: 0.3px; }
    .info-card {
        background: #1a1a2e; border-radius: 14px; padding: 14px;
        border: 1px solid #2a2a4a; margin-bottom: 8px;
    }
    .info-card .val { font-size: 1.5rem; font-weight: 800; color: #e0e0ff; }
    .info-card .lb { font-size: 0.75rem; color: #888; }
    hr { margin: 4px 0 !important; border-color: #2a2a4a; }
    .stAlert { margin-bottom: 4px !important; font-size: 0.7rem !important; }
    .stSpinner { font-size: 0.7rem !important; }
    h1, h2, h3 { display: none !important; }
    .dataframe { font-size: 0.7rem !important; }
    div[data-testid="stDataFrame"] { font-size: 0.7rem; }
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown('<div class="page-titulo">🥧 Body Lab — Distribución</div>', unsafe_allow_html=True)
st.markdown(f'<div class="subtit" style="text-align:center;font-size:0.75rem;color:#888;margin-bottom:8px;">📅 {hoy.strftime("%d %B %Y")}</div>'.replace("</style>", ""), unsafe_allow_html=True)

# ─── KPI generales ──────────────────────────────────────
total_cal = df["calorias"].sum()
total_dias = df["fecha"].nunique()
total_ejercicios = len(df)
total_tiempo = df["metrica2"].sum()

st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;margin-bottom:12px;">
    <div class="info-card" style="text-align:center;">
        <div class="val">{total_dias}</div>
        <div class="lb">Días activos</div>
    </div>
    <div class="info-card" style="text-align:center;">
        <div class="val">{total_ejercicios}</div>
        <div class="lb">Ejercicios totales</div>
    </div>
    <div class="info-card" style="text-align:center;">
        <div class="val">{total_cal:.0f}</div>
        <div class="lb">🔥 kcal totales</div>
    </div>
    <div class="info-card" style="text-align:center;">
        <div class="val">{total_tiempo:.0f}</div>
        <div class="lb">⏱️ min totales</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Distribución Fuerza vs Cardio ─────────────────────
st.markdown('<div class="subtit">🎯 Distribución por categoría</div>', unsafe_allow_html=True)

cat_stats = df.groupby("categoria").agg(
    calorias=("calorias", "sum"),
    minutos=("metrica2", "sum"),
    conteo=("ejercicio", "count")
).reset_index()

total_cat_cal = cat_stats["calorias"].sum() or 1
total_cat_time = cat_stats["minutos"].sum() or 1
total_cat_count = cat_stats["conteo"].sum() or 1

for _, r in cat_stats.iterrows():
    pct_cal = r["calorias"] / total_cat_cal * 100
    pct_time = r["minutos"] / total_cat_time * 100
    pct_count = r["conteo"] / total_cat_count * 100
    emoji = "💪" if r["categoria"] == "Fuerza" else "🚶" if r["categoria"] == "Cardio" else "🎯"

    st.markdown(f"""
    <div style="background:#1a1a2e;border-radius:12px;border:1px solid #2a2a4a;padding:10px 14px;margin-bottom:6px;">
        <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;">
            <div><span style="font-size:1.2rem;">{emoji}</span> <strong>{r['categoria']}</strong></div>
            <div style="font-size:0.8rem;color:#bbb;">{r['conteo']} ejercicios</div>
        </div>
        <div style="display:flex;gap:12px;font-size:0.7rem;color:#888;">
            <span>🔥 {r['calorias']:.0f} kcal ({pct_cal:.0f}%)</span>
            <span>⏱️ {r['minutos']:.0f} min ({pct_time:.0f}%)</span>
        </div>
        <div style="margin-top:4px;background:#0f0f1a;border-radius:4px;height:6px;">
            <div style="width:{pct_cal}%;background:{'#818cf8' if r['categoria']=='Fuerza' else '#ff6b35'};height:6px;border-radius:4px;"></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ─── Top ejercicios ─────────────────────────────────────
st.markdown('<div class="subtit">🏆 Top 10 ejercicios más frecuentes</div>', unsafe_allow_html=True)

top_ej = df["ejercicio"].value_counts().head(10)
max_top = top_ej.max() or 1

for ej, count in top_ej.items():
    pct = count / max_top * 100
    cal_ej = df[df["ejercicio"] == ej]["calorias"].sum()
    st.markdown(f"""
    <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
        <div style="width:65px;font-size:0.65rem;color:#888;text-align:right;overflow:hidden;text-overflow:ellipsis;">{ej[:12]}</div>
        <div style="flex:1;background:#1a1a2e;border-radius:4px;height:14px;overflow:hidden;">
            <div style="width:{pct}%;background:linear-gradient(90deg,#6366f1,#818cf8);height:14px;border-radius:4px;min-width:3px;"></div>
        </div>
        <div style="width:30px;font-size:0.7rem;color:#bbb;text-align:right;">{count}</div>
        {f'<div style="width:35px;font-size:0.65rem;color:#888;text-align:right;">🔥{cal_ej:.0f}</div>' if cal_ej>0 else ''}
    </div>
    """, unsafe_allow_html=True)

# ─── Datos Crudos ──────────────────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="subtit">📋 Bitácora completa</div>', unsafe_allow_html=True)

# Filtros
col_f1, col_f2 = st.columns(2)
with col_f1:
    cats_disponibles = sorted(df["categoria"].unique().tolist())
    cat_filter = st.selectbox("Categoría", ["Todas"] + cats_disponibles, key="bl_cat")
with col_f2:
    periodos = ["Todo", "Últimos 7 días", "Últimos 14 días", "Este mes"]
    per_filter = st.selectbox("Periodo", periodos, key="bl_per")

df_display = df.copy()

if cat_filter != "Todas":
    df_display = df_display[df_display["categoria"] == cat_filter]

if per_filter == "Últimos 7 días":
    df_display = df_display[df_display["fecha"] >= (hoy - timedelta(days=7))]
elif per_filter == "Últimos 14 días":
    df_display = df_display[df_display["fecha"] >= (hoy - timedelta(days=14))]
elif per_filter == "Este mes":
    df_display = df_display[df_display["fecha"].apply(lambda d: d.month == hoy.month and d.year == hoy.year)]

if not df_display.empty:
    df_table = df_display[["fecha", "hora", "categoria", "ejercicio", "metrica1", "unidad1", "metrica2", "unidad2", "calorias", "notas"]].copy()
    df_table["fecha"] = df_table["fecha"].apply(lambda d: d.strftime("%d/%m/%Y"))
    df_table.columns = ["Fecha", "Hora", "Cat", "Ejercicio", "#", "Unid", "Tiempo", "Unid2", "🔥 kcal", "Notas"]

    st.dataframe(
        df_table.sort_values("Fecha", ascending=False),
        hide_index=True,
        height=400,
        use_container_width=True,
    )
else:
    st.info("Sin registros con ese filtro")
