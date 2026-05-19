"""
Body Lab — Evolución
Tendencias: calorías semanales, tiempo, peso corporal, volumen de fuerza
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bodylab_data import load_activity_data, load_weight_data

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()

with st.spinner("Cargando datos..."):
    records = load_activity_data()
    weight_records = load_weight_data()

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
    hr { margin: 4px 0 !important; border-color: #2a2a4a; }
    .stAlert { margin-bottom: 4px !important; font-size: 0.7rem !important; }
    .stSpinner { font-size: 0.7rem !important; }
    h1, h2, h3 { display: none !important; }
</style>"""
st.markdown(CSS, unsafe_allow_html=True)

st.markdown('<div class="page-titulo">📈 Body Lab — Evolución</div>', unsafe_allow_html=True)
st.markdown(f'<div class="fecha" style="text-align:center;font-size:0.75rem;color:#888;margin-bottom:8px;">📅 {hoy.strftime("%d %B %Y")}</div>'.replace("</style>", ""), unsafe_allow_html=True)

# ─── Gráfica 1: Calorías por día (últimos 14 días) ─────
catorce_atras = hoy - timedelta(days=14)
df_14 = df[df["fecha"] >= catorce_atras].copy()

daily_cal = df_14.groupby("fecha")["calorias"].sum().reset_index()
daily_cal.columns = ["fecha", "calorias"]

if not daily_cal.empty:
    st.markdown('<div class="subtit">🔥 Calorías por día</div>', unsafe_allow_html=True)

    dias_es = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}
    daily_cal["dia"] = daily_cal["fecha"].apply(lambda d: dias_es.get(d.weekday(), ""))
    daily_cal["fecha_str"] = daily_cal["fecha"].apply(lambda d: d.strftime("%d/%m"))

    max_cal = daily_cal["calorias"].max() or 1
    bars = ""
    for _, r in daily_cal.iterrows():
        pct = max(r["calorias"] / max_cal * 100, 3)
        es_hoy = "color:#facc15;" if r["fecha"] == hoy else ""
        bars += f"""
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
            <div style="width:32px;font-size:0.65rem;{es_hoy}text-align:right;">{r['dia']}</div>
            <div style="flex:1;background:#1a1a2e;border-radius:4px;height:18px;overflow:hidden;">
                <div style="width:{pct}%;background:linear-gradient(90deg,#ff6b35,#ff8c42);height:18px;border-radius:4px;min-width:3px;"></div>
            </div>
            <div style="width:40px;font-size:0.7rem;color:#bbb;text-align:right;">{r['calorias']:.0f}</div>
        </div>"""

    st.markdown(f'<div style="margin-bottom:12px;">{bars}</div>', unsafe_allow_html=True)

# ─── Gráfica 2: Tiempo de entrenamiento por día ─────
daily_time = df_14.groupby("fecha")["metrica2"].sum().reset_index()
daily_time.columns = ["fecha", "minutos"]
daily_time = daily_time[daily_time["minutos"] > 0]

if not daily_time.empty:
    st.markdown('<div class="subtit">⏱️ Tiempo de entrenamiento (min)</div>', unsafe_allow_html=True)
    daily_time["dia"] = daily_time["fecha"].apply(lambda d: dias_es.get(d.weekday(), ""))
    daily_time["fecha_str"] = daily_time["fecha"].apply(lambda d: d.strftime("%d/%m"))

    max_t = daily_time["minutos"].max() or 1
    bars = ""
    for _, r in daily_time.iterrows():
        pct = max(r["minutos"] / max_t * 100, 3)
        es_hoy = "color:#facc15;" if r["fecha"] == hoy else ""
        bars += f"""
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
            <div style="width:32px;font-size:0.65rem;{es_hoy}text-align:right;">{r['dia']}</div>
            <div style="flex:1;background:#1a1a2e;border-radius:4px;height:18px;overflow:hidden;">
                <div style="width:{pct}%;background:linear-gradient(90deg,#818cf8,#6366f1);height:18px;border-radius:4px;min-width:3px;"></div>
            </div>
            <div style="width:40px;font-size:0.7rem;color:#bbb;text-align:right;">{r['minutos']:.0f}</div>
        </div>"""

    st.markdown(f'<div style="margin-bottom:12px;">{bars}</div>', unsafe_allow_html=True)

