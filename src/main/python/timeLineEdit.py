# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QKeySequence
import json
import math

# custom imports
from support import *
from settings import Settings
from frameTime import FrameTime




class TimeLineEdit(QLineEdit):
    def __init__(self,
                 parent=None,
                 text: str = "",
                 maxLength: int = 32,
                 readOnly: bool = False,
                 allow_decimal: bool = True,
                 allow_negative: bool = True,
                 change_func=None,
                 timeEdit: bool = True,
                 fixedWidth: int = None,
                 centerText: bool = True,
                 styleSheet: str = None,
                 placeHolder: str = None,
                 hide: bool = False):
        super().__init__()


        self.settings: Settings = parent.settings
        self.lastText: str = text
        self.setText(text)
        self.maxLength: int = maxLength
        self.allow_decimal: bool = allow_decimal
        self.allow_negative: bool = allow_negative
        self.changeFunc = change_func
        self.timeEdit = timeEdit
        self.readOnly = readOnly


        self.time = FrameTime()


        if fixedWidth:
            self.setFixedWidth(fixedWidth)
        if centerText:
            self.setAlignment(Qt.AlignCenter)
        if self.readOnly:
            self.setReadOnly(True)
        if styleSheet:
            self.setStyleSheet(styleSheet)
        self.textChanged[str].connect(self.isValid)
        self.placeHolderText = placeHolder
        if self.settings.get("show-hints"):
            self.setPlaceholderText(self.placeHolderText)
        if hide:
            self.hide()

        self.menu = QMenu(self)
        self.initMenu()


    def updateHint(self):
        if self.settings.get("show-hints"):
            self.setPlaceholderText(self.placeHolderText)
        else:
            self.setPlaceholderText("")


    def getFPS(self):
        return self.settings.get("fps")


    def initMenu(self):
        palette = QPalette()
        palette.setColor(QPalette.HighlightedText, text_cyan)
        self.menu.setPalette(palette)
        addNewAction(self.menu, "Format Time", self.handleFormatTime)
        addNewAction(self.menu, "Remove Time", self.clear)
        addNewAction(self.menu, "Paste Frames[WIP]", self.handlePasteFrames)


    def handlePasteFrames(self):
        pass


    def handleFormatTime(self):
        if self.text() != "":
            value = formatToTime(self.getValue(), self.getFPS())
            self.setText(value)


    def setText(self, p_str):
        if not isinstance(p_str, str):
            p_str = str(p_str)
        super().setText(p_str)


    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())


    def clear(self) -> None:
        self.setText("")


    def updateText(self, text, successful=True):
        if successful:
            temp = self.cursorPosition()
        else:
            lengthAdded = len(self.text()) - len(self.lastText)
            temp = self.cursorPosition() - lengthAdded

        text = text.replace("-", "–")

        self.setText(text[0:self.maxLength])
        self.setCursorPosition(temp)
        self.lastText = text

        if callable(self.changeFunc):
            self.changeFunc()



    def isEmpty(self) -> bool:
        return self.text() == ""


    def isValid(self) -> bool:
        text = self.text()
        # prevents recursion
        if self.readOnly or text == self.lastText:
            return

        # parses youtube debug info
        if self.timeEdit:
            frameTime = FrameTime(fps=self.getFPS())
            if frameTime.isYTDebug(text):
                frameTime.YTDebugInfo(text)
                value = frameTime.getTotalTime()
                return self.updateText(value)


        # if the
        if self.time.isValidTime(text, self.allow_decimal, self.allow_negative):
            self.updateText(text[:self.maxLength])
        else:
            self.updateText(self.lastText[:self.maxLength], False)


    # parses a time signature into an integer in seconds.
    def getValue(self):  # 1:32.54 -> 92.54

        if self.timeEdit:
            time = FrameTime.convertToSeconds(self.text())
        else:
            if self.text() == "":
                time = 30
            else:
                time = int(self.text())


        return time

