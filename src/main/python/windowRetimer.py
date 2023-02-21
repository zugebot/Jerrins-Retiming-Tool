# Jerrin Shirks
from typing import List

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
from timeLineEdit import TimeLineEdit
from windowSettings import WindowSettings



class WindowRetimer:
    def __init__(self, parent):
        self.parent = parent
        self.settings = parent.settings
        # self.rowManager: RowManager = RowManager(self)
        self.rows: List[Row] = []

        self.saveFileName: str = self.settings.documentFolder + "save.json"
        self.template: str = None

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)



        # MAIN LAYOUT PARTS
        self.topBar = QVBoxLayout()
        self.firstBar = QHBoxLayout()
        self.secondBar = QHBoxLayout()
        self.topBar.addLayout(self.firstBar)
        self.topBar.addLayout(self.secondBar)
        self.topBar.setSizeConstraint(0)

        self.scrollArea = QScrollArea()
        self.bottomBar = QHBoxLayout()
        self.bottomBar.setAlignment(Qt.AlignTop)

        self.layout.addLayout(self.topBar)
        self.layout.addWidget(self.scrollArea)
        self.layout.addLayout(self.bottomBar)
        # 1. first and second bar stuff

        self.bAddRow = newButton("Add Row", 80, self.addRow)
        self.bDelRow = newButton("Del Row", 80, self.delRow)

        self.LabelFPS = QLabel("FPS")
        self.LabelFPS.setFixedWidth(20)

        self.LineEditFPS = TimeLineEdit(self, text="30", maxLength=3, allow_decimal=False, fixedWidth=30,
                                        timeEdit=False, change_func=self.updateFPS)

        self.buttonCopyMod = newButton("Copy Mod Message", None, self.copyModMessage)

        self.labelModMessage = QLineEdit()
        self.labelModMessage.setStyleSheet("background-color: dark-grey;")
        self.labelModMessage.setReadOnly(True)
        self.labelModMessage.setPlaceholderText("Mod Message...")

        self.rowCountLabel = QLabel(f"Rows: {len(self.rows)}")


        widgetList = [self.bAddRow, self.LabelFPS, self.LineEditFPS, self.buttonCopyMod]
        for widget in widgetList:
            self.firstBar.addWidget(widget)

        self.secondBar.addWidget(self.bDelRow)
        self.secondBar.addWidget(self.rowCountLabel)
        self.secondBar.addWidget(self.labelModMessage)

        # 3. scroll area stuff
        self.rowForm = QFormLayout()
        self.rowForm.setContentsMargins(0, 0, 0, 0)
        self.rowForm.setSpacing(2)
        self.rowForm.setAlignment(Qt.AlignTop)

        # self.layout.setMinimumWidth(self.rowForm.minimumSizeHint().width())
        # self.layout.setSizeConstraint(self.rowForm.sizeHint().width())

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.rowForm)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumHeight(295)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)



    def clearTitleTemplate(self):
        self.template = None
        self.parent.setTitle(self.template)



    def getFPS(self):
        return self.settings.get("fps")


    def resetRows(self):
        while len(self.rows) > 1:
            self.delRow()
        self.rows[0].clear()
        # self.rows[0].setStyle2()
        self.clearTitleTemplate()


    def _resetTimes(self):
        for row in self.rows:
            row.clear(swapSign=False)


    def addRow(self):
        if len(self.rows) == 0:
            newRow = Row(self, len(self.rows), style=2)


        else:
            newRow = Row(self, len(self.rows), style=1)
            # self.scrollArea.setFixedHeight(295)
        self.rows.append(newRow)
        self.rowForm.addRow(newRow.layout)
        self.updateRowCountLabel()
        self.clearTitleTemplate()

        if len(self.rows) == 1:
            self.rows[0].setStyle2()
        else:
            self.rows[0].setStyle1()

        self.scrollArea.verticalScrollBar().setValue(self.scrollArea.verticalScrollBar().maximum())

        return newRow


    def delRow(self):
        if len(self.rows) <= 1:
            return
        rowIntToDelete = len(self.rows) - 1
        self.rowForm.removeRow(rowIntToDelete)
        self.rows.pop()
        self.clearTitleTemplate()
        self.updateRowCountLabel()

        if len(self.rows) == 1:
            self.rows[0].setStyle2()

    def setRowCount(self, count: int = 1):
        while len(self.rows) < count:
            self.addRow()
        while len(self.rows) > count:
            self.delRow()


    def updateRowCountLabel(self):
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
            subLoadTime += row.textTimeSub.getValue()

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
            message = message.replace("\n", "\\n")
            self.labelModMessage.setText(message)



    def updateSettings(self):
        for row in self.rows:
            row.updateSettings()
        self.updateModTotalTime()



    def updateFPS(self):
        self.LineEditFPS.isValid()
        self.settings.set("fps", self.LineEditFPS.getValue())
        if self.getFPS() == 0:
            self.settings.set("fps", 30)
        for row in self.rows:
            row.updateTotalTime()
        self.updateModTotalTime()



    def copyModMessage(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        message = self.labelModMessage.text()
        message = message.replace("\\n", "\n")
        cb.setText(message, mode=cb.Clipboard)



    def resetSplits(self):
        newQuestionBox(self.parent,
                       title="Reset Splits",
                       message="Are you sure to remove all rows and times?",
                       funcYes=self.resetRows)
        self.template = None
        self.parent.setTitle()



    def resetTimes(self):
        newQuestionBox(self.parent,
                       title="Reset Times",
                       message="Are you sure to remove all the times?",
                       funcYes=self._resetTimes)


    def saveFile(self):
        rowData = [row.getDict() for row in self.rows]
        data: dict = {
            "notes"
            "template": self.template,
            "rows": rowData
        }
        write_json(data, self.saveFileName)


    def viewDocumentFolder(self):
        self.saveFile()
        self.settings.openFileDialog(self.saveFileName)


    def loadSaveFile(self):
        data = read_json(self.saveFileName)
        if not data:
            return self.addRow()

        # populates the settings
        self.LineEditFPS.setText(self.getFPS())
        self.updateSettings()

        # update Title if using a template
        self.template = data.get("display-name", None)
        if self.template is not None:
            self.parent.setTitle(self.template)

        # populate the row data
        for row_dict in data["rows"]:
            row = self.addRow()
            row.setDict(row_dict)


    def createTemplate(self, name, filename):
        data: dict = {
            "display-name": name,
            "notes": "",
            "rows": []
        }
        item: dict = {
            "sign-type": None
        }

        rows = self.parent.windowRetimer.rows
        for row in rows:
            _item = item.copy()
            _item["sign-type"] = row.getSignValue()
            data["rows"].append(_item)

        write_json(data, filename)

        self.parent.populateTemplates()



    def loadTemplate(self, filename):
        if not os.path.exists(filename):
            self.parent.populateTemplates()
            return

        data = read_json(filename)

        displayName = data.get("display-name", "None")
        new_rows = data.get("rows", [])

        # deletes rows
        if len(self.rows) != len(new_rows):
            title = "Confirm Load Template"
            message = f"Loading \"{displayName}\"" \
                      f"\nRow Count: {len(self.rows)} -> {len(new_rows)}" \
                      f"\nConfirm by pressing yes."
            status = newQuestionBox(self.parent, title, message)

            if not status:
                return

        self.template = displayName
        self.parent.setTitle(displayName)

        self.setRowCount(len(new_rows))
        for index, row in enumerate(self.rows):
            row.setSignValue(new_rows[index]["sign-type"])









