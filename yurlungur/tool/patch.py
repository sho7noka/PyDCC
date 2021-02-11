# coding: utf-8
import sys
from yurlungur.core import env
from yurlungur import Qt
from yurlungur.tool import window as _window

try:
    from vfxwindow import VFXWindow as _UIWindow
except ImportError:
    UIWindow = object

# https://github.com/Peter92/vfxwindow/wiki/Quick-Start
_UIWindow.c4d = env.C4D()
_UIWindow.marmoset = env.Marmoset()
_UIWindow.rumba = env.Rumba()
_UIWindow.substance_painter = env.SPainter()
_UIWindow.unity = env.Unity()

if env.SPainter():
    import substance_painter.event as e

    _UIWindow.addCallbackProjectOpened
    _UIWindow.addCallbackProjectCreated
    _UIWindow.addCallbackProjectAboutToClose
    _UIWindow.addCallbackProjectAboutToSave
    _UIWindow.addCallbackProjectSaved
    _UIWindow.addCallbackExportTexturesAboutToStart
    _UIWindow.addCallbackExportTexturesEnded
    _UIWindow.addCallbackShelfCrawlingStarted
    _UIWindow.addCallbackShelfCrawlingEnded
    _UIWindow.addCallbackProjectEditionEntered
    _UIWindow.addCallbackProjectEditionLeft = _UIWindow._addApplicationHandler('frame_change_post', func,
                                                                               persistent=persistent, group=group)


    def addCallbackFrameChangeAfter(self, func, persistent=True, group=None):
        """After frame change for playback and rendering."""
        self._addApplicationHandler('frame_change_post', func, persistent=persistent, group=group)

# dispatch for Qt
Qt.main_window = _window.main_window
Qt.show = _window.show
Qt.UIWindow = _UIWindow

# dispatch app exit
if env.Blender() or env.Nuke():
    sys.exit = None

del sys, env
