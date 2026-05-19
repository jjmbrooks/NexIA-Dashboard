"""
Funciones de visualización para NutriFlow Dashboard
Gráficas con plotly — diseño oscuro profesional
"""
import plotly.graph_objects as go
import pandas as pd

COLORS = {
    "calorias": "#FF6B35",
    "proteina": "#818cf8",
    "carbos": "#22c55e",
    "grasas": "#facc15",
    "fibra": "#c084fc",
    "meta": "rgba(255,255,255,0.3)",
}

DARK_TEMPLATE = go.layout.Template(
    layout=dict(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c0c0e0", size=11),
        xaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.05)",
            showline=True, linecolor="rgba(255,255,255,0.1)",
            zeroline=False,
        ),
        yaxis=dict(
            showgrid=True, gridcolor="rgba(255,255,255,0.05)",
            showline=True, linecolor="rgba(255,255,255,0.1)",
            zeroline=False,
        ),
    )
)


def line_chart(df: pd.DataFrame, col: str, title: str, color: str, meta: float = None):
    """Gráfico de línea con media móvil — diseño oscuro profesional"""
    fig = go.Figure()
    fig.update_layout(template=DARK_TEMPLATE)

    # Línea principal
    fig.add_trace(go.Scatter(
        x=df["fecha"], y=df[col],
        mode="lines+markers",
        name="Consumo",
        line=dict(color=color, width=2.5),
        marker=dict(size=5, color=color, line=dict(width=1, color="rgba(255,255,255,0.3)")),
        hovertemplate="%{x|%d/%m}<br>%{y:.0f}<extra></extra>",
    ))

    # Media móvil 7 días
    df_sorted = df.sort_values("fecha")
    df_sorted["media"] = df_sorted[col].rolling(7, min_periods=2).mean()
    fig.add_trace(go.Scatter(
        x=df_sorted["fecha"], y=df_sorted["media"],
        mode="lines",
        name="Media 7d",
        line=dict(color=color, width=2, dash="dot"),
        hovertemplate="%{x|%d/%m}<br>Media: %{y:.0f}<extra></extra>",
    ))

    # Línea de meta
    if meta is not None and meta > 0:
        fig.add_hline(
            y=meta,
            line_dash="dash",
            line_color="rgba(255,255,255,0.25)",
            line_width=1.5,
            annotation_text=f"Meta {meta:.0f}",
            annotation_font=dict(size=10, color="rgba(255,255,255,0.4)"),
            annotation_position="top right",
        )

    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#e0e0ff"), x=0, xanchor="left"),
        height=320,
        margin=dict(l=40, r=20, t=40, b=30),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1,
            font=dict(size=10, color="#888"),
        ),
    )
    return fig


def meal_distribution(df: pd.DataFrame, col: str, title: str):
    """Gráfico de dona por tipo de comida"""
    fig = go.Figure(data=[go.Pie(
        labels=df["comida"],
        values=df[col],
        hole=0.5,
        textinfo="label+percent",
        textfont=dict(size=11, color="#c0c0e0"),
        marker=dict(
            colors=px_colors_qualitative(),
            line=dict(color="#0a0a14", width=2),
        ),
        hovertemplate="%{label}<br>%{value:.0f} (%{percent})<extra></extra>",
    )])
    fig.update_layout(
        title=dict(text=title, font=dict(size=13, color="#e0e0ff"), x=0, xanchor="left"),
        height=340,
        margin=dict(l=20, r=20, t=40, b=10),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c0c0e0", size=11),
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=-0.15, font=dict(size=10, color="#888")),
    )
    return fig


def px_colors_qualitative():
    """Paleta de colores cualitativos para gráficos de dona"""
    return ["#6366f1", "#22c55e", "#facc15", "#ff6b35", "#c084fc",
            "#06b6d4", "#f472b6", "#a855f7", "#14b8a6", "#eab308"]


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
    fig.update_layout(template=DARK_TEMPLATE)

    for i, (key, label, color, unit) in enumerate(metrics):
        # Barra de promedio
        fig.add_trace(go.Bar(
            name=label,
            x=["Promedio"],
            y=[avg.get(key, 0)],
            marker_color=color,
            text=f"{avg.get(key, 0):.0f}{unit}",
            textposition="outside",
            textfont=dict(size=10, color="#c0c0e0"),
            offsetgroup=i,
            width=0.35,
        ))
        # Barra de meta (con patrón)
        fig.add_trace(go.Bar(
            name=f"Meta",
            x=["Meta"],
            y=[metas.get(key, 0)],
            marker_color=color,
            marker_pattern_shape="/",
            marker_pattern_fgcolor="rgba(255,255,255,0.15)",
            text=f"{metas.get(key, 0):.0f}{unit}",
            textposition="outside",
            textfont=dict(size=10, color="rgba(255,255,255,0.5)"),
            offsetgroup=i,
            width=0.35,
            showlegend=False,
        ))

    fig.update_layout(
        barmode="group",
        height=400,
        title=dict(text=f"Comparativa Mensual — {mes}", font=dict(size=13, color="#e0e0ff"), x=0, xanchor="left"),
        margin=dict(l=40, r=20, t=40, b=30),
        hovermode="x unified",
        legend=dict(
            orientation="h", yanchor="bottom", y=1.02,
            font=dict(size=10, color="#888"),
        ),
        xaxis=dict(showticklabels=False),
    )
    return fig
