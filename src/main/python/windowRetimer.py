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
from _support import *
from row import Row
from frameTime import FrameTime
from timeLineEdit import TimeLineEdit
from customTextEdit import CustomTextEdit



class WindowRetimer:
    def __init__(self, root):
        self.root = root
        self.settings = root.settings

        self.rows: List[Row] = []



        self.saveFileName: str = self.settings.documentFolder + "save.json"
        self.template: str = None
        self.totalTime: FrameTime = FrameTime()

        self.widget: QWidget = QWidget()

        self.layout = newQObject(QVBoxLayout, alignment=Qt.AlignTop)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.setSizeConstraint(QLayout.SetMaximumSize)
        self.widget.setLayout(self.layout)

        self.widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Maximum)
        self.widget.setMaximumHeight(self.layout.sizeHint().height())


        # MAIN LAYOUT PARTS
        self.topGrid = newQObject(QGridLayout, alignment=Qt.AlignHCenter)
        self.topGridWidget = newQObject(QWidget, styleSheet=f"background-color: {self.settings.getColorRGB('grey2')};")
        self.topGridWidget.setFixedHeight(65)

        self.topGridWidget.setLayout(self.topGrid)

        self.layout.addWidget(self.topGridWidget)


        # 1. first and second bar stuff

        background = f"background-color: {self.settings.getColorRGB('grey3')}; border-radius: 2px;"

        self.bAddRow = newQObject(QPushButton, text="Add Row", width=80, func=self.addRow)
        self.bDelRow = newQObject(QPushButton, text="Del Row", width=80, func=self.delRow)

        self.LabelFPS: QLabel = newQObject(QLabel, text="FPS", width=35, height=19, styleSheet=background, margins=(0, 0, 0, 0))
        self.LabelFPS.setAlignment(Qt.AlignCenter)
        self.LineEditFPS = TimeLineEdit(self, text="30", width=35, maxChar=3, allow_decimal=False,
                                        timeEdit=False, change_func=self.updateFPS, styleSheet=f"background-color: {self.settings.getColorRGB('black')}; border-radius: 2px;")
        self.LineEditFPS.setContentsMargins(0, 0, 0, 0)
        self.LineEditFPS.setFixedHeight(21)
        fpsWidget: QWidget = newQObject(QWidget, margins=(0, 0, 0, 0))
        fpsWidget.setStyleSheet(background)
        fpsWidget.setFixedHeight(21)
        self.layoutFPS: QHBoxLayout = newQObject(QHBoxLayout)
        self.layoutFPS.setSpacing(0)
        self.layoutFPS.setContentsMargins(0, 0, 0, 0)

        self.layoutFPS.addSpacerItem(QSpacerItem(3, 3, QSizePolicy.Fixed, QSizePolicy.Expanding))
        self.layoutFPS.addWidget(self.LabelFPS)
        self.layoutFPS.addWidget(self.LineEditFPS)
        fpsWidget.setLayout(self.layoutFPS)

        self.buttonCopyMod = newQObject(QPushButton, text="Copy Mod Message", func=self.copyModMessage)

        _ = CustomTextEdit(self.settings)
        self.labelModMessage: CustomTextEdit = editQObject(_, height=48, temp="Mod Message...",
                                          readOnly=True, styleSheet=background)
        # self.labelModMessage = newQObject(QTextEdit, height=48, temp="Mod Message...", readOnly=True,
        #                                   styleSheet=background)
        self.labelModMessage.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        self.rowCountLabel = newQObject(QLabel, width=60, height=21, text=f"Rows: {len(self.rows)}", styleSheet=background)
        self.rowCountLabel.setAlignment(Qt.AlignCenter)


        # placing top grid objects
        self.topGrid.addWidget(self.bAddRow, 0, 0)
        self.topGrid.addWidget(self.bDelRow, 1, 0)

        self.topGrid.addWidget(self.labelModMessage, 0, 1, 2, 2)

        self.topGrid.addWidget(fpsWidget, 1, 3, 1, 2)
        self.topGrid.addWidget(self.rowCountLabel, 1, 5)
        self.topGrid.addWidget(self.buttonCopyMod, 0, 3, 1, 3)

        self.topGrid.setRowStretch(0, 0)
        self.topGrid.setRowStretch(1, 0)

        # 3. scroll area stuff
        # self.rowForm = newQObject(QFormLayout, margins=(0, 0, 0, 0), spacing=2, alignment=Qt.AlignTop,
        #                           )# sizeConstraint=QLayout.SetMinimumSize)

        self.rowBar: QVBoxLayout = newQObject(QVBoxLayout, margins=(0, 0, 0, 0), alignment=Qt.AlignTop)
        self.rowBar.setSpacing(0)
        self.rowBar.setSizeConstraint(QLayout.SetMaximumSize)

        self.scrollArea: QScrollArea = newQObject(QScrollArea)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(QWidget())

        self.scrollArea.setFixedHeight(260)
        self.scrollArea.widget().setLayout(self.rowBar)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.layout.addWidget(self.scrollArea)

        self.updateSettings()
        self.updateMinimumWidth()


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
        newRow = Row(self, len(self.rows), updateFunc=self.updateModTotalTime)
        self.rows.append(newRow)

        self.rowBar.addWidget(newRow.layout)

        self.updateRowCountLabel()
        self.clearTitleTemplate()

        self.update_rowbar_height()
        return newRow


    def delRow(self):
        if len(self.rows) <= 1:
            return

        removeLastChild(self.rowBar)
        self.rows.pop()

        self.clearTitleTemplate()
        self.updateRowCountLabel()

        self.update_rowbar_height()



    def flashRows(self):
        for row in self.rows:
            row.flash()


    def update_rowbar_height(self):
        self.root.setMaximumHeight(self.widget.maximumHeight())

        self.widget.setMaximumHeight(self.layout.sizeHint().height())

        pass
        # set the maximum height of the layout to the height required by its contents


        # size_hint = self.rowBar.sizeHint()

        # set the maximum height of the widget to the height required by the layout
        # self.scrollArea.setMaximumHeight(size_hint.height())
        # self.widget.setMaximumHeight(size_hint.height())

        # fix main window
        # size_hint = self.widget.sizeHint()
        # self.widget.setMaximumHeight(size_hint.height())

        # if self.rowBar.count() >= 9:
        #     self.rowBar.setSizeConstraint(QVBoxLayout.SetMinimumSize)
        # elif self.rowBar.count() <= 8:
        #    self.rowBar.setSizeConstraint(QVBoxLayout.SetMinimumSize)



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
        self.totalTime = FrameTime(fps=self.getFPS())

        allRowsEmpty = True
        for row in self.rows:
            if row.textTimeFinal.isEmpty():
                continue

            allRowsEmpty = False
            row.updateTotalTime(updateMod=False)
            row.textTimeFinal.time.updateFPS(self.getFPS())
            row.textTimeStart.time.updateFPS(self.getFPS())
            row.textTimeEnd.time.updateFPS(self.getFPS())

            finalTime += row.textTimeFinal.getValue()
            subLoadTime += row.textTimeSub.getValue()

            time1 = row.textTimeStart.getValue()
            if self.totalTime.timeStart is None:
                self.totalTime.timeStart = time1
            elif time1 < self.totalTime.timeStart:
                self.totalTime.timeStart = time1

            time2 = row.textTimeEnd.getValue()
            if self.totalTime.timeEnd is None:
                self.totalTime.timeEnd = time2
            elif time2 > self.totalTime.timeEnd:
                self.totalTime.timeEnd = time2

        if allRowsEmpty or finalTime == 0:
            self.labelModMessage.clear()
        else:
            self.totalTime.setMilliseconds(finalTime)
            message = self.totalTime.createModMessage(self.settings.get("mod-message"))
            self.labelModMessage.setText(message)


    def updateMinimumWidth(self):
        if not self.rows:
            return
        width = self.rows[0].getMinimumWidth()
        if len(self.rows) > 8:
            width += 10
        self.widget.setMinimumWidth(width)
        # print(width)


    def updateSettings(self):
        for row in self.rows:
            row.updateSettings()

        self.updateMinimumWidth()
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
        message = self.labelModMessage.toPlainText()
        message = message.replace("\\n", "\n")
        cb.setText(message, mode=cb.Clipboard)
        self.labelModMessage.flash()


    def resetSplits(self):
        newQuestionBox(self.root,
                       title="Reset Rows",
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


    def copyRowsAsText(self):
        self.flashRows()
        clipboard = QApplication.clipboard()

        rows_used = 0
        all_rows_data: list = []
        useSubLoads = self.settings.get("include-sub-loads")

        if useSubLoads:
            all_rows_data.append(["Row", "Start", "Sub", "End", "Final"])
            all_rows_data.append(["–", "–", "–", "–", "–"])
            sep_dict = {0: " | ", 1: "  ", 2: "  ", 3: " | "}

        else:
            all_rows_data.append(["Row", "Start", "End", "Final"])
            all_rows_data.append(["–", "–", "–", "–"])
            sep_dict = {0: " | ", 1: "  ", 2: " | "}

        for row in self.rows:
            row_data = row.getList(includeSub=useSubLoads)
            if row_data[-3:] != ["0", "0", "0"]:
                all_rows_data.append(row_data)
                rows_used += 1


        section1 = makeTable(all_rows_data, separation=2,
                             vert_line=[1],
                             sep=sep_dict)

        section2 = f"Final Time: {self.totalTime.getTotalTime()}\n" \
                   f"Row Count : {rows_used}\n" \
                   f"FPS       : {self.getFPS()}\n"

        string = f"```{section1}\n\n{section2}```"

        clipboard.setText(string)


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

        self.root.openRowTemplateAction.setVisible(True)
        self.root.populateTemplates()


    def loadTemplate(self, filename):
        if not os.path.exists(filename):
            self.root.populateTemplates()
            return

        data = read_json(filename)

        displayName = data.get("display-name", "None")
        new_rows = data.get("rows", [])

        # checks user agrees
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
