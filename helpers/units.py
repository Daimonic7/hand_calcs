"""US customary (kip-inch) units for structural hand calcs.

Loads the forallpeople 'structural' environment once, exposes the unit names
and a few math helpers for `import *`, and reconstructs any
`force^a * length^b` quantity in a fixed kip-inch system. That reconstruction
is what fixes forallpeople's SI fallback: dimensions with no named kip-inch
unit (force/length, or a force that lost its 'kip' tag through a **0.5 chain)
otherwise render as kN, kN/m, MN/m.

Pure with respect to handcalcs — the handcalcs hook lives in formatting.py.
"""
import forallpeople as _si
from math import sin, cos, tan, atan, asin, acos, sqrt, pi  # noqa: F401 (re-exported)

_si.environment("structural")

# unit objects
kip = _si.kip
lb = _si.lb
inch = _si.inch
ft = _si.ft
ksi = _si.ksi
psi = _si.psi
ksf = _si.ksf
psf = _si.psf

# SI magnitude of 1 kip and 1 inch (exact, taken from forallpeople itself)
_KIP_N = float((1 * kip).value)
_IN_M = float((1 * inch).value)


def _fmt_exp(e):
    er = round(e)
    if abs(e - er) < 1e-9:
        e = er
    return f"{e:g}"


def _unit_latex(a, b):
    """LaTeX for force^a * length^b in kip-inch, matching the \\mathrm{} style
    forallpeople uses for the units it already knows."""
    if abs(a - 1) < 1e-9 and abs(b + 2) < 1e-9:  # stress -> ksi (ksi-scale calcs)
        return r"\mathrm{ksi}"
    length_sym = "inch" if abs(a) < 1e-9 else "in"  # forallpeople: 'inch' pure, 'in' composite
    num, den = [], []

    def put(sym, e):
        er = round(e)
        if abs(e - er) < 1e-9:
            e = er
        if e == 0:
            return
        tok = r"\mathrm{%s}" % sym
        if abs(abs(e) - 1) > 1e-9:
            tok += "^{%s}" % _fmt_exp(abs(e))
        (num if e > 0 else den).append(tok)

    put("kip", a)
    put(length_sym, b)
    if not num and not den:
        return ""
    num_s = r" \cdot ".join(num) if num else "1"
    if den:
        den_s = r" \cdot ".join(den)
        if len(den) > 1:
            den_s = "(" + den_s + ")"
        return num_s + " / " + den_s
    return num_s


def customary(physical):
    """(magnitude_in_kip_inch, unit_latex) for a `force^a * length^b` Physical,
    or None if it isn't a pure force/length combination (caller then falls
    back to forallpeople's own repr)."""
    try:
        dims = tuple(physical.dimensions)  # (kg, m, s, A, cd, K, mol)
    except Exception:
        return None
    if len(dims) < 3:
        return None
    kg, m, s = dims[0], dims[1], dims[2]
    if any(abs(d) > 1e-9 for d in dims[3:]):  # electrical/thermal/etc. -> leave alone
        return None
    a = kg                       # force exponent
    if abs(s - (-2.0 * a)) > 1e-9:  # not a pure force/length combination
        return None
    b = m - a                    # length exponent
    try:
        magnitude = float(physical.value) / ((_KIP_N ** a) * (_IN_M ** b))
    except Exception:
        return None
    return magnitude, _unit_latex(a, b)


def mag(physical):
    """kip-inch magnitude of a Physical as a float, for text/tables."""
    c = customary(physical)
    return c[0] if c is not None else float(physical)


__all__ = [
    "kip", "lb", "inch", "ft", "ksi", "psi", "ksf", "psf",
    "sin", "cos", "tan", "atan", "asin", "acos", "sqrt", "pi",
    "customary", "mag",
]
