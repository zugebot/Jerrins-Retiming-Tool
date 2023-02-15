# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from jLineEdit import JLineEdit
from support import *


class Row:
    def __init__(self, parent, number):
        self.number = number
        self.parent = parent
        # VARIABLES
        self.signType = 1  # -1=negative, 1=positive
        # CREATE FRAME
        self.layout = QHBoxLayout()
        self.layout.setContentsMargins(0, 0, 0, 0)
        # SUB ITEMS
        # 1. buttonSignType
        self.buttonSignType = QPushButton("+" + str(number))
        self.buttonSignType.setFixedWidth(30)
        self.buttonSignType.clicked.connect(self.swapValueSign)
        self.buttonSignType.setStyleSheet("font: bold; color: green;")
        # 2. buttonPaste1
        self.buttonPaste1 = QPushButton("Paste")
        self.buttonPaste1.setFixedWidth(45)
        self.buttonPaste1.clicked.connect(self.pasteIntoTextBox1)
        if not self.parent.includePasteButtons:
            self.buttonPaste1.hide()
        # 3.
        self.textTime1 = JLineEdit(self)
        self.textTime1.textChanged[str].connect(self.textTime1.isValid)
        self.textTime1.setFixedWidth(80)
        self.textTime1.setStyleSheet("background-color: dark-grey;")
        # 4.
        self.buttonPaste2 = QPushButton("Paste")
        self.buttonPaste2.setFixedWidth(45)
        self.buttonPaste2.clicked.connect(self.pasteIntoTextBox2)
        if not self.parent.includePasteButtons:
            self.buttonPaste2.hide()
        # 5.
        self.textTime2 = JLineEdit(self)
        self.textTime2.textChanged[str].connect(self.textTime2.isValid)
        self.textTime2.setFixedWidth(80)
        self.textTime2.setStyleSheet("background-color: dark-grey;")
        # 6.
        self.textSubLoad = JLineEdit(self, maxLength=4, allowDecimalAndNegative=False)
        self.textSubLoad.textChanged[str].connect(self.textSubLoad.isValid)
        self.textSubLoad.setFixedWidth(34)
        self.textSubLoad.setStyleSheet("background-color: dark-grey;")
        if not self.parent.includeSubLoads:
            self.textSubLoad.hide()
        # 7.
        self.textFinalTime = JLineEdit(self, readOnly=True)
        # add all these items to self.layout
        self.layout.addWidget(self.buttonSignType)
        self.layout.addWidget(self.buttonPaste1)
        self.layout.addWidget(self.textTime1)
        self.layout.addWidget(self.buttonPaste2)
        self.layout.addWidget(self.textTime2)
        self.layout.addWidget(self.textSubLoad)
        self.layout.addWidget(self.textFinalTime)


    def swapValueSign(self):
        self.signType += self.signType * -2

        if self.signType == -1:
            self.buttonSignType.setText("−" + str(self.number))
            self.buttonSignType.setStyleSheet("font: bold; color: red;")
        else:
            self.buttonSignType.setText("+" + str(self.number))
            self.buttonSignType.setStyleSheet("font: bold; color: green;")

        self.updateTotalTime()


    def ensureMessageBox(self, message):
        qm = QMessageBox()
        ret = qm.question(self.parent.parent.parent, '', message, qm.Yes | qm.No)
        return ret == qm.Yes

    def pasteIntoTextBox1(self):
        status = True
        clipboardText = QApplication.clipboard().text()
        clipboardText, state = formatYoutubeDebugInfo(clipboardText, self.parent.fps)
        if state:
            clipboardText = formatToTime(clipboardText, self.parent.fps)

        if self.textTime1.text() != "":
            status = self.ensureMessageBox(f"Are you sure you want to paste?\n"
                                           f"Current     : {self.textTime1.text()}\n"
                                           f"Clipboard : {clipboardText[:20]}")
        if status:
            self.textTime1.setText(clipboardText)


    def pasteIntoTextBox2(self):
        status = True
        clipboardText = QApplication.clipboard().text()
        clipboardText, state = formatYoutubeDebugInfo(clipboardText, self.parent.fps)
        if state:
            clipboardText = formatToTime(clipboardText, self.parent.fps)

        if self.textTime2.text() != "":
            status = self.ensureMessageBox(f"Are you sure you want to paste?\n"
                                           f"Current     : {self.textTime2.text()}\n"
                                           f"Clipboard : {clipboardText[:20]}")
        if status:
            self.textTime2.setText(clipboardText)


    def clear(self):
        self.textTime1.clear()
        self.textSubLoad.clear()
        self.textTime2.clear()
        if self.signType == -1:
            self.swapValueSign()


    def updateTotalTime(self, updateMod=True):
        time1 = self.textTime1.getValue()
        time2 = self.textTime2.getValue()
        subLoad = self.textSubLoad.getValue()
        if self.textTime1.isEmpty() or self.textTime2.isEmpty():
            self.textFinalTime.clear()
            self.parent.updateModTotalTime()
            return
        value = self.signType * (time2 - time1) + subLoad
        totalTime = self.parent.formatToTime(value)
        self.textFinalTime.setText(totalTime)
        if updateMod:
            self.parent.updateModTotalTime()
