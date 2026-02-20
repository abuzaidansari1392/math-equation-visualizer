"""
cubic.py
Handles y = ax³ + bx² + cx + d — computation and Plotly visualisation.

Mathematical Properties:
  • First derivative  : f'(x) = 3ax² + 2bx + c
  • Critical points   : where f'(x) = 0
  • Inflection point  : where f''(x) = 0  →  x = -b/(3a)

Time Complexity: O(n) for curve; O(n²) for root finding via companion matrix.
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.math_utils import (safe_linspace, find_critical_points,
                               find_inflection_points, polynomial_derivative)
from utils.plot_utils import (base_figure, add_curve, add_scatter_point,
                              VERTEX_COLOR, ROOT_COLOR, CRITICAL_COLOR, clip_y)


# ── Computation ──────────────────────────────────────────────────────────────

def compute_cubic(a: float, b: float, c: float, d: float,
                  x: np.ndarray) -> np.ndarray:
    """Evaluate y = ax³ + bx² + cx + d. O(n)."""
    return a * x**3 + b * x**2 + c * x + d


def cubic_derivative_coeffs(a: float, b: float, c: float) -> tuple[float, float, float]:
    """Return coefficients of f'(x) = 3ax² + 2bx + c."""
    return (3 * a, 2 * b, c)


def cubic_inflection(a: float, b: float) -> float | None:
    """
    Inflection point x where f''(x) = 0.
    f''(x) = 6ax + 2b  →  x = -b/(3a)
    """
    if abs(a) < 1e-12:
        return None
    return -b / (3 * a)


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_cubic(a: float, b: float, c: float, d: float,
               x_range: tuple[float, float]) -> go.Figure:
    """Build Plotly figure for y = ax³ + bx² + cx + d."""
    x = safe_linspace(*x_range, num=1000)
    y = clip_y(compute_cubic(a, b, c, d, x))

    title = f"Cubic: y = {a:.2f}x³ + {b:.2f}x² + {c:.2f}x + {d:.2f}"
    fig = base_figure(title=title)
    add_curve(fig, x, y, name="f(x)")

    # ── Derivative curve (dashed, dimmer) ──────────────────────────────────
    da, db, dc = cubic_derivative_coeffs(a, b, c)
    y_deriv = clip_y(da * x**2 + db * x + dc)
    fig.add_trace(go.Scatter(
        x=x, y=y_deriv, mode="lines", name="f'(x)",
        line=dict(color="#9B59B6", width=1.5, dash="dot"),
    ))

    coeffs = [a, b, c, d]

    # ── Critical points ────────────────────────────────────────────────────
    crit = find_critical_points(coeffs, x_range)
    for xc in crit:
        yc = compute_cubic(a, b, c, d, np.array([xc]))[0]
        add_scatter_point(fig, xc, yc,
                          label=f"Crit ({xc:.2f},{yc:.2f})",
                          color=CRITICAL_COLOR, symbol="triangle-up")

    # ── Inflection point ───────────────────────────────────────────────────
    xi = cubic_inflection(a, b)
    if xi is not None and x_range[0] <= xi <= x_range[1]:
        yi = compute_cubic(a, b, c, d, np.array([xi]))[0]
        add_scatter_point(fig, xi, yi,
                          label=f"Infl ({xi:.2f},{yi:.2f})",
                          color=VERTEX_COLOR, symbol="diamond")

    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_cubic():
    """Render sidebar controls, graph, and analysis for cubic equations."""
    st.sidebar.markdown("### ⚙️ Cubic Parameters")
    a = st.sidebar.slider("a (x³ coeff)", -5.0, 5.0, 1.0, 0.1)
    b = st.sidebar.slider("b (x² coeff)", -10.0, 10.0, 0.0, 0.1)
    c = st.sidebar.slider("c (x coeff)", -10.0, 10.0, -3.0, 0.1)
    d = st.sidebar.slider("d (constant)", -10.0, 10.0, 0.0, 0.1)
    x_min = st.sidebar.slider("X min", -20.0, 0.0, -5.0, 0.5)
    x_max = st.sidebar.slider("X max", 0.0, 20.0, 5.0, 0.5)

    coeffs = [a, b, c, d]
    da, db, dc = cubic_derivative_coeffs(a, b, c)
    crit = find_critical_points(coeffs, (x_min, x_max))
    xi = cubic_inflection(a, b)

    # ── Graph ──
    st.plotly_chart(plot_cubic(a, b, c, d, (x_min, x_max)),
                    use_container_width=True)

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")

    st.markdown(rf"""
**Equation:** $y = {a:.2f}x^3 + {b:.2f}x^2 + {c:.2f}x + {d:.2f}$

**First Derivative:** $f'(x) = {da:.2f}x^2 + {db:.2f}x + {dc:.2f}$

**Second Derivative:** $f''(x) = {6*a:.2f}x + {2*b:.2f}$
""")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Critical Points** (f'(x) = 0)")
        if crit:
            for xc in crit:
                yc = compute_cubic(a, b, c, d, np.array([xc]))[0]
                st.markdown(f"  - $x = {xc:.4f}$, $y = {yc:.4f}$")
        else:
            st.info("No critical points in range.")

    with col2:
        st.markdown("**Inflection Point** (f''(x) = 0)")
        if xi is not None:
            yi = compute_cubic(a, b, c, d, np.array([xi]))[0]
            st.markdown(f"$x = {xi:.4f}$, $y = {yi:.4f}$")
        else:
            st.info("No inflection point (a ≈ 0).")