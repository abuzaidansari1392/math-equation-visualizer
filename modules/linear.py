"""
linear.py
Handles y = mx + c — computation and Plotly visualisation.

Mathematical Properties:
  • Slope  : m  (rate of change)
  • Y-intercept : c  (value at x=0)
  • X-intercept : -c/m  (root, when m≠0)

Time Complexity: O(n) for n sample points.
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.math_utils import safe_linspace
from utils.plot_utils import (base_figure, add_curve, add_scatter_point,
                              VERTEX_COLOR, ROOT_COLOR)


# ── Computation ──────────────────────────────────────────────────────────────

def compute_linear(m: float, c: float, x: np.ndarray) -> np.ndarray:
    """Evaluate y = mx + c at each x. O(n)."""
    return m * x + c


def linear_properties(m: float, c: float) -> dict:
    """Return a dict of mathematical properties for the linear equation."""
    props = {
        "slope": m,
        "y_intercept": c,
        "x_intercept": None,
        "parallel_to_x": False,
        "is_vertical": False,
    }
    if abs(m) < 1e-12:
        props["parallel_to_x"] = True
    else:
        props["x_intercept"] = -c / m
    return props


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_linear(m: float, c: float, x_range: tuple[float, float]) -> go.Figure:
    """Build and return a Plotly figure for y = mx + c."""
    x = safe_linspace(*x_range)
    y = compute_linear(m, c, x)

    title = f"Linear: y = {m:.2f}x + {c:.2f}" if c >= 0 else f"Linear: y = {m:.2f}x − {abs(c):.2f}"
    fig = base_figure(title=title)
    add_curve(fig, x, y, name="y = mx + c")

    props = linear_properties(m, c)

    # Mark y-intercept
    add_scatter_point(fig, 0, c, label=f"y-int ({c:.2f})",
                      color=VERTEX_COLOR, symbol="diamond")

    # Mark x-intercept (root) if it exists
    if props["x_intercept"] is not None:
        xi = props["x_intercept"]
        if x_range[0] <= xi <= x_range[1]:
            add_scatter_point(fig, xi, 0, label=f"x-int ({xi:.2f})",
                              color=ROOT_COLOR, symbol="x")

    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_linear():
    """Render sidebar controls, graph, and analysis panel for linear equations."""
    st.sidebar.markdown("### ⚙️ Linear Parameters")
    m = st.sidebar.slider("Slope (m)", -10.0, 10.0, 1.0, 0.1)
    c = st.sidebar.slider("Y-Intercept (c)", -10.0, 10.0, 0.0, 0.1)
    x_min = st.sidebar.slider("X min", -50.0, 0.0, -10.0, 1.0)
    x_max = st.sidebar.slider("X max", 0.0, 50.0, 10.0, 1.0)

    props = linear_properties(m, c)

    # ── Graph ──
    st.plotly_chart(plot_linear(m, c, (x_min, x_max)),
                    use_container_width=True)

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Slope (m)", f"{props['slope']:.4f}")
    with col2:
        st.metric("Y-Intercept", f"{props['y_intercept']:.4f}")
    with col3:
        xi = props.get("x_intercept")
        st.metric("X-Intercept", f"{xi:.4f}" if xi is not None else "∞ (m=0)")

    st.markdown(r"""
**Equation:**  $y = mx + c$

| Property | Value |
|----------|-------|
| Slope | $m = """ + f"{m:.4f}" + r"""$ |
| Y-Intercept | $c = """ + f"{c:.4f}" + r"""$ |
| Direction | """ + ("Increasing ↑" if m > 0 else "Decreasing ↓" if m < 0 else "Horizontal →") + """ |
""")

    if props["parallel_to_x"]:
        st.info("ℹ️ Line is horizontal (parallel to x-axis). No x-intercept exists.")
    else:
        st.success(f"✅ X-Intercept at x = {props['x_intercept']:.4f}")