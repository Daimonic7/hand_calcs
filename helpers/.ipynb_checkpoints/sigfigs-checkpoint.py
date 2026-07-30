import math
import handcalcs
import handcalcs.handcalcs as _hc

# --- Significant Figures Configuration ---
_orig_latex_repr = _hc.latex_repr
_CURRENT_SIG_FIGS = 3

def _to_sigfig(x, sig, latex=True):
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

def _sigfig_latex_repr(item, use_scientific_notation, precision, preferred_formatter):
    try:
        out = _to_sigfig(item, precision if precision else _CURRENT_SIG_FIGS, latex=True)
        if out is not None:
            return out
    except Exception:
        pass
    return _orig_latex_repr(item, use_scientific_notation, precision, preferred_formatter)

def setup_formatting(sig_figs=3):
    """Patches handcalcs to use sig figs and sets default options."""
    global _CURRENT_SIG_FIGS
    _CURRENT_SIG_FIGS = sig_figs
    _hc.latex_repr = _sigfig_latex_repr
    handcalcs.set_option("display_precision", sig_figs)
    handcalcs.set_option("param_columns", 2)

def sig(x, n=3):
    """Significant-figure string for plain-text (non-handcalcs) output."""
    return _to_sigfig(float(x), n, latex=False)