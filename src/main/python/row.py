# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from src.main.python.support import *
from src.main.python.timeLineEdit import TimeLineEdit
from src.main.python.frameTime import FrameTime


class Row:
    def __init__(self, root, number, showIndex=True, style=1):

        # variables
        self.style = None
        self.root = root
        self.settings = root.settings
        self.number = number
        self.signType = 1
        self.showIndex = showIndex

        self.layout: QWidget = QWidget()
        # self.layout.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.container: QVBoxLayout = QVBoxLayout()
        self.container.setSizeConstraint(QLayout.SetMinimumSize)

        self.layout.setLayout(self.container)
        self.container.setContentsMargins(0, 0, 0, 0)
        self.layout.setStyleSheet("background-color: rgb(40,40,40);")

        # easier time
        hideSubLoad = not self.settings.get("show-sub-loads")

        # widget presets
        # txt_color = self.settings.getTextQColor()
        grey1 = self.settings.getColorRGB("grey1")
        grey2 = self.settings.getColorRGB("grey2")
        grey3 = self.settings.getColorRGB("grey3")
        black = self.settings.getColorRGB("black")
        text = self.settings.getTextColorRGB()

        k_style_sign = {"styleSheet": makeStyle(text) + "; padding: 0px;"}
        k_style_button = {"minHeight": 22}

        k_paste = {
            "text": "Paste",
            "width": 45,
            "hidden": not self.settings.get("show-paste-buttons")
        }
        k_style_text1 = {"styleSheet": f"background-color: {black};"}
        k_style_text2 = {"styleSheet": f"background-color: {grey3};"}
        k_time = {"minWidth": 60, "maxWidth": 120}
        k_final = {"minWidth": 60, "maxWidth": 150}
        k_update = {"change_func": self.updateTotalTime}
        # add widgets
        # self.textRowTitle = TimeLineEdit(self, temp="text...", width=80, hide=hideText, **k_style_text1)
        self.buttonSignType = newQObject(QPushButton, text=f"+{number + 1}", width=30, func=self.swapSignValue,
                                         **k_style_button, **k_style_sign)
        self.buttonPasteStart = newQObject(QPushButton, func=self.pasteIntoTextBox1, **k_paste, **k_style_button)
        self.buttonPasteEnd = newQObject(QPushButton, func=self.pasteIntoTextBox2, **k_paste, **k_style_button)
        self.textTimeSub = TimeLineEdit(self, temp="Sub...", width=40, maxChar=4, hide=hideSubLoad,
                                        allow_decimal=False, **k_style_text1, **k_update)
        self.textTimeStart = TimeLineEdit(self, temp="Start...", **k_time, **k_update, **k_style_text1)
        self.textTimeEnd = TimeLineEdit(self, temp="End...", **k_time, **k_update, **k_style_text1)
        self.textTimeFinal = TimeLineEdit(self, temp="Total...", readOnly=True, **k_final, **k_style_text2)
        self.widgets = [self.buttonSignType, self.buttonPasteStart, self.textTimeStart, self.buttonPasteEnd,
                        self.textTimeEnd, self.textTimeSub, self.textTimeFinal]

        self.setStyle1()


    def setStyle1(self):
        removeChildren(self.container)
        self.style = 1

        # spacers
        rowLayout: QHBoxLayout = QHBoxLayout()
        spacer1 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer2 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer3 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        spacer4 = QSpacerItem(5, 5, QSizePolicy.Minimum, QSizePolicy.Fixed)
        rowLayout.setContentsMargins(0, 0, 0, 0)
        self.container.addSpacerItem(spacer1)
        self.container.addLayout(rowLayout)
        self.container.addSpacerItem(spacer2)

        # widgets to row
        rowLayout.addSpacerItem(spacer3)
        for widget in self.widgets:
            rowLayout.addWidget(widget)
        rowLayout.addSpacerItem(spacer4)

        # stretch factors
        rowLayout.setStretchFactor(self.textTimeStart, 4)
        rowLayout.setStretchFactor(self.textTimeEnd, 4)
        rowLayout.setStretchFactor(self.textTimeFinal, 6)


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
        self.layout.setMinimumSize(self.container.minimumSize())


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
            style = makeStyle(self.settings.getAntiTextColorRGB())
            self.buttonSignType.setStyleSheet(style)
        else:
            text = "+"
            style = makeStyle(self.settings.getTextColorRGB())
            self.buttonSignType.setStyleSheet(style)
        if self.showIndex:
            text += str(self.number + 1)
        self.buttonSignType.setText(text)
        self.updateTotalTime()


    def getValueSignAsText(self):
        if self.signType == 1:
            return f"+{self.number + 1}"
        else:
            return f"–{self.number + 1}"


    def updateSettings(self):
        self.resizeWidgets()
        # hints
        self.textTimeStart.updateHint()
        self.textTimeEnd.updateHint()
        self.textTimeSub.updateHint()
        self.textTimeFinal.updateHint()
        # subload
        if self.settings.get("show-sub-loads"):
            self.textTimeSub.show()
        else:
            self.textTimeSub.clear()
            self.textTimeSub.hide()
        # paste button
        state = self.settings.get("show-paste-buttons")
        self.buttonPasteStart.setVisible(state)
        self.buttonPasteEnd.setVisible(state)


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
        if self.textTimeStart.text() == "":
            self.textTimeStart.setText(clipboardText)
            return
        text = "Are you sure you want to paste?\nCurrent     : {}\nClipboard : {}"
        newQuestionBox(self.root.root,
                       message=text.format(self.textTimeStart.text(), clipboardText[:20]),
                       funcYes=self.textTimeStart.setText,
                       argsYes=clipboardText)


    def pasteIntoTextBox2(self):
        clipboardText = self.getPasteText()
        if self.textTimeEnd.text() == "":
            self.textTimeEnd.setText(clipboardText)
            return
        text = "Are you sure you want to paste?\nCurrent     : {}\nClipboard : {}"
        newQuestionBox(self.root.root,
                       message=text.format(self.textTimeEnd.text(), clipboardText[:20]),
                       funcYes=self.textTimeEnd.setText,
                       argsYes=clipboardText)


    def clear(self, swapSign: bool = True):
        self.textTimeStart.clear()
        self.textTimeSub.clear()
        self.textTimeEnd.clear()
        if swapSign:
            if self.signType == -1:
                self.swapSignValue()


    def getDict(self, defaults=False):
        """
        return {"sign-type": self.signType,
                "time-start": self.textTime1.text(),
                "time-sub": self.textTimeSub.text(),
                "time-end": self.textTime2.text()
                }
        """
        data: dict = {"sign-type": self.signType}

        if self.textTimeStart.text() != "":
            data["time-start"] = self.textTimeStart.text()
        elif defaults:
            data.setdefault("time-start", "0")

        if self.textTimeSub.text() != "":
            data["time-sub"] = self.textTimeSub.text()
        elif defaults:
            data.setdefault("time-sub", "0")

        if self.textTimeEnd.text() != "":
            data["time-end"] = self.textTimeEnd.text()
        elif defaults:
            data.setdefault("time-end", "0")
        return data


    def getList(self, includeSub=True):
        data = [
            self.getValueSignAsText(),
            self.textTimeStart.text(),
            self.textTimeEnd.text(),
        ]
        if includeSub:
            data.append(self.textTimeSub.text())
        data.append(self.textTimeFinal.text())

        # make sure only 0's
        for index, item in enumerate(data):
            if item == "":
                data[index] = "0"
        return data



    def setDict(self, data: dict):
        if data.get("sign-type", 1) == -1:
            self.swapSignValue()
        self.textTimeStart.setText(data.get("time-start", ""))
        self.textTimeSub.setText(data.get("time-sub", ""))
        self.textTimeEnd.setText(data.get("time-end", ""))


    def updateTotalTime(self, updateMod=True):
        fps = self.settings.get("fps")
        self.textTimeStart.time.updateFPS(fps)
        self.textTimeEnd.time.updateFPS(fps)

        time1 = self.textTimeStart.getValue()
        time2 = self.textTimeEnd.getValue()
        subLoad = self.textTimeSub.getValue()

        if self.textTimeStart.isEmpty() or self.textTimeEnd.isEmpty():
            self.textTimeFinal.clear()
            self.root.updateModTotalTime()
            return

        value = self.signType * (time2 - time1) + subLoad
        totalTime = FrameTime(fps=fps)
        totalTime.setMilliseconds(value)
        time_str = totalTime.getTotalTime()
        totalTime = time_str

        self.textTimeFinal.setText(totalTime)
        if updateMod:
            self.root.updateModTotalTime()
