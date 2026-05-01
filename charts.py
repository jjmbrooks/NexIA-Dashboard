"""
Funciones de visualización para NutriFlow Dashboard
Gráficas con plotly
"""
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "calorias": "#FF6B35",
    "proteina": "#1E88E5",
    "carbos": "#43A047",
    "grasas": "#FDD835",
    "fibra": "#8E24AA",
    "meta": "#FFFFFF80",
}

def barra_progreso(valor: float, meta: float, label: str, color: str, unidad: str = "") -> go.Figure:
    """Barra de progreso horizontal tipo KPI"""
    pct = min(valor / meta * 100, 100) if meta > 0 else 0
    fig = go.Figure(go.Bar(
        x=[pct],
        y=[""],
        orientation="h",
        marker=dict(color=color, line=dict(color=color, width=2)),
        text=f"{valor:.0f}{unidad} / {meta:.0f}{unidad} ({pct:.0f}%)",
        textposition="inside",
        insidetextanchor="middle",
        showlegend=False,
        width=0.3
    ))
    fig.update_layout(
        height=80, margin=dict(l=10, r=10, t=5, b=5),
        xaxis=dict(range=[0, 110], showticklabels=False, showgrid=False),
        yaxis=dict(showticklabels=False),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title=dict(text=f"<b>{label}</b>", font=dict(size=14), x=0, y=0.95),
    )
    return fig

def line_chart(df: pd.DataFrame, col: str, title: str, color: str, meta: float = None):
    """Gráfico de línea con media móvil"""
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df[col],
        mode="lines+markers", name=title,
        line=dict(color=color, width=2),
        marker=dict(size=4),
    ))
    if meta:
        fig.add_hline(y=meta, line_dash="dash", line_color="gray",
                      annotation_text=f"Meta {meta:.0f}")
    # Media móvil 7 días
    df_sorted = df.sort_values("fecha")
    df_sorted["media"] = df_sorted[col].rolling(7, min_periods=2).mean()
    fig.add_trace(go.Scatter(
        x=df_sorted["fecha"], y=df_sorted["media"],
        mode="lines", name="Media 7d",
        line=dict(color=color, width=2, dash="dot"),
    ))
    fig.update_layout(
        title=title, height=350,
        template="plotly_dark",
        margin=dict(l=40, r=20, t=40, b=30),
        hovermode="x unified",
    )
    return fig

def meal_distribution(df: pd.DataFrame, col: str, title: str):
    """Gráfico de dona por tipo de comida"""
    fig = px.pie(
        df, values=col, names="comida",
        title=title, hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )
    fig.update_layout(template="plotly_dark", height=350)
    fig.update_traces(textinfo="label+percent")
    return fig

def monthly_comparison(daily_df: pd.DataFrame, metas: dict, mes: str):
    """Barras comparativas: promedio mensual vs meta"""
    avg = daily_df.mean(numeric_only=True)
    metrics = [
        ("calorias", "Calorías", COLORS["calorias"], "kcal"),
        ("proteina", "Proteína", COLORS["proteina"], "g"),
        ("carbos", "Carbohidratos", COLORS["carbos"], "g"),
        ("grasas", "Grasas", COLORS["grasas"], "g"),
        ("fibra", "Fibra", COLORS["fibra"], "g"),
    ]
    fig = go.Figure()
    for i, (key, label, color, unit) in enumerate(metrics):
        fig.add_trace(go.Bar(
            name=label,
            x=[f"Promedio {mes}"],
            y=[avg.get(key, 0)],
            marker_color=color,
            text=f"{avg.get(key, 0):.0f}{unit}",
            textposition="outside",
            offsetgroup=i,
        ))
        fig.add_trace(go.Bar(
            name=f"Meta {label}",
            x=[f"Meta {mes}"],
            y=[metas.get(key, 0)],
            marker_color=color,
            marker_pattern_shape="/",
            text=f"{metas.get(key, 0):.0f}{unit}",
            textposition="outside",
            offsetgroup=i,
            showlegend=False,
        ))
    fig.update_layout(
        barmode="group", height=400,
        template="plotly_dark",
        title=f"Comparativa Mensual - {mes}",
        margin=dict(l=40, r=20, t=40, b=30),
    )
    return fig
