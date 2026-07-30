"""Significant-figure formatting — pure numeric helpers.

No dependency on handcalcs or forallpeople. This module answers one question:
"given a number and a target number of significant figures, what string do I
show?" Unit handling lives in units.py; the handcalcs wiring lives in
formatting.py.
"""
import math


def to_sigfig(x, sig=3, latex=True):
    """Return `x` rounded to `sig` significant figures as a string.

    Returns None if `x` is not a real number (so callers can fall through).
    """
    if isinstance(x, bool) or not isinstance(x, (int, float)):
        return None
    if x != x or x in (float("inf"), float("-inf")):
        return None
    if x == 0:
        return "0"

    mag = math.floor(math.log10(abs(x)))
    if mag < -4 or mag >= 7:  # scientific if extreme
        m = round(x / 10.0**mag, sig - 1)
        if abs(m) >= 10:
            m /= 10.0
            mag += 1
        ms = f"{m:.{max(sig - 1, 0)}f}".rstrip("0").rstrip(".")
        return f"{ms} \\times 10^{{{mag}}}" if latex else f"{ms}e{mag}"

    dp = sig - 1 - mag
    r = round(x * 10.0**dp) / 10.0**dp
    if r != 0:  # rounding may carry (9.99 -> 10.0)
        mag = math.floor(math.log10(abs(r)) + 1e-9)
        dp = sig - 1 - mag

    s = f"{r:.{max(dp, 0)}f}"
    return s.rstrip("0").rstrip(".") if "." in s else s


def sig(x, n=3):
    """Significant-figure string for plain-text output (e.g. summary tables).

    Accepts a plain number or anything float()-able. For a forallpeople
    Physical this yields the magnitude in its *current display unit*; to get a
    kip-inch magnitude in text, use `units.mag(x)`.
    """
    try:
        return to_sigfig(float(x), n, latex=False)
    except Exception:
        return str(x)
