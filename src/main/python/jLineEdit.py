# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QKeySequence
import json
import math

# custom imports
from support import *




class JLineEdit(QLineEdit):
    def __init__(self,
                 row,
                 maxLength: int = 32,
                 text: str = "",
                 readOnly: bool = False,
                 allowDecimalAndNegative: bool = True,
                 isRow: bool = True):
        super().__init__()

        if isRow:
            self.parent = row.parent
        else:
            self.parent = row
        self.row = row
        self.isRow: bool = isRow
        self.maxLength: int = maxLength
        self.pastedYoutube: bool = False
        self.lastText: str = text
        self.setText(text)
        self.readOnly = readOnly
        if self.readOnly:
            self.setReadOnly(True)
        self.allowDecimalAndNegative: bool = allowDecimalAndNegative
        self.setAlignment(Qt.AlignCenter)

        self.menu = QMenu(self)
        palette = QPalette()
        palette.setColor(QPalette.HighlightedText, QColor(42, 130, 218))
        self.menu.setPalette(palette)
        self.menu.addAction(QAction("Format Time", self, triggered=self.handleFormatTime))
        self.menu.addAction(QAction("Remove Time", self, triggered=self.clear))
        self.menu.addAction(QAction("Paste Frames[WIP]", self, triggered=self.handlePasteFrames))


    def handlePasteFrames(self):
        pass


    def handleFormatTime(self):
        print("handle format Time")
        if self.text() != "":
            value = self.getValue()
            value = formatToTime(value, self.parent.fps)
            self.setText(str(value))


    def contextMenuEvent(self, event):
        self.menu.exec_(event.globalPos())


    def clear(self):
        self.setText("")


    def updateText(self, text, successful=True):
        # do this if it is debug info
        if self.pastedYoutube:
            self.pastedYoutube = False
        # fix the cursor position, hold it
        if successful:
            temp = self.cursorPosition()
        else:
            lengthAdded = len(self.text()) - len(self.lastText)
            temp = self.cursorPosition() - lengthAdded
        # replace the minus sign for making it look nicer
        # text = text.replace("–", "-")
        # ensure the string is smaller than max length
        self.setText(text[0:self.maxLength])
        # fix the cursor location
        self.setCursorPosition(temp)
        # update last text
        self.lastText = text
        if self.isRow:
            # update that columns total time
            self.row.updateTotalTime()


    def isEmpty(self):
        return self.text() == ""


    def isValid(self):
        # prevents recursion
        if self.text() == self.lastText:
            return
        # prevents "fixing" non-writable text boxes
        if self.readOnly:
            return

        # parses youtube debug info
        try:
            self.pastedYoutube = True
            value, state = formatYoutubeDebugInfo(self.text(), self.parent.fps)
            if state:
                value = self.parent.formatToTime(float(value))
                return self.updateText(value)
        except:
            self.pastedYoutube = False

        text = self.text()
        if ("–" in text) or ("-" in text):
            # print("has", text)
            text = "–" + text.replace("–", "").replace("-", "")
        # tests validity of entered text
        if self.allowDecimalAndNegative:
            isvalid1 = all(x in " dw0123456789.:–-" for x in text)
        else:
            isvalid1 = all(x in " dw0123456789" for x in text)
        isvalid2 = text.count(".") < 2
        isvalid3 = text.count("–") + text.count("-") < 2
        # print(isvalid1, isvalid2, isvalid3)
        if not (isvalid1 and isvalid2 and isvalid3):
            return self.updateText(self.lastText, False)
        else:
            self.updateText(text[:self.maxLength])


    # parses a time signature into an integer in seconds.
    def getValue(self):  # 1:32.54 -> 92.54
        # parses the negative out
        isNegative = "–" in self.text() or "-" in self.text()
        text = self.text().replace("–", "-").replace("-", "")
        # break up the text to its sub pieces
        text = text.replace("d :", "d:")
        text = text.replace("d", "")
        text = text.replace("w", "")
        text = text.replace(" ", ":")
        textValues = text.split(":")
        # converts all strings in the parsed list to float or 0
        values = [0 if i in ["", "0"] else float(i) for i in textValues]
        # Makes all numbers negative if top number is negative, makes order [seconds, minutes, hours, etc]
        values = reversed([-i if isNegative else i for i in values])
        # computes final amount by parsing the sections into amounts
        totalTime = 0
        multiples = [1, 60, 3600, 86400, 604800]  # seconds in [seconds, minutes, hours, days, weeks]
        # looks over different sizes
        for n, val in enumerate(values):
            totalTime += val * multiples[n]
        # converts total time to an int if it should be one IDK lol
        if str(totalTime).endswith(".0"):
            totalTime = int(totalTime)
        # :sunglasses: we did it fam!!! :heart-emoji:
        return totalTime
