# Jerrin Shirks
from typing import List

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QSize
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
    def __init__(self, root):
        self.root = root
        self.settings = root.settings

        self.rows: List[Row] = []

        self.saveFileName: str = self.settings.documentFolder + "save.json"
        self.template: str = None


        self.layout = newQObject(QVBoxLayout, alignment=Qt.AlignTop)


        # MAIN LAYOUT PARTS
        self.topBar = QVBoxLayout()
        self.firstBar = QHBoxLayout()
        self.secondBar = QHBoxLayout()
        self.topBar.addLayout(self.firstBar)
        self.topBar.addLayout(self.secondBar)
        self.topBar.setSizeConstraint(0)

        self.scrollArea = newQObject(QScrollArea, alignment=Qt.AlignTop)
        self.bottomBar = newQObject(QHBoxLayout, alignment=Qt.AlignTop)

        self.layout.addLayout(self.topBar)
        self.layout.addWidget(self.scrollArea)
        self.layout.addLayout(self.bottomBar)
        # 1. first and second bar stuff

        self.bAddRow = newQObject(QPushButton, text="AddRow", width=80, func=self.addRow)
        self.bDelRow = newQObject(QPushButton, text="Del Row", width=80, func=self.delRow)
        self.LabelFPS = newQObject(QLabel, text="FPS", width=20)
        self.LineEditFPS = TimeLineEdit(self, text="30", maxLength=3, allow_decimal=False, width=30,
                                        timeEdit=False, change_func=self.updateFPS)
        self.buttonCopyMod = newQObject(QPushButton, text="Copy Mod Message", func=self.copyModMessage)
        self.labelModMessage = newQObject(QLineEdit, temp="Mod Message...", readOnly=True, styleSheet="background-color: dark-grey;")
        self.rowCountLabel = QLabel(f"Rows: {len(self.rows)}")


        for widget in [self.bAddRow, self.LabelFPS, self.LineEditFPS, self.buttonCopyMod]:
            self.firstBar.addWidget(widget)

        self.secondBar.addWidget(self.bDelRow)
        self.secondBar.addWidget(self.rowCountLabel)
        self.secondBar.addWidget(self.labelModMessage)

        # 3. scroll area stuff
        self.rowForm = newQObject(QFormLayout, margins=(0, 0, 0, 0), spacing=2, alignment=Qt.AlignTop, sizeConstraint=QLayout.SetMinimumSize)



        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.rowForm)
        self.scrollArea.setWidget(self.scrollWidget)

        self.maxRowFormHeight = 295
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setMaximumHeight(self.maxRowFormHeight)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def minimum_size(self):
        # Get the minimum size required by the WindowRetimer object based on the minimum size of the Row objects
        # return self.scrollArea.minimumSize()

        # width
        width = 0
        if self.rows:
            width = 0
            count = 0
            for i in self.rows[0].widgets:
                if not i.isHidden():
                    width += i.minimumWidth()
                    count += 1
                else:
                    "do nothing"
            width += self.rows[0].container.spacing() * (count + 2)
            width += self.layout.spacing() * 4

        if self.rows:
            return QSize(width, self.scrollArea.minimumHeight())
        else:
            return self.scrollArea.minimumSize()


    def clearTitleTemplate(self):
        self.template = None
        self.root.setTitle(self.template)



    def getFPS(self):
        return self.settings.get("fps")


    def resetRows(self):
        while len(self.rows) > 1:
            self.delRow()
        self.rows[0].clear()
        self.clearTitleTemplate()


    def _resetTimes(self):
        for row in self.rows:
            row.clear(swapSign=False)


    def addRow(self):
        newRow = Row(self, len(self.rows))
        self.rows.append(newRow)
        self.rowForm.addRow(newRow.layout)
        self.updateRowCountLabel()
        self.clearTitleTemplate()

        self.root.update_minimum_size()
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
        print("updating size!")
        self.minimum_size()
        for row in self.rows:
            row.updateSettings()
        self.minimum_size()
        self.updateModTotalTime()
        self.minimum_size()



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
        newQuestionBox(self.root,
                       title="Reset Splits",
                       message="Are you sure to remove all rows and times?",
                       funcYes=self.resetRows)
        self.template = None
        self.root.setTitle()



    def resetTimes(self):
        newQuestionBox(self.root,
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
            self.root.setTitle(self.template)

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

        rows = self.root.windowRetimer.rows
        for row in rows:
            _item = item.copy()
            _item["sign-type"] = row.getSignValue()
            data["rows"].append(_item)

        write_json(data, filename)

        self.root.populateTemplates()



    def loadTemplate(self, filename):
        if not os.path.exists(filename):
            self.root.populateTemplates()
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
            status = newQuestionBox(self.root, title, message)

            if not status:
                return

        self.template = displayName
        self.root.setTitle(displayName)

        self.setRowCount(len(new_rows))
        for index, row in enumerate(self.rows):
            row.setSignValue(new_rows[index]["sign-type"])









