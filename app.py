"""
app.py — Dynamic Mathematical Equation Visualizer
===================================================
Entry point for the Streamlit application.

Architecture:
  - Sidebar : equation selector + parameter sliders (delegated to each module)
  - Main panel : interactive Plotly graph
  - Analysis panel : computed mathematical properties

Run:
  streamlit run app.py
"""

import streamlit as st

# ── Page config (must be first Streamlit call) ────────────────────────────────
st.set_page_config(
    page_title="Math Equation Visualizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Module imports ────────────────────────────────────────────────────────────
from modules.linear        import render_linear
from modules.quadratic     import render_quadratic
from modules.cubic         import render_cubic
from modules.polynomial    import render_polynomial
from modules.ellipse       import render_ellipse
from modules.trigonometric import render_trigonometric

# ── Custom CSS — dark academic theme ─────────────────────────────────────────
st.markdown("""
<style>
/* Import Fira Code for monospace code feel */
@import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;500;600&family=Playfair+Display:wght@400;700&display=swap');

/* Root palette */
:root {
    --bg-primary:   #293548;
    --bg-secondary: #161B22;
    --bg-tertiary:  #21262D;
    --accent-cyan:  #00C9FF;
    --accent-gold:  #FFD93D;
    --text-primary: #E6EDF3;
    --text-muted:   #8B949E;
    --border:       rgba(255,255,255,0.08);
}

/* Full app background */
.stApp { background-color: var(--bg-primary); }

/* Sidebar */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary);
    border-right: 1px solid var(--border);
}





            
/* Sidebar text only */
section[data-testid="stSidebar"] .stMarkdown,
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] span {
    color: var(--text-primary);
}

/* Sidebar selectbox text */
section[data-testid="stSidebar"] div[data-baseweb="select"] {
    color: var(--text-primary);
}

/* Base button */
section[data-testid="stSidebar"] div[data-testid="stButton"] button {
    background-color: var(--bg-tertiary);
    color: white;
    transition: all 0.3s ease;
}

/* Hover */
section[data-testid="stSidebar"] div[data-testid="stButton"] button:hover {
    background-color: #ffffff;
    color: #000000 !important;
}





/* Main content */
.main .block-container { padding-top: 1.5rem; }

/* Headings */
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: var(--text-primary) !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: var(--bg-tertiary);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 0.75rem 1rem;
}
[data-testid="stMetricValue"] {
    font-family: 'Fira Code', monospace !important;
    color: var(--accent-cyan) !important;
    font-size: 1.1rem !important;
}
[data-testid="stMetricLabel"] { color: var(--text-muted) !important; }

/* Dataframes */
.dataframe { background: var(--bg-tertiary) !important; }

/* Info / success / warning boxes */
.stAlert { border-radius: 6px; font-family: 'Fira Code', monospace; }

/* Slider label */
.stSlider label { font-family: 'Fira Code', monospace !important; font-size: 0.85rem !important; }

/* Horizontal rule */
hr { border-color: var(--border) !important; margin: 1rem 0; }

/* Header banner */
.header-banner {
    background: linear-gradient(135deg, #0D1117 0%, #161B22 50%, #0D1117 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem 2rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.header-banner::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-gold), transparent);
}
.header-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    color: var(--text-primary);
    margin: 0;
    letter-spacing: 0.02em;
}
.header-subtitle {
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    color: var(--text-muted);
    margin-top: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="header-banner">
  <p class="header-title">📈 Dynamic Mathematical Equation Visualizer</p>
  <p class="header-subtitle">
    BTech CSE Mini-Project &nbsp;·&nbsp; Real-Time Parameter Manipulation
    &nbsp;·&nbsp; Powered by Python · Streamlit · Plotly · NumPy
  </p>
</div>
""", unsafe_allow_html=True)

# ── Sidebar — equation selector ───────────────────────────────────────────────
st.sidebar.markdown("""
<div style='text-align:center; padding: 0.5rem 0 1rem; 
            font-family: Playfair Display, serif; font-size: 1.1rem;
            color: #E6EDF3; border-bottom: 1px solid rgba(255,255,255,0.08);
            margin-bottom: 1rem;'>
📐 Equation Visualizer
</div>
""", unsafe_allow_html=True)

EQUATION_OPTIONS = {
    "📏  Linear          — y = mx + c":          "Linear",
    "📐  Quadratic       — y = ax² + bx + c":    "Quadratic",
    "🌀  Cubic           — y = ax³ + bx² + cx + d": "Cubic",
    "🔢  Polynomial      — degree 1 – 6":         "Polynomial",
    "⭕  Ellipse         — x²/a² + y²/b² = 1":   "Ellipse",
    "〰️  Trigonometric   — A·sin/cos(Bx+C)":     "Trigonometric",
}

selected_label = st.sidebar.selectbox(
    "Select Equation Type",
    options=list(EQUATION_OPTIONS.keys()),
    index=0,
)
selected = EQUATION_OPTIONS[selected_label]

# ── Reset button ──────────────────────────────────────────────────────────────
if st.sidebar.button("🔄 Reset Parameters", use_container_width=True):
    # Clear all widget state so sliders return to defaults
    keys_to_clear = [k for k in st.session_state if k.startswith("poly_coeff_")
                     or k in ("poly_degree",)]
    for k in keys_to_clear:
        del st.session_state[k]
    st.rerun()

st.sidebar.markdown("---")

# ── Dispatch to the selected module ──────────────────────────────────────────
RENDERERS = {
    "Linear":         render_linear,
    "Quadratic":      render_quadratic,
    "Cubic":          render_cubic,
    "Polynomial":     render_polynomial,
    "Ellipse":        render_ellipse,
    "Trigonometric":  render_trigonometric,
}

RENDERERS[selected]()

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='text-align:center; font-family: Fira Code, monospace; "
    "font-size:0.75rem; color:#8B949E;'>"
    "Dynamic Mathematical Equation Visualizer &nbsp;·&nbsp; "
    "BTech CSE Mini-Project &nbsp;·&nbsp; Built with ❤️ using Python + Streamlit + Plotly"
    "</p>",
    unsafe_allow_html=True,
)