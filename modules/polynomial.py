"""
polynomial.py
Handles general polynomial y = a_n x^n + ... + a_0 for degree 1–6.

Features:
  • Dynamic degree selection
  • Auto-generated coefficient sliders
  • Real root detection via companion matrix eigenvalues
  • Curve plotting with root markers

Time Complexity:
  • Evaluation: O(n·N) — n = degree, N = sample points (Horner's method internally)
  • Root finding: O(n³) — eigenvalue decomposition of n×n companion matrix
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.math_utils import safe_linspace, find_real_roots, polynomial_value
from utils.plot_utils import (base_figure, add_curve, add_scatter_point,
                              clip_y, ROOT_COLOR, VERTEX_COLOR)


# ── Computation ──────────────────────────────────────────────────────────────

def build_coeffs_from_sidebar(degree: int) -> list[float]:
    """
    Dynamically create Streamlit sliders for each coefficient and return
    coefficient list [a_n, ..., a_0] (highest degree first).
    """
    coeffs = []
    for k in range(degree, -1, -1):
        label = f"a_{k} (x^{k} coeff)" if k > 1 else (f"a_{k} (x coeff)" if k == 1 else "a_0 (constant)")
        default = 1.0 if k == degree else 0.0
        val = st.sidebar.slider(label, -10.0, 10.0, default, 0.1,
                                key=f"poly_coeff_{k}")
        coeffs.append(val)   # highest degree first
    return coeffs


def build_poly_title(coeffs: list[float]) -> str:
    """Construct a human-readable polynomial title string."""
    n = len(coeffs) - 1
    terms = []
    for i, c in enumerate(coeffs):
        deg = n - i
        if abs(c) < 1e-12:
            continue
        if deg == 0:
            terms.append(f"{c:.2f}")
        elif deg == 1:
            terms.append(f"{c:.2f}x")
        else:
            terms.append(f"{c:.2f}x^{deg}")
    return "y = " + " + ".join(terms) if terms else "y = 0"


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_polynomial(coeffs: list[float], x_range: tuple[float, float]) -> go.Figure:
    """Build Plotly figure for the polynomial with given coefficients."""
    x = safe_linspace(*x_range, num=1200)
    y = clip_y(polynomial_value(coeffs, x))

    title = build_poly_title(coeffs)
    fig = base_figure(title=f"Polynomial: {title}")
    add_curve(fig, x, y, name="P(x)")

    # Real roots
    roots = find_real_roots(coeffs)
    for r in roots:
        if x_range[0] <= r <= x_range[1]:
            add_scatter_point(fig, r, 0,
                              label=f"Root ({r:.3f})",
                              color=ROOT_COLOR, symbol="x")

    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_polynomial():
    """Render sidebar controls, graph, and analysis for general polynomials."""
    st.sidebar.markdown("### ⚙️ Polynomial Parameters")
    degree = st.sidebar.selectbox("Polynomial Degree", options=list(range(1, 7)),
                                   index=3, key="poly_degree")

    coeffs = build_coeffs_from_sidebar(degree)

    x_min = st.sidebar.slider("X min", -50.0, 0.0, -5.0, 0.5)
    x_max = st.sidebar.slider("X max", 0.0, 50.0, 5.0, 0.5)

    roots = find_real_roots(coeffs)
    real_roots_in_range = [r for r in roots if x_min <= r <= x_max]

    # ── Graph ──
    st.plotly_chart(plot_polynomial(coeffs, (x_min, x_max)),
                    use_container_width=True)

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")

    n = len(coeffs) - 1
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"**Degree:** {n}")
        st.markdown(f"**Leading Coefficient:** {coeffs[0]:.4f}")
        end = "→ +∞" if coeffs[0] > 0 else "→ −∞"
        st.markdown(f"**End Behavior (x→+∞):** y {end}")

    with col2:
        st.markdown(f"**Number of Real Roots:** {len(roots)}")
        if real_roots_in_range:
            for r in real_roots_in_range:
                st.markdown(f"  - $x ≈ {r:.6f}$")
        else:
            st.info("No real roots in selected range.")

    st.markdown("**Coefficient Table:**")
    coeff_table = {f"x^{n-i}": [f"{c:.4f}"] for i, c in enumerate(coeffs)}
    import pandas as pd
    st.dataframe(pd.DataFrame(coeff_table), use_container_width=True)