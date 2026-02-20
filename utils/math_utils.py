"""
math_utils.py
Shared mathematical computation utilities used across all equation modules.
Time Complexity Notes:
- Root finding via numpy: O(n^3) for degree-n polynomials (eigenvalue decomposition)
- Critical point finding via derivative: O(n) for degree-n polynomial
"""

import numpy as np


def safe_linspace(start: float, end: float, num: int = 1000) -> np.ndarray:
    """Generate evenly spaced points, guarding against invalid ranges."""
    if start >= end:
        end = start + 1e-6
    return np.linspace(start, end, num)


def find_real_roots(coefficients: list[float]) -> list[float]:
    """
    Find real roots of a polynomial with given coefficients (highest degree first).
    Uses numpy's companion-matrix eigenvalue method.
    Returns list of real roots (imaginary part < 1e-8).
    Time Complexity: O(n^3) for degree-n polynomial.
    """
    roots = np.roots(coefficients)
    real_roots = [r.real for r in roots if abs(r.imag) < 1e-8]
    return sorted(real_roots)


def polynomial_value(coeffs: list[float], x: np.ndarray) -> np.ndarray:
    """
    Evaluate polynomial with given coefficients at points x.
    coeffs: [a_n, a_{n-1}, ..., a_0] (highest degree first)
    Uses Horner's method: O(n) per point.
    """
    return np.polyval(coeffs, x)


def polynomial_derivative(coeffs: list[float]) -> list[float]:
    """
    Return coefficients of the derivative polynomial.
    Input: [a_n, ..., a_0], Output: [n*a_n, ..., a_1]
    Time Complexity: O(n)
    """
    n = len(coeffs)
    if n <= 1:
        return [0.0]
    return [coeffs[i] * (n - 1 - i) for i in range(n - 1)]


def find_critical_points(coeffs: list[float], x_range: tuple[float, float]) -> list[float]:
    """
    Find critical points (where derivative = 0) within x_range.
    Returns list of x-values where f'(x) ≈ 0.
    """
    deriv = polynomial_derivative(coeffs)
    if all(c == 0 for c in deriv):
        return []
    roots = find_real_roots(deriv)
    return [r for r in roots if x_range[0] <= r <= x_range[1]]


def find_inflection_points(coeffs: list[float], x_range: tuple[float, float]) -> list[float]:
    """
    Find inflection points (where second derivative = 0) within x_range.
    """
    deriv1 = polynomial_derivative(coeffs)
    deriv2 = polynomial_derivative(deriv1)
    if all(c == 0 for c in deriv2):
        return []
    roots = find_real_roots(deriv2)
    return [r for r in roots if x_range[0] <= r <= x_range[1]]


def quadratic_discriminant(a: float, b: float, c: float) -> float:
    """Compute discriminant D = b² - 4ac for quadratic ax²+bx+c."""
    return b ** 2 - 4 * a * c


def quadratic_roots(a: float, b: float, c: float) -> tuple[str, list[float]]:
    """
    Compute roots of quadratic. Returns (nature_string, [roots]).
    Handles degenerate case a=0.
    """
    if abs(a) < 1e-12:
        if abs(b) < 1e-12:
            return "Constant (no roots)", []
        return "Linear (one root)", [-c / b]

    D = quadratic_discriminant(a, b, c)
    if D > 0:
        r1 = (-b + np.sqrt(D)) / (2 * a)
        r2 = (-b - np.sqrt(D)) / (2 * a)
        return f"Two distinct real roots (D={D:.4f})", sorted([r1, r2])
    elif abs(D) < 1e-10:
        r = -b / (2 * a)
        return f"One repeated real root (D≈0)", [r]
    else:
        re = -b / (2 * a)
        im = np.sqrt(-D) / (2 * a)
        return f"Two complex roots: {re:.3f} ± {abs(im):.3f}i (D={D:.4f})", []


def quadratic_vertex(a: float, b: float, c: float) -> tuple[float, float]:
    """Return (x_vertex, y_vertex) of parabola."""
    if abs(a) < 1e-12:
        return (0.0, c)
    xv = -b / (2 * a)
    yv = a * xv ** 2 + b * xv + c
    return (xv, yv)