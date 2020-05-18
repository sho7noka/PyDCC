# coding: utf-8
try:
    import maya.cmds as cmds
except ImportError:
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("maya")._actions
