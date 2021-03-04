import yurlungur

import sys
import os
from yurlungur.Qt import QtWidgets, UIWindow
sys.path.append(os.path.abspath(__file__).rsplit(os.path.sep, 2)[0])


class Window1(UIWindow):
    def __init__(self, *args, **kwargs):
        super(Window1, self).__init__(*args, **kwargs)
        self.setCentralWidget(QtWidgets.QPushButton('Open Window'))
        self.centralWidget().clicked.connect(Window2.show)


class Window2(UIWindow):
    def __init__(self, *args, **kwargs):
        super(Window2, self).__init__(*args, **kwargs)
        self.setCentralWidget(QtWidgets.QPushButton('Close'))
        self.centralWidget().clicked.connect(self.close)

def main():
    Window1.show()

if __name__ == '__main__':
    main()
