# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import subprocess
import webbrowser
import json
import os

# custom imports
from support import *
from row import Row
from frameTime import FrameTime
from jLineEdit import JLineEdit
from windowSettings import WindowSettings



class WindowRetimer:
    def __init__(self, parent):
        self.parent = parent
        self.settings = parent.settings
        # self.rowManager: RowManager = RowManager(self)
        self.rows: List[Row] = []

        self.saveFileName: str = self.settings.documentFolder + "save.json"
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # MAIN LAYOUT PARTS
        self.firstBar = QHBoxLayout()
        self.secondBar = QHBoxLayout()
        self.scrollArea = QScrollArea()
        self.bottomBar = QHBoxLayout()
        self.layout.addLayout(self.firstBar)
        self.layout.addLayout(self.secondBar)
        self.layout.addWidget(self.scrollArea)
        self.layout.addLayout(self.bottomBar)
        # 1. first and second bar stuff

        self.bAddRow = newButton("Add Row", 97, self.addRow)
        self.bDelRow = newButton("Del Row", 97, self.delRow)

        self.LabelFPS = QLabel("FPS")
        self.LabelFPS.setFixedWidth(20)

        self.LineEditFPS = JLineEdit(self, text="30", maxLength=3, allow_decimal=False, fixedWidth=30,
                                     timeEdit=False)
        self.LineEditFPS.textChanged[str].connect(self.updateFPS)

        self.buttonCopyMod = newButton("Copy Mod Message", None, self.copyModMessage)
        self.buttonClearSplits = newButton("Clear Splits", 85, self.resetManagerSplits)
        self.buttonClearTimes = newButton("Clear Times", 85, self.resetManagerTimes)

        self.labelModMessage = QLineEdit()
        self.labelModMessage.setStyleSheet("background-color: dark-grey;")
        self.labelModMessage.setReadOnly(True)
        self.labelModMessage.setPlaceholderText("Mod Message...")

        widgetList = [self.bAddRow, self.LabelFPS, self.LineEditFPS,
                      self.buttonCopyMod, self.buttonClearSplits, self.buttonClearTimes]
        for widget in widgetList:
            self.firstBar.addWidget(widget)

        self.secondBar.addWidget(self.bDelRow)
        self.secondBar.addWidget(self.labelModMessage)

        # 3. scroll area stuff
        self.rowForm = QFormLayout()
        self.rowForm.setAlignment(Qt.AlignTop)

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.rowForm)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(285)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # bottom part
        self.rowCountLabel = QLabel(f"Rows: {len(self.rows)}")
        self.bottomBar.addWidget(self.rowCountLabel)


    def getFPS(self):
        return self.settings.get("fps")


    def resetRows(self):
        while len(self.rows) > 1:
            self.delRow()
        self.rows[0].clear()


    def resetTimes(self):
        for row in self.rows:
            row.clear(swapSign=False)


    def addRow(self):
        newRow = Row(self, len(self.rows))
        self.rows.append(newRow)
        self.rowForm.addRow(newRow.layout)
        self.updateRowCount()
        return newRow


    def delRow(self):
        if len(self.rows) <= 1:
            return
        rowIntToDelete = len(self.rows) - 1
        self.rowForm.removeRow(rowIntToDelete)
        self.rows.pop()
        self.updateRowCount()


    def updateRowCount(self):
        self.rowCountLabel.setText(f"Rows: {len(self.rows)}")


    def updateModTotalTime(self):
        finalTime = 0
        subLoadTime = 0
        frameTime = FrameTime(fps=self.getFPS())

        allRowsEmpty = True
        for row in self.rows:
            if row.textFinalTime.isEmpty():
                continue

            allRowsEmpty = False
            row.updateTotalTime(updateMod=False)
            row.textFinalTime.time.updateFPS(self.getFPS())
            row.textTime1.time.updateFPS(self.getFPS())
            row.textTime2.time.updateFPS(self.getFPS())
            finalTime += row.textFinalTime.getValue()
            subLoadTime += row.textSubLoad.getValue()

            time1 = row.textTime1.getValue()
            if time1 < frameTime.timeStart:
                frameTime.timeStart = time1

            time2 = row.textTime2.getValue()
            if time2 > frameTime.timeEnd:
                frameTime.timeEnd = time2

        if allRowsEmpty or finalTime == 0:
            self.labelModMessage.clear()
        else:
            frameTime.setMilliseconds(finalTime)
            message = frameTime.createModMessage(self.settings.get("mod-message"))
            self.labelModMessage.setText(message)


    def updateSettings(self):
        self.toggleSubLoads()
        self.togglePasteButtons()
        self.resizeRowWidgets()
        self.updateRowHints()
        self.updateModTotalTime()


    def resizeRowWidgets(self):
        for row in self.rows:
            row.resizeWidgets()


    def updateRowHints(self):
        for row in self.rows:
            row.updateHints()


    def toggleSubLoads(self):
        for row in self.rows:
            if self.settings.get("include-sub-loads"):
                row.textSubLoad.show()
            else:
                row.textSubLoad.clear()
                row.textSubLoad.hide()

    def togglePasteButtons(self):
        for row in self.rows:
            if self.settings.get("include-paste-buttons"):
                row.buttonPaste1.show()
                row.buttonPaste2.show()
            else:
                row.buttonPaste1.hide()
                row.buttonPaste2.hide()


    def updateFPS(self):
        self.LineEditFPS.isValid()
        self.settings.set("fps", self.LineEditFPS.getValue())
        if self.getFPS() == 0:
            self.settings.set("fps", 30)
        for row in self.rows:
            row.updateTotalTime()
        self.updateModTotalTime()
        print(f"updated FPS to {self.settings.get('fps')}")



    def copyModMessage(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.labelModMessage.text(), mode=cb.Clipboard)



    def resetManagerSplits(self):
        newQuestionBox(self.parent,
                       title="Reset Splits",
                       message="Are you sure to remove all rows and times?",
                       funcYes=self.resetRows)



    def resetManagerTimes(self):
        newQuestionBox(self.parent,
                       title="Reset Times",
                       message="Are you sure to remove all the times?",
                       funcYes=self.resetTimes)


    def saveTimes(self):
        rowData = [row.getDict() for row in self.rows]
        write_json({"rows": rowData}, self.saveFileName)


    def viewFile(self):
        self.saveTimes()
        self.settings.openFileDialog(self.saveFileName)


    def loadTimes(self):
        data = read_json(self.saveFileName)
        if not data:
            return self.addRow()

        # populates the settings
        self.LineEditFPS.setText(self.getFPS())

        self.toggleSubLoads()
        self.togglePasteButtons()

        # populate the row data
        for row_dict in data["rows"]:
            row = self.addRow()
            row.setDict(row_dict)

