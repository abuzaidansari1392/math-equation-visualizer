"""
ellipse.py
Handles the ellipse equation  x²/a² + y²/b² = 1.

Mathematical Properties:
  • Semi-major axis : max(a, b)
  • Semi-minor axis : min(a, b)
  • Area            : π·a·b
  • Eccentricity    : e = √(1 − min²/max²)
  • Foci            : located along the major axis

Parametric form used for plotting:
  x(t) = a·cos(t),  y(t) = b·sin(t),  t ∈ [0, 2π]

Time Complexity: O(n) for n sample points of the parametric curve.
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.plot_utils import base_figure, CURVE_COLOR, ROOT_COLOR, VERTEX_COLOR


# ── Computation ──────────────────────────────────────────────────────────────

def ellipse_properties(a: float, b: float) -> dict:
    """Compute key geometric properties of the ellipse."""
    if abs(a) < 1e-9 or abs(b) < 1e-9:
        return {"error": "Semi-axes must be non-zero"}

    major = max(abs(a), abs(b))
    minor = min(abs(a), abs(b))
    area  = np.pi * abs(a) * abs(b)
    ecc   = np.sqrt(1 - (minor / major) ** 2) if major > 0 else 0.0
    c     = np.sqrt(max(abs(a)**2 - abs(b)**2, 0))   # focal distance

    return {
        "semi_major": major,
        "semi_minor": minor,
        "area": area,
        "eccentricity": ecc,
        "focal_distance": c,
        "major_axis_length": 2 * major,
        "minor_axis_length": 2 * minor,
        "major_axis_along": "x-axis" if abs(a) >= abs(b) else "y-axis",
    }


def parametric_ellipse(a: float, b: float, num: int = 800):
    """Return (x, y) parametric points of the ellipse."""
    t = np.linspace(0, 2 * np.pi, num)
    return a * np.cos(t), b * np.sin(t)


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_ellipse(a: float, b: float) -> go.Figure:
    """Build Plotly figure for the ellipse x²/a² + y²/b² = 1."""
    x, y = parametric_ellipse(a, b)

    title = f"Ellipse: x²/{a:.2f}² + y²/{b:.2f}² = 1"
    fig = base_figure(title=title, x_label="x", y_label="y")

    # Main ellipse curve (closed loop)
    fig.add_trace(go.Scatter(
        x=np.append(x, x[0]), y=np.append(y, y[0]),
        mode="lines", name="Ellipse",
        line=dict(color=CURVE_COLOR, width=3),
    ))

    props = ellipse_properties(a, b)
    if "error" in props:
        return fig

    # Vertices on major / minor axes
    vertices = [(a, 0, "A(a,0)"), (-a, 0, "A'(-a,0)"),
                (0, b, "B(0,b)"), (0, -b, "B'(0,-b)")]
    for vx, vy, label in vertices:
        fig.add_trace(go.Scatter(
            x=[vx], y=[vy], mode="markers+text",
            text=[f"  {label}"], textposition="top right",
            textfont=dict(color=VERTEX_COLOR, size=10),
            marker=dict(color=VERTEX_COLOR, size=8, symbol="diamond"),
            name=label, showlegend=False,
        ))

    # Foci (only meaningful when a ≠ b)
    c = props["focal_distance"]
    if c > 1e-6:
        if abs(a) >= abs(b):
            foci = [(c, 0), (-c, 0)]
        else:
            foci = [(0, c), (0, -c)]
        for fx, fy in foci:
            fig.add_trace(go.Scatter(
                x=[fx], y=[fy], mode="markers",
                name=f"Focus ({fx:.2f},{fy:.2f})",
                marker=dict(color=ROOT_COLOR, size=10, symbol="circle-open",
                            line=dict(color=ROOT_COLOR, width=2)),
            ))

    # Axes lines (major & minor)
    fig.add_shape(type="line", x0=-abs(a)*1.1, x1=abs(a)*1.1, y0=0, y1=0,
                  line=dict(color="rgba(255,255,255,0.2)", dash="dash"))
    fig.add_shape(type="line", x0=0, x1=0, y0=-abs(b)*1.1, y1=abs(b)*1.1,
                  line=dict(color="rgba(255,255,255,0.2)", dash="dash"))

    # Equal aspect ratio so ellipse isn't distorted
    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=1))

    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_ellipse():
    """Render sidebar controls, graph, and analysis for ellipses."""
    st.sidebar.markdown("### ⚙️ Ellipse Parameters")
    a = st.sidebar.slider("Semi-axis a (x-direction)", 0.5, 10.0, 5.0, 0.1)
    b = st.sidebar.slider("Semi-axis b (y-direction)", 0.5, 10.0, 3.0, 0.1)

    props = ellipse_properties(a, b)

    # ── Graph ──
    st.plotly_chart(plot_ellipse(a, b), use_container_width=True)

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Area (πab)", f"{props['area']:.4f}")
    with col2:
        st.metric("Eccentricity", f"{props['eccentricity']:.4f}")
    with col3:
        st.metric("Focal Distance c", f"{props['focal_distance']:.4f}")

    st.markdown(rf"""
**Equation:** $\dfrac{{x^2}}{{{a:.2f}^2}} + \dfrac{{y^2}}{{{b:.2f}^2}} = 1$

| Property | Value |
|----------|-------|
| Semi-Major Axis | ${props['semi_major']:.4f}$ |
| Semi-Minor Axis | ${props['semi_minor']:.4f}$ |
| Major Axis Length | ${props['major_axis_length']:.4f}$ |
| Minor Axis Length | ${props['minor_axis_length']:.4f}$ |
| Major Axis Direction | {props['major_axis_along']} |
| Area | $\pi \cdot {a:.2f} \cdot {b:.2f} = {props['area']:.4f}$ |
| Eccentricity | ${props['eccentricity']:.6f}$ |
| Focal Distance | $c = {props['focal_distance']:.4f}$ |
""")

    if abs(a - b) < 1e-6:
        st.success("✅ a = b → This is a **Circle** (special case of ellipse).")