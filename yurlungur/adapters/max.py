# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["pymxs"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("3dsmax")._actions

    __all__ = ["run", "shell", "end", "connect"]


class Layer(object):
    def __init__(self, layer):
        self.layer = layer

    @property
    def keyframes(self):
        return Keyframe(self.layer)


class Keyframe(object):
    def __init__(self, layer):
        self.layer = layer
