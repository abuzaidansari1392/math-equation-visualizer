# 📈 Dynamic Mathematical Equation Visualizer

> **BTech CSE Mini-Project** | Real-Time Parameter Manipulation  
> Built with Python · Streamlit · Plotly · NumPy

---

## 🖥️ Demo Screenshot

The application provides a dark, academic-grade interface with a left sidebar for parameter control and a main panel for interactive Plotly graphs + mathematical analysis.

---

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip

### Steps

```bash
# 1. Clone / download the project
git clone <repo-url>
cd math_visualizer

# 2. (Recommended) Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run the application
streamlit run app.py
```

The app will open automatically at `http://localhost:8501`.

---

## 🏗️ Project Structure

```
math_visualizer/
│
├── app.py                      # Streamlit entry point — routing + UI shell
│
├── modules/
│   ├── __init__.py
│   ├── linear.py               # y = mx + c
│   ├── quadratic.py            # y = ax² + bx + c
│   ├── cubic.py                # y = ax³ + bx² + cx + d
│   ├── polynomial.py           # y = aₙxⁿ + ... + a₀  (degree 1–6)
│   ├── ellipse.py              # x²/a² + y²/b² = 1
│   └── trigonometric.py       # y = A·sin/cos(Bx + C)
│
├── utils/
│   ├── __init__.py
│   ├── math_utils.py           # Shared computation helpers
│   └── plot_utils.py           # Shared Plotly theming helpers
│
├── requirements.txt
└── README.md
```

---

## ✨ Features by Equation Type

### 1. Linear — `y = mx + c`
- Sliders for slope `m` and y-intercept `c`
- Shows slope, y-intercept, x-intercept
- Marks intercept points on graph

### 2. Quadratic — `y = ax² + bx + c`
- Sliders for `a`, `b`, `c`
- Computes discriminant D = b² − 4ac
- Shows nature of roots (real/complex/repeated)
- Marks vertex and axis of symmetry
- Plots real roots as X markers

### 3. Cubic — `y = ax³ + bx² + cx + d`
- Full parameter control
- Overlays first derivative f'(x) curve
- Detects and marks critical points (f'(x)=0)
- Detects and marks inflection point (f''(x)=0)

### 4. Polynomial — degree 1–6
- Dynamic degree selector (1–6)
- Auto-generates coefficient sliders per degree
- Root detection via companion-matrix eigenvalues
- Coefficient table display

### 5. Ellipse — `x²/a² + y²/b² = 1`
- Semi-axis sliders `a` and `b`
- Equal-aspect-ratio plot (no distortion)
- Shows foci, vertices, axis lines
- Computes area, eccentricity, focal distance
- Detects circle as special case (a = b)

### 6. Trigonometric — `y = A·sin/cos(Bx + C)`
- Switch between sin and cos
- Amplitude, frequency, phase sliders
- Shows amplitude envelope lines
- Phase shift marker
- **Optional wave animation** (Play/Pause button)

---

## 🔬 Algorithm Explanations

### Root Finding (Polynomial)
Uses NumPy's `np.roots()` which internally constructs the **companion matrix** of the polynomial and finds its eigenvalues via the QR algorithm. Roots with imaginary part |Im| < 1e-8 are classified as real.

- **Time Complexity:** O(n³) — dominated by n×n eigenvalue decomposition

### Critical / Inflection Points (Cubic & Polynomial)
The derivative polynomial is computed symbolically by differentiating coefficients:
```
f(x) = aₙxⁿ + ... → f'(x) = n·aₙxⁿ⁻¹ + ...
```
Then `np.roots()` is called on the derivative to find zeros.

- **Time Complexity:** O(n³) for degree-n polynomial

### Quadratic Formula
```
D = b² - 4ac
x = (-b ± √D) / (2a)
```
Direct O(1) computation; edge cases (a=0, D<0) handled explicitly.

### Discriminant Analysis
| D > 0 | Two distinct real roots |
|-------|------------------------|
| D = 0 | One repeated real root |
| D < 0 | Two complex conjugate roots |

### Ellipse Parametric Rendering
```
x(t) = a·cos(t),  y(t) = b·sin(t),  t ∈ [0, 2π]
```
800 sample points ensure smooth curves. Equal aspect ratio enforced via Plotly's `scaleanchor`.

### Trigonometric Properties
```
Amplitude  = |A|
Period     = 2π / |B|
Frequency  = |B| / (2π)
Phase Shift= -C / B
```

---

## ⏱️ Time Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| Curve rendering (n points) | O(n) | NumPy vectorised |
| Polynomial root finding (degree d) | O(d³) | Companion matrix eigenvalues |
| Quadratic roots | O(1) | Direct formula |
| Cubic inflection point | O(1) | Analytical: x = -b/(3a) |
| Derivative computation | O(d) | Coefficient manipulation |
| Ellipse parametric | O(n) | Vectorised cos/sin |
| Trig animation (f frames, n points) | O(f·n) | Per-frame evaluation |

---

## 🚀 Future Scope

1. **3D Surface Plots** — Extend to z = f(x, y) for multivariable visualisation
2. **Differential Equations** — ODE solver integration (scipy.integrate.solve_ivp)
3. **Fourier Analysis** — Decompose signals into harmonic components
4. **Polar Coordinates** — r = f(θ) curves (rose curves, spirals, limaçons)
5. **Complex Function Visualisation** — Domain coloring for f: ℂ → ℂ
6. **Export** — Save graphs as PNG/SVG; export data as CSV
7. **Symbolic Math** — SymPy integration for exact symbolic derivatives
8. **Mobile Responsive** — Optimised layout for touch devices
9. **Multi-curve Overlay** — Plot multiple equations simultaneously for comparison
10. **AI Equation Parser** — Type equations in natural language, auto-parse to plot

---

## 🛠️ Technologies Used

| Library | Version | Role |
|---------|---------|------|
| Python | ≥ 3.10 | Core language |
| Streamlit | ≥ 1.32 | Web UI framework |
| Plotly | ≥ 5.20 | Interactive charts |
| NumPy | ≥ 1.26 | Numerical computation |
| Pandas | ≥ 2.2 | Coefficient table display |

---

## 📄 License

MIT License — Free for academic and personal use.

---

*Developed as a BTech CSE Mini-Project demonstrating real-time mathematical visualisation with modular Python architecture.*