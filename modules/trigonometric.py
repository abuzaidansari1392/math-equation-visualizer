"""
trigonometric.py
Handles  y = A·sin(Bx + C)  and  y = A·cos(Bx + C).

Mathematical Properties:
  • Amplitude     : |A|
  • Angular freq  : B  (radians per unit x)
  • Period        : 2π/|B|
  • Phase shift   : −C/B  (horizontal shift)
  • Frequency     : B/(2π)

Animation: optional frame-by-frame phase animation using Plotly frames.

Time Complexity: O(n) per frame for n sample points.
"""

import numpy as np
import streamlit as st
import plotly.graph_objects as go

from utils.math_utils import safe_linspace
from utils.plot_utils import (base_figure, add_curve, add_hline,
                               CURVE_COLOR, VERTEX_COLOR, ROOT_COLOR)


# ── Computation ──────────────────────────────────────────────────────────────

def compute_trig(A: float, B: float, C: float,
                 func: str, x: np.ndarray) -> np.ndarray:
    """
    Evaluate y = A·sin(Bx+C) or y = A·cos(Bx+C).
    func: 'sin' | 'cos'
    """
    if B == 0:
        return np.zeros_like(x)
    arg = B * x + C
    if func == "sin":
        return A * np.sin(arg)
    elif func == "cos":
        return A * np.cos(arg)
    else:
        raise ValueError(f"Unknown trig function: {func}")


def trig_properties(A: float, B: float, C: float) -> dict:
    """Compute standard trigonometric properties."""
    if abs(B) < 1e-12:
        return {
            "amplitude": abs(A),
            "period": float("inf"),
            "frequency": 0.0,
            "phase_shift": 0.0,
            "angular_freq": 0.0,
        }
    return {
        "amplitude": abs(A),
        "angular_freq": B,
        "period": 2 * np.pi / abs(B),
        "frequency": abs(B) / (2 * np.pi),
        "phase_shift": -C / B,
    }


# ── Plotting ─────────────────────────────────────────────────────────────────

def plot_trig(A: float, B: float, C: float,
              func: str, x_range: tuple[float, float],
              show_animation: bool = False) -> go.Figure:
    """Build Plotly figure for the trigonometric equation."""
    x = safe_linspace(*x_range, num=1000)
    y = compute_trig(A, B, C, func, x)

    fn_str = "sin" if func == "sin" else "cos"
    B_str  = f"{B:.2f}"
    C_str  = f"+{C:.2f}" if C >= 0 else f"{C:.2f}"
    title  = f"Trig: y = {A:.2f}·{fn_str}({B_str}x {C_str})"

    if show_animation:
        return _animated_plot(A, B, C, func, x, title)

    fig = base_figure(title=title)
    add_curve(fig, x, y, name=f"y={A:.2f}·{fn_str}({B_str}x{C_str})")

    props = trig_properties(A, B, C)

    # Amplitude lines
    add_hline(fig, A, label=f"Amp +{A:.2f}", color=VERTEX_COLOR, dash="dot")
    add_hline(fig, -A, label=f"Amp −{A:.2f}", color=VERTEX_COLOR, dash="dot")

    # Phase shift marker
    ps = props["phase_shift"]
    if x_range[0] <= ps <= x_range[1]:
        y_ps = compute_trig(A, B, C, func, np.array([ps]))[0]
        fig.add_trace(go.Scatter(
            x=[ps], y=[y_ps], mode="markers+text",
            name=f"Phase shift x={ps:.2f}",
            text=[f"  Phase ({ps:.2f})"],
            textposition="top right",
            textfont=dict(color=ROOT_COLOR, size=10),
            marker=dict(color=ROOT_COLOR, size=9, symbol="triangle-right"),
        ))

    return fig


