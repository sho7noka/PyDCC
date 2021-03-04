# -*- coding: utf-8 -*-
import yurlungur
from yurlungur.Qt import UIWindow
from PySide2 import QtGui, QtWidgets, QtCore


class Window(UIWindow):
    WindowID = 'unique_window_id'
    WindowName = 'My Window'
    WindowDockable = True

    def __init__(self, parent=None, **kwargs):
        super(Window, self).__init__(parent, **kwargs)
        self.setup()

    def setup(self):
        list = QtWidgets.QListWidget()
        layout = QtWidgets.QHBoxLayout()

    @QtCore.SLOT
    def run(self, app):
        getattr(yurlungur, app).run()

if __name__ == '__main__':
    Window.show()