# ─── Gráfica 3: Peso corporal ─────────────────────────
if len(weight_records) >= 2:
    st.markdown('<div class="subtit">📉 Peso corporal (kg)</div>', unsafe_allow_html=True)

    wd = pd.DataFrame(weight_records)
    wd = wd.dropna(subset=["fecha"]).sort_values("fecha")

    min_peso = wd["peso_kg"].min() - 2
    max_peso = wd["peso_kg"].max() + 2
    rango = max_peso - min_peso if max_peso > min_peso else 5

    # Línea de puntos
    points = ""
    for i, (_, r) in enumerate(wd.iterrows()):
        y_pct = 100 - ((r["peso_kg"] - min_peso) / rango * 100)
        is_last = "border: 3px solid #facc15;" if i == len(wd) - 1 else ""
        points += f"""
        <div style="position:absolute;bottom:{y_pct}%;left:{i/(len(wd)-1)*100 if len(wd)>1 else 50}%;transform:translate(-50%,50%);">
            <div style="width:10px;height:10px;border-radius:50%;background:#4ade80;{is_last}"></div>
        </div>"""

    # Conectar con líneas
    lines = ""
    for i in range(len(wd) - 1):
        y1 = 100 - ((wd.iloc[i]["peso_kg"] - min_peso) / rango * 100)
        y2 = 100 - ((wd.iloc[i+1]["peso_kg"] - min_peso) / rango * 100)
        x1 = i / (len(wd)-1) * 100 if len(wd) > 1 else 50
        x2 = (i+1) / (len(wd)-1) * 100 if len(wd) > 1 else 50
        lines += f'<line x1="{x1}%" y1="{y1}%" x2="{x2}%" y2="{y2}%" stroke="#4ade80" stroke-width="2"/>'

    # Último valor
    ultimo = wd.iloc[-1]
    ultimo_pct = 100 - ((ultimo["peso_kg"] - min_peso) / rango * 100)
    labels = ""
    for _, r in wd.iterrows():
        y = 100 - ((r["peso_kg"] - min_peso) / rango * 100)
        ix = list(wd.index).index(r.name)
        x = ix / (len(wd)-1) * 100 if len(wd) > 1 else 50
        labels += f'<div style="position:absolute;bottom:{y-8}%;left:{x}%;transform:translateX(-50%);font-size:0.6rem;color:#888;">{r["peso_kg"]:.1f}</div>'

    st.markdown(f"""
    <div style="background:#1a1a2e;border-radius:16px;border:1px solid #2a2a4a;padding:16px;position:relative;height:160px;margin-bottom:12px;">
        <svg width="100%" height="100%" style="position:absolute;top:0;left:0;">
            {lines}
        </svg>
        <div style="position:absolute;bottom:0;left:0;right:0;display:flex;justify-content:space-between;padding:0 4px;font-size:0.6rem;color:#555;">
            {''.join(f'<span>{r["fecha"].strftime("%d/%m")}</span>' for _, r in wd.iterrows())}
        </div>
        {points}
        {labels}
    </div>
    """, unsafe_allow_html=True)

# ─── Resumen semanal: totales ─────────────────────────
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="subtit">📊 Resumen semanal</div>', unsafe_allow_html=True)

df_semana = df[df["fecha"] >= (hoy - timedelta(days=7))]
cal_sem = df_semana["calorias"].sum()
tiempo_sem = df_semana["metrica2"].sum()
dias_sem = df_semana["fecha"].nunique()
ejercicios_sem = len(df_semana)

st.markdown(f"""
<div style="display:grid;grid-template-columns:1fr 1fr;gap:6px;">
    <div style="background:#1a1a2e;border-radius:12px;padding:10px;text-align:center;border:1px solid #2a2a4a;">
        <div style="font-size:0.7rem;color:#888;">🔥 Calorías</div>
        <div style="font-size:1.4rem;font-weight:700;color:#e0e0ff;">{cal_sem:.0f}</div>
    </div>
    <div style="background:#1a1a2e;border-radius:12px;padding:10px;text-align:center;border:1px solid #2a2a4a;">
        <div style="font-size:0.7rem;color:#888;">⏱️ Tiempo total</div>
        <div style="font-size:1.4rem;font-weight:700;color:#e0e0ff;">{tiempo_sem:.0f} min</div>
    </div>
    <div style="background:#1a1a2e;border-radius:12px;padding:10px;text-align:center;border:1px solid #2a2a4a;">
        <div style="font-size:0.7rem;color:#888;">📅 Días activos</div>
        <div style="font-size:1.4rem;font-weight:700;color:#e0e0ff;">{dias_sem}/7</div>
    </div>
    <div style="background:#1a1a2e;border-radius:12px;padding:10px;text-align:center;border:1px solid #2a2a4a;">
        <div style="font-size:0.7rem;color:#888;">🏋️ Ejercicios</div>
        <div style="font-size:1.4rem;font-weight:700;color:#e0e0ff;">{ejercicios_sem}</div>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── Progresión de fuerza (sentadillas por semana) ──
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="subtit">🦵 Progresión: Sentadillas por semana</div>', unsafe_allow_html=True)

df_fuerza = df[df["categoria"] == "Fuerza"].copy()
sentadillas = df_fuerza[df_fuerza["ejercicio"].str.lower().str.contains("sentadilla", na=False)].copy()
sentadillas["semana"] = sentadillas["fecha"].apply(lambda d: d.strftime("%Y-W%W"))

if not sentadillas.empty:
    semanal = sentadillas.groupby("semana").agg(
        reps=("metrica1", "sum"),
        veces=("ejercicio", "count")
    ).reset_index().sort_values("semana")

    max_reps = semanal["reps"].max() or 1
    bars = ""
    for _, r in semanal.iterrows():
        pct = max(r["reps"] / max_reps * 100, 3)
        bars += f"""
        <div style="display:flex;align-items:center;gap:6px;margin-bottom:3px;">
            <div style="width:48px;font-size:0.65rem;color:#888;text-align:right;">{r['semana'][-2:]}</div>
            <div style="flex:1;background:#1a1a2e;border-radius:4px;height:18px;overflow:hidden;">
                <div style="width:{pct}%;background:linear-gradient(90deg,#22c55e,#4ade80);height:18px;border-radius:4px;min-width:3px;"></div>
            </div>
            <div style="width:50px;font-size:0.7rem;color:#bbb;text-align:right;">{r['reps']:.0f} reps</div>
        </div>"""

    st.markdown(f'<div style="margin-bottom:12px;">{bars}</div>', unsafe_allow_html=True)
else:
    st.caption("Sin datos de sentadillas aún")