def _animated_plot(A: float, B: float, C: float,
                   func: str, x: np.ndarray, title: str) -> go.Figure:
    """
    Create an animated Plotly figure that sweeps the phase C from 0 → 2π.
    Each frame shifts the wave, creating a travelling-wave animation.
    """
    fn = np.sin if func == "sin" else np.cos
    n_frames = 60
    phase_sweep = np.linspace(0, 2 * np.pi, n_frames)

    frames = []
    for phi in phase_sweep:
        y_frame = A * fn(B * x + C + phi)
        frames.append(go.Frame(
            data=[go.Scatter(x=x, y=y_frame, mode="lines",
                             line=dict(color=CURVE_COLOR, width=2.5))],
        ))

    y0 = A * fn(B * x + C)
    fig = go.Figure(
        data=[go.Scatter(x=x, y=y0, mode="lines",
                         line=dict(color=CURVE_COLOR, width=2.5),
                         name=title)],
        frames=frames,
        layout=go.Layout(
            title=dict(text=f"🎬 Animated: {title}",
                       font=dict(size=16, color="#E6EDF3")),
            paper_bgcolor="#0D1117",
            plot_bgcolor="#161B22",
            font=dict(color="#E6EDF3", family="Fira Code, monospace"),
            xaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)",
                       zeroline=True, zerolinecolor="rgba(255,255,255,0.35)"),
            yaxis=dict(showgrid=True, gridcolor="rgba(255,255,255,0.08)",
                       zeroline=True, zerolinecolor="rgba(255,255,255,0.35)"),
            updatemenus=[dict(
                type="buttons", showactive=False,
                buttons=[
                    dict(label="▶ Play",
                         method="animate",
                         args=[None, dict(frame=dict(duration=50, redraw=True),
                                          fromcurrent=True, loop=True)]),
                    dict(label="⏸ Pause",
                         method="animate",
                         args=[[None], dict(frame=dict(duration=0),
                                             mode="immediate")]),
                ],
                x=0.1, y=1.1, bgcolor="#21262D",
                font=dict(color="#E6EDF3"),
            )],
        ),
    )
    return fig


# ── Streamlit UI ─────────────────────────────────────────────────────────────

def render_trigonometric():
    """Render sidebar controls, graph, and analysis for trig equations."""
    st.sidebar.markdown("### ⚙️ Trigonometric Parameters")
    func = st.sidebar.radio("Function", ["sin", "cos"], horizontal=True)
    A    = st.sidebar.slider("Amplitude (A)", -5.0, 5.0, 1.0, 0.1)
    B    = st.sidebar.slider("Angular Frequency (B)", -4.0, 4.0, 1.0, 0.1)
    C    = st.sidebar.slider("Phase (C, radians)", -np.pi, np.pi, 0.0, 0.05)
    x_min = st.sidebar.slider("X min", -4*np.pi, 0.0, -2*np.pi, 0.1)
    x_max = st.sidebar.slider("X max", 0.0, 4*np.pi, 2*np.pi, 0.1)
    animate = st.sidebar.checkbox("🎬 Animate Phase Sweep", value=False)

    if abs(B) < 1e-12:
        st.sidebar.warning("⚠️ B ≈ 0 — function becomes flat line (y = A).")

    props = trig_properties(A, B, C)

    # ── Graph ──
    st.plotly_chart(
        plot_trig(A, B, C, func, (x_min, x_max), show_animation=animate),
        use_container_width=True,
    )

    # ── Analysis Panel ──
    st.markdown("---")
    st.markdown("### 📐 Mathematical Analysis")

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Amplitude |A|", f"{props['amplitude']:.4f}")
    with col2:
        period_str = f"{props['period']:.4f}" if props['period'] != float("inf") else "∞"
        st.metric("Period T", period_str)
    with col3:
        st.metric("Frequency (Hz)", f"{props['frequency']:.4f}")
    with col4:
        st.metric("Phase Shift", f"{props['phase_shift']:.4f} rad")

    fn_label = "sin" if func == "sin" else "cos"
    C_str = f"+{C:.3f}" if C >= 0 else f"{C:.3f}"
    st.markdown(rf"""
**Equation:** $y = {A:.2f} \cdot \{fn_label}\!\left({B:.2f}x {C_str}\right)$

| Property | Formula | Value |
|----------|---------|-------|
| Amplitude | $|A|$ | ${props['amplitude']:.4f}$ |
| Angular Frequency | $B$ | ${B:.4f}$ rad/unit |
| Period | $T = 2\pi / |B|$ | ${period_str}$ |
| Frequency | $f = |B|/(2\pi)$ | ${props['frequency']:.4f}$ Hz |
| Phase Shift | $-C/B$ | ${props['phase_shift']:.4f}$ units |
| Vertical Range | $[-|A|,\ |A|]$ | $[{-abs(A):.4f},\ {abs(A):.4f}]$ |
""")

    if animate:
        st.info("🎬 Animation mode active — use ▶ Play button on the chart.")