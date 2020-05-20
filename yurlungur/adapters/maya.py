# coding: utf-8
import sys

try:
    sys.modules[__name__] = sys.modules["maya"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("maya")._actions
