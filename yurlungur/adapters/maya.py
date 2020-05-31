# coding: utf-8
import sys

try:
    sys.modules[__name__] = sys.modules["maya"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("maya")._actions


class Layer(object):
    def __init__(self, layer):
        self.layer = layer

    @property
    def keyframes(self):
        return Keyframe(self.layer)


class Keyframe(object):
    def __init__(self, layer):
        self.layer = layer
