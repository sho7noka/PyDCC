import random
import sys
sys.path.append("/Users/shosumioka/Yurlungur")

import yurlungur
from yurlungur.Qt import QtWidgets, UIWindow
from vfxwindow.utils.palette import getPaletteList


class YWindow(UIWindow):
    WindowID = 'unique_window_id'
    WindowName = 'My Window'
    WindowDockable = True

    def __init__(self, parent=None, **kwargs):
        super(YWindow, self).__init__(parent, **kwargs)

        # Setup window here
        container = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        messageButton = QtWidgets.QPushButton('Popup Message')
        messageButton.clicked.connect(self.message)
        layout.addWidget(messageButton)

        confirmButton = QtWidgets.QPushButton('Confirmation Box')
        confirmButton.clicked.connect(self.confirm)
        layout.addWidget(confirmButton)

        paletteButton = QtWidgets.QPushButton('Random Palette')
        paletteButton.clicked.connect(self.palette)
        layout.addWidget(paletteButton)

    def message(self):
        """Test message box."""
        value = self.displayMessage(
            title='Test',
            message='This is a test.'
        )
        print('Chosen value: {}'.format(value))
        return value

    def confirm(self):
        """Test confirmation box."""
        value = self.displayMessage(
            title='Test',
            message='This is a test.',
            buttons=('Yes', 'No'),
            defaultButton='Yes',
            cancelButton='No',
        )
        print('Chosen value: {}'.format(value))
        return value

    def palette(self):
        newPalette = random.choice(getPaletteList())
        self.setWindowPalette(*newPalette.split('.', 1))
        # Setup callbacks, but wait until the program is ready
        self.deferred(self.newScene)

    def newScene(self, *args):
        """Example: Delete and reapply callbacks after loading a new scene."""
        self.removeCallbacks('sceneNewCallbacks')
        if self.maya:
            self.addCallbackScene('kAfterNew', self.newScene, group='sceneNewCallbacks')
        elif self.nuke:
            self.addCallbackOnCreate(self.newScene, nodeClass='Root', group='sceneNewCallbacks')
        elif self.unity:
            print(1)

if __name__ == '__main__':
    YWindow.show()
