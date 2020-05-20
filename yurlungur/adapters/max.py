# coding: utf-8
import sys

try:
    sys.modules[__name__] = sys.modules["pymxs"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("3dsmax")._actions
