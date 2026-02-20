"""
quadratic.py
Handles y = ax² + bx + c — computation and Plotly visualisation.

Mathematical Properties:
  • Discriminant D = b² − 4ac
  • Roots via quadratic formula
  • Vertex at (−b/2a, f(−b/2a))
  • Axis of symmetry: x = −b/2a

Time Complexity: O(n) for curve; O(1) for root/vertex computation.
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.math_utils import (safe_linspace, quadratic_discriminant,
                               quadratic_roots, quadratic_vertex)
from utils.plot_utils import (base_figure, add_curve, add_scatter_point,
                              add_vline, VERTEX_COLOR, ROOT_COLOR, CRITICAL_COLOR)


# ── Computation ──────────────────────────────────────────────────────────────

def compute_quadratic(a: float, b: float, c: float, x: np.ndarray) -> np.ndarray:
    """Evaluate y = ax² + bx + c. O(n)."""
    return a * x**2 + b * x + c


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_quadratic(a: float, b: float, c: float,
                   x_range: tuple[float, float]) -> go.Figure:
    """Build Plotly figure for the quadratic equation."""
    x = safe_linspace(*x_range)
    y = compute_quadratic(a, b, c, x)

    sign_b = "+" if b >= 0 else "−"
    sign_c = "+" if c >= 0 else "−"
    title = f"Quadratic: y = {a:.2f}x² {sign_b} {abs(b):.2f}x {sign_c} {abs(c):.2f}"
    fig = base_figure(title=title)
    add_curve(fig, x, y, name="y = ax²+bx+c")

    # Vertex
    vx, vy = quadratic_vertex(a, b, c)
    add_scatter_point(fig, vx, vy, label=f"Vertex ({vx:.2f},{vy:.2f})",
                      color=VERTEX_COLOR, symbol="star")

    # Axis of symmetry
    if x_range[0] <= vx <= x_range[1]:
        add_vline(fig, vx, label=f"x={vx:.2f}", color=VERTEX_COLOR)

    # Roots
    _, roots = quadratic_roots(a, b, c)
    for i, r in enumerate(roots):
        if x_range[0] <= r <= x_range[1]:
            add_scatter_point(fig, r, 0,
                              label=f"Root {i+1} ({r:.3f})",
                              color=ROOT_COLOR, symbol="x")

    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_quadratic():
    """Render sidebar controls, graph, and analysis for quadratic equations."""
    st.sidebar.markdown("### ⚙️ Quadratic Parameters")
    a = st.sidebar.slider("a (x² coeff)", -5.0, 5.0, 1.0, 0.1)
    b = st.sidebar.slider("b (x coeff)", -10.0, 10.0, 0.0, 0.1)
    c = st.sidebar.slider("c (constant)", -10.0, 10.0, 0.0, 0.1)
    x_min = st.sidebar.slider("X min", -50.0, 0.0, -10.0, 1.0)
    x_max = st.sidebar.slider("X max", 0.0, 50.0, 10.0, 1.0)

    if abs(a) < 1e-12:
        st.sidebar.warning("⚠️ a ≈ 0 — equation becomes linear.")

    D          = quadratic_discriminant(a, b, c)
    nature, roots = quadratic_roots(a, b, c)
    vx, vy     = quadratic_vertex(a, b, c)

    # ── Graph ──
    st.plotly_chart(plot_quadratic(a, b, c, (x_min, x_max)),
                    use_container_width=True)

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Discriminant (D)", f"{D:.4f}")
    with col2:
        st.metric("Vertex X", f"{vx:.4f}")
    with col3:
        st.metric("Vertex Y", f"{vy:.4f}")

    # Nature of roots
    if D > 1e-10:
        st.success(f"✅ {nature}")
    elif abs(D) <= 1e-10:
        st.info(f"ℹ️ {nature}")
    else:
        st.warning(f"⚠️ {nature}")

    if roots:
        st.markdown("**Roots:**")
        for i, r in enumerate(roots):
            st.markdown(f"  - $x_{i+1} = {r:.6f}$")

    opening = "upward ∪" if a > 0 else "downward ∩" if a < 0 else "flat (degenerate)"
    st.markdown(rf"""
**Equation:** $y = {a:.2f}x^2 + {b:.2f}x + {c:.2f}$

| Property | Value |
|----------|-------|
| Discriminant | $D = {D:.4f}$ |
| Vertex | $\left({vx:.4f},\ {vy:.4f}\right)$ |
| Axis of Symmetry | $x = {vx:.4f}$ |
| Parabola Opens | {opening} |
""")