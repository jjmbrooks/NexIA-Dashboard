"""
Body Lab — Resumen Diario
KPIs del día: calorías, tiempo, ejercicios, peso
"""
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from bodylab_data import load_activity_data, load_weight_data, parse_date

CDMX = ZoneInfo("America/Mexico_City")
ahora = datetime.now(CDMX)
hoy = ahora.date()

with st.spinner("Cargando datos de Body Lab..."):
    records = load_activity_data()
    weight_records = load_weight_data()

if not records:
    st.error("No se pudieron cargar los datos de actividad.")
    st.stop()

df = pd.DataFrame(records)
df = df.dropna(subset=["fecha"])

# ─── Datos del día ─────────────────────────────────────────
df_hoy = df[df["fecha"] == hoy]
actividades_hoy = len(df_hoy)
cal_hoy = df_hoy["calorias"].sum()
tiempo_hoy = df_hoy[df_hoy["unidad2"] == "min"]["metrica2"].sum()
ejercicios_hoy = df_hoy["ejercicio"].nunique()
categorias_hoy = df_hoy["categoria"].unique().tolist()

# ─── Último peso ──────────────────────────────────────────────
peso_actual = None
peso_anterior = None
if weight_records:
    last = weight_records[-1]
    peso_actual = last["peso_kg"]
    fecha_peso = last["fecha"]
    if len(weight_records) >= 2:
        peso_anterior = weight_records[-2]["peso_kg"]

# ─── Racha de días consecutivos entrenando ──────────────────
dias_activos = sorted(df["fecha"].unique())
racha = 0
if dias_activos:
    check = hoy
    while check in dias_activos:
        racha += 1
        check -= timedelta(days=1)

# ─── Últimos 7 días para tabla semanal ─────────────────────
DIAS_ES = {0: "Lun", 1: "Mar", 2: "Mié", 3: "Jue", 4: "Vie", 5: "Sáb", 6: "Dom"}
siete_atras = hoy - timedelta(days=7)
df_week = df[df["fecha"] >= siete_atras]
daily = df_week.groupby("fecha").agg(
    calorias=("calorias", "sum"),
    tiempo=("metrica2", "sum"),
    ejercicios=("ejercicio", "count"),
    categorias=("categoria", lambda x: ", ".join(sorted(set(x))))
).reset_index()
daily["etiqueta"] = daily["fecha"].apply(lambda d: DIAS_ES[d.weekday()])
daily = daily.sort_values("fecha")

