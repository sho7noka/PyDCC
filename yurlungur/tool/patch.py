# coding: utf-8
import sys
from yurlungur.core import env as _env
from yurlungur.tool import window as _window

try:
    from yurlungur import Qt
    from vfxwindow import VFXWindow as _UIWindow

    # dispatch for Qt
    Qt.main_window = _window.main_window
    Qt.show = _window.show
    Qt.UIWindow = _UIWindow

    # dispatch app
    _UIWindow.c4d = _env.C4D()
    _UIWindow.marmoset = _env.Marmoset()
    _UIWindow.rumba = _env.Rumba()
    _UIWindow.substance_painter = _env.SPainter()
    _UIWindow.unity = _env.Unity()

except ImportError:
    _UIWindow = object

if _env.Blender() or _env.Nuke():
    sys.exit = None

# https://github.com/huntfx/vfxwindow/wiki/Quick-Start#callbacks
if _env.Max():
    _UIWindow.addCallback = None

if _env.Unity():
    _UIWindow.addCallback = None

if _env.Substance():
    import sd as __sd

    app = __sd.getContext().getSDApplication()

    _UIWindow.addCallbackBeforeFileLoaded = app.registerBeforeFileLoadedCallback
    _UIWindow.addCallbackAfterFileLoaded = app.registerAfterFileLoadedCallback
    _UIWindow.addCallbackBeforeFileSaved = app.registerBeforeFileSavedCallback
    _UIWindow.addCallbackAfterFileSaved = app.registerAfterFileSavedCallback
    _UIWindow.removeCallbacks = (app.unregisterCallback(uuid) for uuid in [])

if _env.SPainter():
    import substance_painter.event as __e

    # Subscribe to project related events.
    connections = {
        __e.ProjectOpened: _UIWindow.addCallbackProjectOpened,
        __e.ProjectCreated: _UIWindow.addCallbackProjectCreated,
        __e.ProjectAboutToClose: _UIWindow.addCallbackProjectAboutToClose,
        __e.ProjectAboutToSave: _UIWindow.addCallbackProjectAboutToSave,
        __e.ProjectSaved: _UIWindow.addCallbackProjectSaved,
        __e.ExportTexturesAboutToStart: _UIWindow.addCallbackExportTexturesAboutToStart,
        __e.ExportTexturesEnded: _UIWindow.addCallbackExportTexturesEnded,
        __e.ShelfCrawlingStarted: _UIWindow.addCallbackShelfCrawlingStarted,
        __e.ShelfCrawlingEnded: _UIWindow.addCallbackShelfCrawlingEnded,
        __e.ProjectEditionEntered: _UIWindow.addCallbackProjectEditionEntered,
        __e.ProjectEditionLeft: _UIWindow.addCallbackProjectEditionLeft,
    }
    for event, callback in connections.items():
        __e.DISPATCHER.connect(event, callback)


def remote_debug_listen(HOST='localhost', port=3000):
    """
    https://jurajtomori.wordpress.com/2018/06/13/debugging-python-in-vfx-applications/

    https://developers.maxon.net/docs/Cinema4DPythonSDK/html/manuals/introduction/python_c4dpy.html
    https://github.com/Barbarbarbarian/Blender-VScode-Debugger/blob/master/Blender_VScode_Debugger.py
    https://www.sidefx.com/ja/docs/houdini18.0/hom/hou/ShellIO
    Returns:
    """
    try:
        # https://docs.substance3d.com/sddoc/debugging-plugins-using-visual-studio-code-172825679.html
        # https://help.autodesk.com/view/MAXDEV/2021/ENU/?guid=Max_Python_API_tutorials_creating_the_dialog_html
        import ptvsd
        try:
            ptvsd.wait_for_attach()
            ptvsd.enable_attach("SFds_KjLDFJ:LK", address=(HOST, port), redirect_output=True)
            print("Not attached already, attaching...")
        except ptvsd.AttachAlreadyEnabledError:
            print("Attached already, continuing...")

    except (ImportError, ValueError):
        # https://pleiades.io/help/pycharm/remote-debugging-with-product.html
        import pydevd_pycharm as pycharm
        # pydevd.stoptrace()
        pycharm.settrace(HOST, port=port, stdoutToServer=True, stderrToServer=True)
        print("listen from pycharm server debug")


    except:
        import traceback
        traceback.print_exc()


is_code, is_evd = False, False

try:
    import pydevd_pycharm as __pycharm

    is_evd = True
except ImportError:
    try:
        import debugpy as __dpy

        is_code = True
    except ImportError:
        try:
            import ptvsd as __ptvsd

            is_code = True
        except:
            import traceback

            traceback.print_exc()

if is_code or is_evd:
    from yurlungur.tool import rpc as __rpc

    __rpc.debug_listen = remote_debug_listen

del is_code, is_evd
