# coding: utf-8
try:
    import substance_painter as sp
except ImportError:
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("substance_painter")._actions
