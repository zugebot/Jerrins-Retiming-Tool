# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from support import *
from timeLineEdit import TimeLineEdit
from frameTime import FrameTime


class Row:
    def __init__(self, parent, number, showIndex=True, style=1):

        # variables
        self.parent = parent
        self.settings = parent.settings
        self.number = number
        self.signType = 1
        self.showIndex = showIndex

        # easier time
        hidePaste = not self.settings.get("include-paste-buttons")
        hideSubLoad = not self.settings.get("include-sub-loads")

        # add widgets
        txt_color = self.settings.getTextQColor()
        bkg_color = makeStyle(bkg_color=self.settings.get("background-color"))
        self.buttonSignType = newButton(f"+{number + 1}", 30, self.swapSignValue,
                                        style_sheet=makeStyle(text_color=txt_color))
        self.buttonPaste1 = newButton("Paste", 45, self.pasteIntoTextBox1, hide=hidePaste)
        self.buttonPaste2 = newButton("Paste", 45, self.pasteIntoTextBox2, hide=hidePaste)
        self.textTime1 = TimeLineEdit(self, styleSheet=bkg_color, placeHolder="Start...",
                                      change_func=self.updateTotalTime)
        self.textTime2 = TimeLineEdit(self, styleSheet=bkg_color, placeHolder="End...",
                                      change_func=self.updateTotalTime)
        self.textTimeSub = TimeLineEdit(self, styleSheet=bkg_color, placeHolder="Sub...",
                                        change_func=self.updateTotalTime,
                                        maxLength=4, hide=hideSubLoad, allow_decimal=False)
        self.textFinalTime = TimeLineEdit(self, styleSheet=bkg_color, placeHolder="Total...", readOnly=True)

        self.labels = [QLabel(), QLabel(), QLabel()]
        self.widgets = [self.buttonSignType,  # 0
                        self.buttonPaste1,  # 1
                        self.textTime1,  # 2
                        self.buttonPaste2,  # 3
                        self.textTime2,  # 4
                        self.textTimeSub,  # 5
                        self.textFinalTime]  # 6


        self.layout: QWidget = QWidget()
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.container: QVBoxLayout = QVBoxLayout()
        self.layout.setLayout(self.container)
        self.container.setContentsMargins(0, 0, 0, 0)
        self.layout.setStyleSheet("background-color: rgb(40,40,40);")

        self.style = style
        if self.style == 1:
            self.setStyle1()
        elif self.style == 2:
            self.setStyle1()
            # self.setStyle2()

    def setStyle1(self):
        removeChildren(self.container)
        self.style = 1

        rowLayout: QHBoxLayout = QHBoxLayout()
        spacer1 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer2 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer3 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer4 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        rowLayout.setContentsMargins(0, 0, 0, 0)

        self.container.addSpacerItem(spacer1)
        self.container.addLayout(rowLayout)
        self.container.addSpacerItem(spacer2)


        rowLayout.addSpacerItem(spacer3)
        for widget in self.widgets:
            rowLayout.addWidget(widget)
        rowLayout.addSpacerItem(spacer4)

        self.resizeWidgets()

    def setStyle2(self):
        removeChildren(self.container)
        self.style = 2

        grid = QGridLayout()
        self.container.addLayout(grid)

        grid.addWidget(self.widgets[5], 0, 0)
        grid.addWidget(self.widgets[1], 1, 0)
        grid.addWidget(self.widgets[2], 1, 1)
        grid.addWidget(self.widgets[3], 2, 0)
        grid.addWidget(self.widgets[4], 3, 1)
        grid.addWidget(self.widgets[6], 4, 0, 2, 1)

    def resizeWidgets(self):
        widgets = [self.buttonSignType,
                   self.buttonPaste1, self.textTime1, self.buttonPaste2,
                   self.textTime2, self.textTimeSub, self.textFinalTime]

        widths = [
            [None, None, 80, None, 80, None, 80],  # pastes and subload not showing 0
            [None, 43, 80, 43, 80, None, 80],  # subload not showing 1
            [None, None, 80, None, 80, 34, 80],  # pastes not showing 2
            [None, 43, 80, 43, 80, 34, 80]  # all showing 3
        ]

        settingIndex = self.settings.get("include-paste-buttons") + 2 * self.settings.get("include-sub-loads")
        for n, widget in enumerate(widgets):
            value = widths[settingIndex][n]
            if value is None or value == -1:
                widget.setMinimumWidth(0)
            else:
                widget.setMinimumWidth(value)

    def getSignValue(self):
        return self.signType

    def setSignValue(self, sign_type: int = 1):
        self.signType = sign_type
        self.updateValueSign()

    def swapSignValue(self):
        self.signType *= -1
        self.updateValueSign()

    def updateValueSign(self):
        if self.signType == -1:
            text = "–"
            style = makeStyle(text_color=self.settings.getNegTextQColor())
            self.buttonSignType.setStyleSheet(style)
        else:
            text = "+"
            style = makeStyle(text_color=self.settings.getTextQColor())
            self.buttonSignType.setStyleSheet(style)
        if self.showIndex:
            text += str(self.number + 1)
        self.buttonSignType.setText(text)
        self.updateTotalTime()

    def updateSettings(self):
        self.resizeWidgets()
        # hints
        self.textTime1.updateHint()
        self.textTime2.updateHint()
        self.textTimeSub.updateHint()
        self.textFinalTime.updateHint()
        # subload
        if self.settings.get("include-sub-loads"):
            self.textTimeSub.show()
        else:
            self.textTimeSub.clear()
            self.textTimeSub.hide()
        # paste button
        state = self.settings.get("include-paste-buttons")
        self.buttonPaste1.setVisible(state)
        self.buttonPaste2.setVisible(state)


    def getPasteText(self):
        frameTime = FrameTime(fps=self.settings.get("fps"))
        clipboardText = QApplication.clipboard().text()

        # parses youtube debug info
        if frameTime.isYTDebug(clipboardText):
            frameTime.YTDebugInfo(clipboardText)
            clipboardText = frameTime.getTotalTime(rounded=True)

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
        self.textTimeSub.clear()
        self.textTime2.clear()
        if swapSign:
            if self.signType == -1:
                self.swapSignValue()

    def getDict(self):
        return {"sign-type": self.signType,
                "time-start": self.textTime1.text(),
                "time-sub": self.textTimeSub.text(),
                "time-end": self.textTime2.text()
                }

    def setDict(self, data: dict):
        if data.get("sign-type", 1) == -1:
            self.swapSignValue()
        self.textTime1.setText(data.get("time-start", ""))
        self.textTimeSub.setText(data.get("time-sub", ""))
        self.textTime2.setText(data.get("time-end", ""))

    def updateTotalTime(self, updateMod=True):
        fps = self.settings.get("fps")
        self.textTime1.time.updateFPS(fps)
        self.textTime2.time.updateFPS(fps)

        time1 = self.textTime1.getValue()
        time2 = self.textTime2.getValue()
        subLoad = self.textTimeSub.getValue()

        if self.textTime1.isEmpty() or self.textTime2.isEmpty():
            self.textFinalTime.clear()
            self.parent.updateModTotalTime()
            return

        value = self.signType * abs(time2 - time1) + subLoad
        totalTime = FrameTime(fps=fps)
        totalTime.setMilliseconds(value)
        totalTime = totalTime.getTotalTime()

        self.textFinalTime.setText(totalTime)
        if updateMod:
            self.parent.updateModTotalTime()
