# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QKeySequence
import json
import math

# custom imports
from _support import *
from frameTime import FrameTime



class TimeLineEdit(QLineEdit):
    def __init__(self,
                 row=None,
                 text: str = "",
                 maxChar: int = 32,
                 readOnly: bool = False,
                 allow_decimal: bool = True,
                 allow_negative: bool = True,
                 change_func=None,
                 timeEdit: bool = True,
                 width: int = None,
                 minWidth: int = None,
                 maxWidth: int = None,
                 centerText: bool = True,
                 styleSheet: str = None,
                 temp: str = None,
                 hide: bool = False):
        super().__init__()

        self.row = row
        self.settings = row.settings
        self.lastText: str = text
        self.setText(text)
        self.maxLength: int = maxChar
        self.allow_decimal: bool = allow_decimal
        self.allow_negative: bool = allow_negative
        self.changeFunc = change_func
        self.timeEdit = timeEdit
        self.readOnly = readOnly


        self.time = FrameTime()


        if width:
            self.setFixedWidth(width)
        if minWidth:
            self.setMinimumWidth(minWidth)
        if maxWidth:
            self.setMaximumWidth(maxWidth)
        if centerText:
            self.setAlignment(Qt.AlignCenter)
        if self.readOnly:
            self.setReadOnly(True)
        if styleSheet:
            self.setStyleSheet(styleSheet)
        self.textChanged[str].connect(self.isValid)
        self.placeHolderText = temp
        if self.settings.get("show-hints"):
            self.setPlaceholderText(self.placeHolderText)
        if hide:
            self.hide()

        self.menu = QMenu(self)
        self.initMenu()

        # animations
        self.orig_style = None
        self.color = None
        self._animation = None

    def _animate(self, value):
        r, g, b = (int(i) + (255 - int(i)) * value for i in self.color)
        self.setStyleSheet(self.orig_style + f"color: rgb({r},{g},{b})")

    def flash(self):
        if self.orig_style is None:
            self.orig_style = self.styleSheet()
            self.color = self.settings.getTextColorTuple()
        self.setStyleSheet(self.orig_style + f"color: {self.settings.getTextColorRGB()}")
        self._animation = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=1000
        )
        self._animation.start()



    def updateHint(self):
        if self.settings.get("show-hints"):
            self.setPlaceholderText(self.placeHolderText)
        else:
            self.setPlaceholderText("")


    def getFPS(self):
        return self.settings.get("fps")





    def initMenu(self):
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.showContextMenu)

        addNewAction(self.menu, "Format Time", self.handleFormatTime)
        addNewAction(self.menu, "Remove Time", self.clear)
        addNewAction(self.menu, "Copy as Mod Message", self.copyModMessage)
        # addNewAction(self.menu, "Paste Frames[WIP]", self.handlePasteFrames)


    def showContextMenu(self, point):
        style_sheet = f"""
            QMenu {{
                background-color: {self.settings.get("grey2")};
                color: white;
            }}
            QMenu::item:selected {{
                background-color: {self.settings.getHighlightRGB()};
                color: black;
            }}
        """
        self.menu.setStyleSheet(style_sheet)
        self.menu.exec_(self.mapToGlobal(point))


    def copyModMessage(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        time = FrameTime(time_str=self.text())
        message = time.createModMessage(self.settings.get("mod-message"))
        message = message.replace("\\n", "\n")
        cb.setText(message, mode=cb.Clipboard)


    def handlePasteFrames(self):
        pass


    def handleFormatTime(self):
        if self.text() != "":
            frameTime = FrameTime(self.getValue(), self.getFPS())
            self.setText(frameTime.getTotalTime())


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
        text = text.replace(" ", ":")

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
                value = frameTime.getTotalTime(rounded=True)
                return self.updateText(value)

        # if the yes
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

