# coding: utf-8
import sys as __sys

try:
    __sys.modules[__name__] = __sys.modules["c4d"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, shell, end, connect = __App("c4d")._actions

    __all__ = ["run", "shell", "end", "connect"]


class Project(object):
    def __init__(self, project):
        self.project = project

    def __repr__(self):
        return self.project.name()

    @property
    def sequences(self):
        return Timeline(self.project)


class Timeline(object):
    def __init__(self, timeline):
        self.timeline = timeline

    @property
    def tracks(self):
        return Track(self.timeline)


class Track(object):
    def __init__(self, track):
        self.track = track

    @property
    def clips(self):
        return Item(self.track)


class Item(object):
    pass
