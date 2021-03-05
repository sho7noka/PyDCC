# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["c4d"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("c4d")._actions

    __all__ = ["run", "shell", "end", "connect"]
    """
    https://www.cineversity.com/wiki/Python:_Finding_Plugin_IDs/
    >>> for p in c4d.plugins.FilterPluginList(c4d.PLUGINTYPE_SCENELOADER,True):
    >>>    print(p.GetID(), " = ", p.GetName())
    # 1055179  =  USD (*.usda/*.usdc)
    """
