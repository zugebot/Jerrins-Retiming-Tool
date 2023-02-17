# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from support import *
from jLineEdit import TimeLineEdit
from frameTime import FrameTime


class Row:
    def __init__(self, parent, number):

        # variables
        self.parent = parent
        self.settings = parent.settings
        self.number = number
        self.signType = 1
        hidePaste = not self.settings.get("include-paste-buttons")
        hideSubLoad = not self.settings.get("include-sub-loads")

        # create frame
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)

        # add widgets
        self.buttonSignType = newButton(f"+{number + 1}", 30, self.swapValueSign, style_sheet=bold_cyan)
        self.buttonPaste1 = newButton("Paste", 45, self.pasteIntoTextBox1, hide=hidePaste)
        self.textTime1 = TimeLineEdit(self, styleSheet=bkg_grey, placeHolder="Start...", change_func=self.updateTotalTime)
        self.buttonPaste2 = newButton("Paste", 45, self.pasteIntoTextBox2, hide=hidePaste)
        self.textTime2 = TimeLineEdit(self, styleSheet=bkg_grey, placeHolder="End...", change_func=self.updateTotalTime)
        self.textSubLoad = TimeLineEdit(self, maxLength=4, allow_decimal=False, styleSheet=bkg_grey,
                                        hide=hideSubLoad, change_func=self.updateTotalTime)
        self.textFinalTime = TimeLineEdit(self, readOnly=True, styleSheet=bkg_grey, placeHolder="Total...")
        self.rightSpacer = QSpacerItem(5, 5, QSizePolicy.Fixed)
        # add all these items to self.layout
        widgetList = [self.buttonSignType, self.buttonPaste1, self.textTime1, self.buttonPaste2,
                      self.textTime2, self.textSubLoad, self.textFinalTime]
        for widget in widgetList:
            self.layout.addWidget(widget)
        # self.layout.addItem(self.rightSpacer)
        self.resizeWidgets()

    def resizeWidgets(self):
        widgets = [self.buttonPaste1, self.textTime1, self.buttonPaste2,
                   self.textTime2, self.textSubLoad, self.textFinalTime]

        widths = [
            [None, 80, None,  80, None, 80],  # pastes and subload not showing 0
            [  43, 80,   43,  80, None, 80],  # subload not showing 1
            [None, 80, None,  80,   34, 80],  # pastes not showing 2
            [  43, 80,   43,  80,   34, 80]   # all showing 3
        ]

        settingIndex = self.settings.get("include-paste-buttons") + 2 * self.settings.get("include-sub-loads")
        for n, widget in enumerate(widgets):
            value = widths[settingIndex][n]
            if value is None or value == -1:
                widget.setMinimumWidth(0)
            else:
                widget.setMinimumWidth(value)

    def swapValueSign(self):
        self.signType *= -1

        if self.signType == -1:
            self.buttonSignType.setText(f"−{self.number + 1}")
            self.buttonSignType.setStyleSheet(bold_red)
        else:
            self.buttonSignType.setText(f"+{self.number + 1}")
            self.buttonSignType.setStyleSheet(bold_cyan)


        self.updateTotalTime()


    def updateHints(self):
        self.textTime1.updateHint()
        self.textTime2.updateHint()
        self.textFinalTime.updateHint()


    def getPasteText(self):
        frameTime = FrameTime(fps=self.settings.get("fps"))
        clipboardText = QApplication.clipboard().text()

        # parses youtube debug info
        if frameTime.isYTDebug(clipboardText):
            frameTime.YTDebugInfo(clipboardText)
            clipboardText = frameTime.getTotalTime(rounded=False)

        return clipboardText


    # make it so that when it pastes in, it puts the rounded value as .milli, but the actual
    # as backup
    def updateFrameTime(self):
        pass

    def pasteIntoTextBox1(self):
        clipboardText = self.getPasteText()

        if self.textTime1.text() == "":
            self.textTime1.setText(clipboardText)
            return
        newQuestionBox(self.parent.parent,
                       message=f"Are you sure you want to paste?\n"
                               f"Current     : {self.textTime1.text()}\n"
                               f"Clipboard : {clipboardText[:20]}",
                       funcYes=self.textTime1.setText,
                       argsYes=clipboardText)

    def pasteIntoTextBox2(self):
        clipboardText = self.getPasteText()

        if self.textTime2.text() == "":
            self.textTime2.setText(clipboardText)
            return
        newQuestionBox(self.parent.parent,
                       message=f"Are you sure you want to paste?\n"
                               f"Current     : {self.textTime2.text()}\n"
                               f"Clipboard : {clipboardText[:20]}",
                       funcYes=self.textTime2.setText,
                       argsYes=clipboardText)


    def clear(self, swapSign: bool = True):
        self.textTime1.clear()
        self.textSubLoad.clear()
        self.textTime2.clear()
        if swapSign:
            if self.signType == -1:
                self.swapValueSign()

    def getDict(self):
        return {"sign-type": self.signType,
                "time-start": self.textTime1.text(),
                "time-sub": self.textSubLoad.text(),
                "time-end": self.textTime2.text()
                }


    def setDict(self, data: dict):
        if data["sign-type"] == -1:
            self.swapValueSign()
        self.textTime1.setText(data["time-start"])
        self.textSubLoad.setText(data["time-sub"])
        self.textTime2.setText(data["time-end"])


    def updateTotalTime(self, updateMod=True):
        fps = self.settings.get("fps")
        self.textTime1.time.updateFPS(fps)
        self.textTime2.time.updateFPS(fps)

        time1 = self.textTime1.getValue()
        time2 = self.textTime2.getValue()
        subLoad = self.textSubLoad.getValue()

        if self.textTime1.isEmpty() or self.textTime2.isEmpty():
            self.textFinalTime.clear()
            self.parent.updateModTotalTime()
            return

        value = self.signType * abs(time2 - time1) + subLoad
        totalTime = FrameTime(value, fps).getTotalTime()

        self.textFinalTime.setText(totalTime)
        if updateMod:
            self.parent.updateModTotalTime()
