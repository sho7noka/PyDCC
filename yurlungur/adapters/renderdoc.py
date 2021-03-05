# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["renderdoc"]

except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("renderdoc")._actions

    __all__ = ["run", "shell", "end", "connect"]
