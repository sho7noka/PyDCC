import yurlungur as yr


class MyWindow(yr.UIWindow):
    WindowID = 'unique_window_id'
    WindowName = 'My Window'

    def __init__(self, parent=None, **kwargs):
        super(MyWindow, self).__init__(parent, **kwargs)
        # Setup window here

        container = yr.Qt.QtWidgets.QWidget()
        layout = yr.Qt.QtWidgets.QVBoxLayout()
        container.setLayout(layout)
        self.setCentralWidget(container)

        messageButton = yr.Qt.QtWidgets.QPushButton('Popup Message')
        messageButton.clicked.connect(self.message)
        layout.addWidget(messageButton)

        confirmButton = yr.Qt.QtWidgets.QPushButton('Confirmation Box')
        confirmButton.clicked.connect(self.confirm)
        layout.addWidget(confirmButton)

        paletteButton = yr.Qt.QtWidgets.QPushButton('Random Palette')
        paletteButton.clicked.connect(self.palette)
        layout.addWidget(paletteButton)
        
        # Setup callbacks, but wait until the program is ready
        self.deferred(self.newScene)

    def newScene(self, *args):
        """Example: Delete and reapply callbacks after loading a new scene."""
        self.removeCallbacks('sceneNewCallbacks')
        if self.maya:
            self.addCallbackScene('kAfterNew', self.newScene, group='sceneNewCallbacks')
        elif self.nuke:
            self.addCallbackOnCreate(self.newScene, nodeClass='Root', group='sceneNewCallbacks')

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


def main():
    MyWindow.show()


if __name__ == '__main__':
    main()
