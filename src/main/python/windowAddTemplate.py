# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from functools import partial

# custom imports
from _support import *
from frameTime import FrameTime



class WindowAddTemplate(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(f"Add Template")

        self.setMinimumWidth(300)


        # CREATES THE WINDOW
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        grid = QGridLayout()
        self.layout.addLayout(grid)

        labelName = QLabel("Template Name:")
        self.lineName = QLineEdit()
        self.lineName.setMinimumWidth(190)
        self.lineName.setMaxLength(31)
        cancelButton = newButton("Cancel", None, func=self.close)
        confirmButton = newButton("Confirm", None, func=self.confirmTemplate)

        grid.addWidget(labelName, 0, 0)
        grid.addWidget(self.lineName, 0, 1)
        grid.addWidget(cancelButton, 1, 0)
        grid.addWidget(confirmButton, 1, 1)


    def confirmTemplate(self):
        text = self.lineName.text()
        if text == "":
            self.lineName.setFocus()
            return

        for letter in "#|\\<>*?\":":
            if letter in text:
                self.lineName.setFocus()
                return

        displayName = text.strip()
        file = text.lower().replace(" ", "_") + ".rt"
        fileName = self.settings.dirJoiner(self.settings.templateFolder, file)

        self.parent.windowRetimer.createTemplate(displayName, fileName)
        self.close()
