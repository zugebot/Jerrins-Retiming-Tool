# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QKeySequence

# custom imports
from _support import *
from row import Row



class WindowRetimerTiny(QWidget):
    def __init__(self, root, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.root = root
        self.settings = root.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowCloseButtonHint)
        self.setWindowTitle(" ")
        self.setMaximumSize(150, 80)

        shortcut1 = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        shortcut1.activated.connect(self.close)
        shortcut2 = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_F), self)
        shortcut2.activated.connect(self.close)

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
        self.copyButton = newQObject(QPushButton, text="Copy Mod Message", func=self.copyModMessage, maxWidth=150)
        self.row = Row(root, 0, style=1)

        # add items
        self.layout.addWidget(self.row.layout)
        self.layout.addWidget(self.copyButton)

        # set layout

        self.setLayout(self.layout)



    def copyModMessage(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        message = self.row.textTimeFinal.time.createModMessage(self.settings.get("mod-message"))
        message = message.replace("\\n", "\n")
        cb.setText(message, mode=cb.Clipboard)


    def closeEvent(self, event):
        self.root.show()
        self.close()
