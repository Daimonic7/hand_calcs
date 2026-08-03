"""Wire significant figures + kip-inch units into handcalcs.

This is the single import for a calc notebook:

    from helpers.formatting import *
    setup_formatting(3)

Importing it also registers the handcalcs `%%render` / `%%tex` cell magics and
re-exports the unit names, math helpers, `sig`, and `export_notebook`, so the
notebook preamble needs nothing else.
"""
import handcalcs
import handcalcs.handcalcs as _hc

from .sigfigs import to_sigfig, sig            # noqa: F401 (sig re-exported)
from .units import customary
from .units import *                            # unit names + math helpers, re-exported
from . import units as _units
from .exporter import export_notebook           # noqa: F401 (re-exported)

# Register %%render / %%tex on import. Safe (no-op) when imported outside a kernel.
try:
    import handcalcs.render  # noqa: F401
except Exception:
    pass

_orig_latex_repr = _hc.latex_repr
_CURRENT_SIG_FIGS = 3


def _latex_repr(item, use_scientific_notation, precision, preferred_formatter):
    n = precision if precision else _CURRENT_SIG_FIGS
    # forallpeople Physical -> kip-inch magnitude at n sig figs
    if hasattr(item, "dimensions") and hasattr(item, "value"):
        conv = customary(item)
        if conv is not None:
            num = to_sigfig(conv[0], n, latex=True)
            if num is not None:
                return (num + r"\ " + conv[1]) if conv[1] else num
    # plain int / float -> n sig figs
    try:
        out = to_sigfig(item, n, latex=True)
        if out is not None:
            return out
    except Exception:
        pass
    return _orig_latex_repr(item, use_scientific_notation, precision, preferred_formatter)


def setup_formatting(sig_figs=3):
    """Install the sig-fig + kip-inch renderer and set handcalcs options."""
    global _CURRENT_SIG_FIGS
    _CURRENT_SIG_FIGS = sig_figs
    _hc.latex_repr = _latex_repr
    handcalcs.set_option("display_precision", sig_figs)
    handcalcs.set_option("param_columns", 2)


__all__ = list(_units.__all__) + [
    "setup_formatting", "sig", "export_notebook", "to_sigfig", "customary",
]
