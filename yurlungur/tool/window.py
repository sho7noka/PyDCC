# coding: utf-8
u"""
Qt 管理Windowモジュール
"""
import sys
import os
import inspect
import traceback

import yurlungur
from yurlungur.core import env


def main_window():
    """
    >>> import yurlungur
    >>> ptr = yurlungur.Qt.main_window()
    >>> view = yurlungur.Qt.QMainWindow(ptr)
    >>> yurlungur.Qt.show(view)

    :return:
    """
    import yurlungur.core.app

    app_name = yurlungur.core.application.__name__

    if app_name == "maya.cmds":
        from yurlungur.Qt import QtCompat
        from maya import OpenMayaUI

        ptr = long(OpenMayaUI.MQtUtil.mainWindow())
        return QtCompat.wrapInstance(ptr, QWidget)

    if app_name == "sd.api":
        from yurlungur.adapters import substance_designer
        return substance_designer.qt.getMainWindow()

    if app_name == "hou":
        import hou
        return hou.qt.mainWindow()

    if app_name == "nuke":
        return QApplication.activeWindow()

    if app_name == "fusion":
        try:
            import fusionscript
        except ImportError:
            import PeyeonScript as fusionscript

        fusion = fusionscript.scriptapp('Fusion')
        return fusion.GetMainWindow()

    if app_name == "pymxs":
        try:
            import qtmax
            return qtmax.GetQMaxMainWindow()
        except ImportError:
            import MaxPlus
            return MaxPlus.QtHelpers_GetQmaxMainWindow()

    if app_name == "substance_painter":
        import substance_painter
        return substance_painter.ui.get_main_window()

    if app_name == "rumba":
        import rumbapy
        return rumbapy.widget("MainWindow")

    if app_name == "renderdoc":
        import qrenderdoc
        return qrenderdoc.MainWindow

    return None


def show(view):
    """
    >>> view = yurlungur.Qt.QWidget()
    >>> yurlungur.Qt.show(view)

    :param view:
    :return:
    """
    try:
        view.deleteLater()
    except:
        yurlungur.logger.pprint(view)

    try:
        __dark_view(view)

        if env.Max():
            __protect_show(view)

        elif env.Unreal():
            import unreal
            unreal.parent_external_window_to_slate(view.winId())

        else:
            view.show()

    except:
        view.deleteLater()
        yurlungur.logger.warn(traceback.print_exc())

    if not QApplication.instance():
        app = QApplication(sys.argv)
        __dark_view(view)

        if env.Max():
            __protect_show(view)
        else:
            view.show()

        sys.exit(app.exec_())


class __GCProtector(object):
    widgets = []


def __protect_show(w):
    w.setWindowFlags(Qt.WindowStaysOnTopHint)
    w.show()
    __GCProtector.widgets.append(w)


def __dark_view(view):
    local = os.path.dirname(os.path.dirname(inspect.currentframe().f_code.co_filename))
    with open(local + "/user/dark.css") as f:
        view.setStyleSheet("".join(f.readlines()))