# ─── CSS ─────────────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding: 0.6rem 0.8rem 0.3rem !important; max-width: 500px !important; }
    .element-container { margin-bottom: 0 !important; }
    div[data-testid="column"] { display: none !important; }

    .page-titulo { font-size: 1.1rem; font-weight: 700; color: #e0e0ff; text-align: center; margin-bottom: 2px; }
    .fecha { font-size: 0.75rem; color: #888; text-align: center; margin-bottom: 2px; }
    .fecha span { color: #facc15; font-weight: 700; }

    .kpi-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px;
        margin-bottom: 4px;
    }
    .kpi-grid .full-width { grid-column: 1 / -1; }
    .kpi-grid .center-col {
        grid-column: 1 / -1;
        display: flex;
        justify-content: center;
    }
    .kpi-grid .center-col .kpi { width: 50%; }

    .kpi {
        background: #1a1a2e; border-radius: 16px; padding: 12px 6px;
        text-align: center; border: 1px solid #2a2a4a;
    }
    .kpi .emoji { font-size: 1.7rem; line-height: 1; }
    .kpi .label { font-size: 0.7rem; color: #888; margin-top: 1px; }
    .kpi .valor { font-size: 1.7rem; font-weight: 800; line-height: 1.1; margin: 2px 0; }
    .kpi .valor span { font-size: 0.8rem; font-weight: 400; color: #666; }
    .kpi .delta { font-size: 0.7rem; line-height: 1; }
    .kpi .delta.pos { color: #4ade80; }
    .kpi .delta.neg { color: #f87171; }

    .kpi-mini {
        background: #16213e; border-radius: 12px; padding: 6px 10px;
        display: flex; justify-content: space-between; align-items: center;
        margin-bottom: 4px;
    }
    .kpi-mini .nm { font-size: 0.7rem; color: #888; }
    .kpi-mini .vl { font-size: 0.85rem; font-weight: 700; color: #ddd; }

    .seccion-tit { font-size: 0.85rem; font-weight: 600; color: #aaa; margin: 10px 0 6px 0; letter-spacing: 0.3px; }
    .comida {
        background: #16213e; border-radius: 10px; padding: 8px 10px;
        margin-bottom: 4px; display: flex; justify-content: space-between; align-items: center;
    }
    .comida .nom { font-weight: 600; font-size: 0.85rem; color: #ddd; }
    .comida .cat { font-size: 0.65rem; color: #888; }
    .comida .mac { font-size: 0.7rem; text-align: right; white-space: nowrap; color: #bbb; }

    .semana-tabla { font-size: 0.75rem; width: 100%; border-collapse: collapse; margin-top: 6px; }
    .semana-tabla th { color: #888; font-weight: 600; padding: 4px 5px; text-align: center; border-bottom: 1px solid #2a2a4a; font-size: 0.7rem; }
    .semana-tabla td { padding: 4px 5px; text-align: center; border-bottom: 1px solid #1e1e3a; font-size: 0.7rem; }
    .semana-tabla tr:hover { background: #1e1e3a; }
    .semana-tabla .hoy { color: #facc15; font-weight: 700; }

    hr { margin: 4px 0 !important; border-color: #2a2a4a; }
    h1, h2, h3 { display: none !important; }
    .stAlert { margin-bottom: 4px !important; font-size: 0.7rem !important; }
    .stSpinner { font-size: 0.7rem !important; }
</style>
""", unsafe_allow_html=True)

# ==================================================================
# SECCIÓN 1: KPIs DEL DÍA (2 columnas forzadas con CSS Grid)
# ==================================================================
st.markdown('<div class="page-titulo">🏋️ Body Lab — Hoy</div>', unsafe_allow_html=True)
st.markdown(f'<div class="fecha">📅 <span>{hoy.strftime("%d %B %Y")}</span> — {categorias_hoy}</div>', unsafe_allow_html=True)

def kpi_card(emoji, label, valor, unit="", delta=None, delta_cls=""):
    d_html = ""
    if delta is not None:
        sign = "+" if delta >= 0 else ""
        cls = "pos" if delta >= 0 else "neg"
        d_html = f'<div class="delta {cls}">{sign}{delta:.1f}</div>'
    u_html = f'<span>{unit}</span>' if unit else ""
    return f'<div class="kpi"><div class="emoji">{emoji}</div><div class="label">{label}</div><div class="valor">{valor:.0f}{u_html}</div>{d_html}</div>'

grid_html = f"""<div class="kpi-grid">
    {kpi_card("🔥", "Calorías", cal_hoy, "kcal")}
    {kpi_card("⏱️", "Tiempo", tiempo_hoy, "min")}
    {kpi_card("💪", "Ejercicios", actividades_hoy)}
    {kpi_card("🔥", "Racha", racha, "días")}
</div>"""

st.markdown(grid_html, unsafe_allow_html=True)

# ─── Tarjeta de peso ─────────────────────────────────────
if peso_actual:
    peso_delta = peso_actual - peso_anterior if peso_anterior else 0
    delta_peso_cls = "pos" if peso_delta <= 0 else "neg"  # perder peso = positivo
    peso_emoji = "📉" if peso_delta <= 0 else "📈"
    peso_label = f"Último: {fecha_peso.strftime('%d/%m')}" if fecha_peso else ""
    st.markdown(f"""
    <div style="background:#1a1a2e;border-radius:16px;border:1px solid #3a3a5a;padding:14px 16px;margin:8px 0;display:flex;justify-content:space-between;align-items:center;">
        <div>
            <div style="font-size:0.7rem;color:#888;">Peso corporal {peso_label}</div>
            <div style="font-size:1.6rem;font-weight:800;color:#e0e0ff;">{peso_actual:.1f} <span style="font-size:0.8rem;color:#666;font-weight:400;">kg</span></div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:0.7rem;color:#888;">vs anterior</div>
            <div style="font-size:1.2rem;font-weight:700;color:{'#4ade80' if peso_delta <= 0 else '#f87171'};">{peso_emoji} {abs(peso_delta):.1f} kg</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ==================================================================
# SECCIÓN 2: EJERCICIOS DEL DÍA
# ==================================================================
st.markdown("<hr>", unsafe_allow_html=True)

if actividades_hoy > 0:
    st.markdown(f'<div class="seccion-tit">🏋️ Ejercicios de hoy ({actividades_hoy})</div>', unsafe_allow_html=True)

    emoji_ej = {
        "Sentadillas": "🦵", "Sentadilla": "🦵",
        "Caminata": "🚶", "Caminata matutina": "🚶",
        "Lagartijas": "💪", "Push ups": "💪",
        "Press": "🏋️", "Prensa": "🏋️",
    }

    for _, row in df_hoy.iterrows():
        nombre = row["ejercicio"]
        emoji = "🏋️"
        for key, e in emoji_ej.items():
            if key.lower() in nombre.lower():
                emoji = e
                break

        reps = f'{row["metrica1"]:.0f} {row["unidad1"]}' if row["metrica1"] > 0 else ""
        tiempo = f'{row["metrica2"]:.0f} {row["unidad2"]}' if row["metrica2"] > 0 else ""
        cal = f'🔥{row["calorias"]:.0f}' if row["calorias"] > 0 else ""
        mac_text = " | ".join(filter(None, [reps, tiempo, cal]))

        st.markdown(f"""
        <div class="comida">
            <div>
                <div class="nom">{emoji} {nombre}</div>
                <div class="cat">{row["categoria"]} · {row.get("notas", "")}</div>
            </div>
            <div class="mac">{mac_text}</div>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("💤 Sin actividad registrada hoy")

# ==================================================================
# SECCIÓN 3: RESUMEN SEMANAL
# ==================================================================
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown('<div class="seccion-tit">📅 Últimos 7 días</div>', unsafe_allow_html=True)

if not daily.empty:
    rows_html = ""
    for _, r in daily.iterrows():
        es_hoy = r["fecha"] == hoy
        cls_fila = 'class="hoy"' if es_hoy else ""
        cats_short = r["categorias"][:12]
        rows_html += f"""<tr>
            <td {cls_fila}>{r['etiqueta']}</td>
            <td>{r['calorias']:.0f}</td>
            <td>{r['tiempo']:.0f}</td>
            <td>{r['ejercicios']}</td>
            <td>{cats_short}</td>
        </tr>"""

    st.markdown(f"""
    <table class="semana-tabla">
        <tr><th>Día</th><th>🔥</th><th>⏱️</th><th>💪</th><th>Tipo</th></tr>
        {rows_html}
    </table>
    """, unsafe_allow_html=True)
else:
    st.caption("Sin datos en los últimos 7 días")
