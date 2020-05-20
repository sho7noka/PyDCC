# coding: utf-8
import sys

try:
    sys.modules[__name__] = sys.modules["substance_painter"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("substance_painter")._actions
