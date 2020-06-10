# coding: utf-8
import sys

try:
    import rumbapy

    sys.modules[__name__] = sys.modules["rumba"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("rumba")._actions


class Layer(object):
    def __init__(self, layer):
        self.layer = layer

    def add(self):
        rumbapy.add_animation_layer()

    def delete(self):
        rumbapy.remove_layer()

    @property
    def keyframes(self):
        return Keyframe(self.layer)


class Keyframe(object):
    def __init__(self, layer):
        from yurlungur.tool.meta import meta
        self.layer = layer
        self.meta = meta

    def add(self):
        self.meta.key_layer(self.layer, self.meta.current_frame())

    def delete(self):
        self.meta.remove_keys(self.layer)

    def transform(self):
        self.meta.transform_keys

    def time_warp(self):
        self.meta.time_warp_keys
