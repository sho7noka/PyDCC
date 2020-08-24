# coding: utf-8
import sys

try:
    sys.modules[__name__] = sys.modules["mset"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, connect = __App("marmoset")._actions
