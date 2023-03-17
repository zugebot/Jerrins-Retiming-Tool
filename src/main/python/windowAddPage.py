# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from functools import partial

# custom imports
from _support import *
from frameTime import FrameTime



class WindowAddPage(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(f"Add Page")

        # CREATES THE WINDOW
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
















