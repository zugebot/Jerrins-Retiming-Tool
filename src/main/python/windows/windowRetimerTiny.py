# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

# custom imports
from src.main.python.support import *
from src.main.python.row import Row



class WindowRetimerTiny(QWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.settings = root.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(" ")
        self.setMaximumSize(150, 80)

        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        shortcut.activated.connect(self.close)


        self.layout = QVBoxLayout()
        self.layout.setSpacing(2)
        # self.layout.setContentsMargins(0,0,0,0)

        grey2 = self.settings.getColorRGB("grey2")

        # CREATES THE WINDOW
        self.widget = newQObject(QWidget, maxWidth=150)
        self.widget.setLayout(self.layout)
        # self.widget.setStyleSheet(f"background-color: {grey3};")

        self.setStyleSheet(f"background-color: {grey2};")

        # make items
        self.copyButton = newQObject(QPushButton, text="Copy Mod Message", func=None, maxWidth=150)
        self.row = Row(root, 0, style=1)

        # add items
        self.layout.addWidget(self.row.layout)
        self.layout.addWidget(self.copyButton)

        # set layout

        self.setLayout(self.layout)




    def closeEvent(self, event):
        self.root.show()
        self.close()
