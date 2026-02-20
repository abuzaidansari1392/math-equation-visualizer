"""
plot_utils.py
Shared Plotly figure utilities — theming, axis formatting, annotations.
"""

import plotly.graph_objects as go
import numpy as np

# ── Colour palette ──────────────────────────────────────────────────────────
CURVE_COLOR     = "#00C9FF"   # bright cyan for main curve
ROOT_COLOR      = "#FF6B6B"   # coral for roots
VERTEX_COLOR    = "#FFD93D"   # gold for special points
CRITICAL_COLOR  = "#6BCB77"   # green for critical / inflection
GRID_COLOR      = "rgba(255,255,255,0.08)"
AXIS_COLOR      = "rgba(255,255,255,0.35)"
PAPER_BG        = "#0D1117"
PLOT_BG         = "#161B22"
FONT_COLOR      = "#E6EDF3"
FONT_FAMILY     = "Fira Code, monospace"


def base_figure(title: str = "", x_label: str = "x", y_label: str = "y") -> go.Figure:
    """
    Return a pre-styled dark-themed Plotly figure.
    All equation plots start from this template.
    """
    
    fig = go.Figure()

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=18, color=FONT_COLOR, family=FONT_FAMILY),
            x=0.5, xanchor="center",
            y=0.95, yanchor="top"
        ),
        paper_bgcolor=PAPER_BG,
        plot_bgcolor=PLOT_BG,
        font=dict(color=FONT_COLOR, family=FONT_FAMILY),

        xaxis=dict(
            title=x_label,
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=True,
            zerolinecolor=AXIS_COLOR,
            zerolinewidth=2,
        ),

        yaxis=dict(
            title=dict(
                text=y_label,
                font=dict(size=16),
                standoff=20
            ),
            automargin=True,
            showgrid=True,
            gridcolor=GRID_COLOR,
            zeroline=True,
            zerolinecolor=AXIS_COLOR,
            zerolinewidth=2,
        ),

        legend=dict(
            bgcolor="#ffffff",
            bordercolor=AXIS_COLOR,
            borderwidth=1,
            font=dict(color="#000000")  # black text
        ),

        margin=dict(l=50, r=30, t=60, b=50),
        hovermode="x unified",
    )

    return fig


def add_curve(fig: go.Figure, x: np.ndarray, y: np.ndarray,
              name: str = "f(x)", color: str = CURVE_COLOR,
              width: int = 3) -> go.Figure:
    """Add the main equation curve to the figure."""
    fig.add_trace(go.Scatter(
        x=x, y=y,
        mode="lines",
        name=name,
        line=dict(color=color, width=width),
    ))
    return fig


def add_scatter_point(fig: go.Figure, x: float, y: float,
                      label: str, color: str = ROOT_COLOR,
                      symbol: str = "circle", size: int = 10) -> go.Figure:
    """Add a single labelled scatter point (root, vertex, etc.)."""
    fig.add_trace(go.Scatter(
        x=[x], y=[y],
        mode="markers+text",
        name=label,
        text=[f"  {label}"],
        textposition="top right",
        textfont=dict(color=color, size=11),
        marker=dict(color=color, size=size, symbol=symbol,
                    line=dict(color="white", width=1)),
        showlegend=True,
    ))
    return fig


def add_vline(fig: go.Figure, x: float, label: str,
              color: str = AXIS_COLOR, dash: str = "dash") -> go.Figure:
    """Add a vertical dashed reference line."""
    fig.add_vline(x=x, line=dict(color=color, dash=dash, width=1),
                  annotation_text=label,
                  annotation_font=dict(color=color, size=10))
    return fig


def add_hline(fig: go.Figure, y: float, label: str,
              color: str = AXIS_COLOR, dash: str = "dash") -> go.Figure:
    """Add a horizontal dashed reference line."""
    fig.add_hline(y=y, line=dict(color=color, dash=dash, width=1),
                  annotation_text=label,
                  annotation_font=dict(color=color, size=10))
    return fig


def clip_y(y: np.ndarray, y_max: float = 1e6) -> np.ndarray:
    """Clip extreme y values to prevent plotting artifacts."""
    return np.clip(y, -y_max, y_max)