# coding: utf-8
import sys as __sys

try:
    import sd
    from sd.api.sdproperty import SDPropertyCategory

    context = sd.getContext()
    app = context.getSDApplication()
    manager = app.getPackageMgr()

    if getattr(app, "getUIMgr", False):
        graph = app.getUIMgr().getCurrentGraph()
        UndoGroup = sd.api.SDHistoryUtils.UndoGroup
        qt = app.getQtForPythonUIMgr()
    else:
        graph = manager.getUserPackages()[0].getChildrenResources(True)[0]

    __sys.modules[__name__] = __sys.modules["sd"]
except (ImportError, KeyError):
    from yurlungur.core.env import App as __App

    run, _, end, _ = __App("substance_designer")._actions

    __all__ = ["run", "end"]
