# Jerrin Shirks

from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import sys
import json
import math
import os
import subprocess
import webbrowser
import requests



class JLineEdit(QLineEdit):
    def __init__(self, row, maxLength=32, text="", readOnly=False, allowDecimalAndNegative=True, isRow=True):
        super().__init__()
        if isRow:
            self.parent = row.parent
        else:
            self.parent = row
        self.row = row
        self.isRow = isRow
        self.maxLength = maxLength
        self.pastedYoutube = False
        self.lastText = text
        self.setText(text)
        self.readOnly = readOnly
        if self.readOnly:
            self.setReadOnly(True)
        self.allowDecimalAndNegative = allowDecimalAndNegative
        self.setAlignment(Qt.AlignCenter)

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
            value = float(json.loads(self.text())['cmt'])
            value = float("%.3f" % value)
            value = math.floor(value * self.parent.fps) / self.parent.fps
            value = "%.3f" % value
            print(value)
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
            isvalid1 = all(x in "0123456789.:–-" for x in text)
        else:
            isvalid1 = all(x in "0123456789" for x in text)
        isvalid2 = text.count(".") < 2
        isvalid3 = text.count("–") + text.count("-") < 2
        # print(isvalid1, isvalid2, isvalid3)
        if not (isvalid1 and isvalid2 and isvalid3):
            return self.updateText(self.lastText, False)
        else:
            self.updateText(text[:self.maxLength])

    # parses a time signature into an integer in seconds.
    def getValue(self): # 1:32.54 -> 92.54
        # parses the negative out
        isNegative = "–" in self.text() or "-" in self.text()
        text = self.text().replace("–", "-").replace("-", "")
        # break up the text to its sub pieces
        text = text.replace(" ", ":")
        text = text.replace("d", "")
        text = text.replace("w", "")
        textValues = text.split(":")
        # converts all strings in the parsed list to float or 0
        values = [0 if i in ["", "0"] else float(i) for i in textValues]
        # Makes all numbers negative if top number is negative, makes order [seconds, minutes, hours, etc]
        values = reversed([-i if isNegative else i for i in values])
        # computes final amount by parsing the sections into amounts
        totalTime = 0
        multiples = [1, 60, 3600, 86400, 604800] # seconds in [seconds, minutes, hours, days, weeks]
        # looks over different sizes
        for n, val in enumerate(values):
            totalTime += val * multiples[n]
        # converts total time to an int if it should be one IDK lol
        if str(totalTime).endswith(".0"):
             totalTime = int(totalTime)
        # :sunglasses: we did it fam!!! :heart-emoji:
        return totalTime



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
        self.buttonPaste1.setFixedWidth(50)
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
        self.buttonPaste2.setFixedWidth(50)
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

    def pasteIntoTextBox1(self):
        text = QApplication.clipboard().text()
        self.textTime1.setText(text)

    def pasteIntoTextBox2(self):
        text = QApplication.clipboard().text()
        self.textTime2.setText(text)

    def clear(self):
        self.textTime1.setText("")
        self.textSubLoad.setText("")
        self.textTime2.setText("")
        if self.signType == -1:
            self.swapValueSign()


    def updateTotalTime(self, updateMod=True):
        time1 = self.textTime1.getValue()
        time2 = self.textTime2.getValue()
        subLoad = self.textSubLoad.getValue()
        if self.textTime1.isEmpty() or self.textTime2.isEmpty():
            self.textFinalTime.setText("")
            self.parent.updateModTotalTime()
            return
        value = self.signType * (time2 - time1) + subLoad
        totalTime = self.parent.formatToTime(value)
        self.textFinalTime.setText(totalTime)
        if updateMod:
            self.parent.updateModTotalTime()




class rowManager:
    def __init__(self, parent):
        self.parent = parent
        self.fps = 30
        self.modMessage = "Mod Note: Retimed to {}."
        self.modMessageWithSubLoad = "Mod Note: Retimed to {} ({} in subloads)."
        self.includeMilliseconds = True
        self.includeFPS = True
        self.includeSubLoads = True
        self.includePasteButtons = True
        self.rows = []

    def resetRows(self):
        while len(self.rows) > 1:
            self.delRow()
        self.rows[0].clear()

    def addRow(self):
        rowNumber = len(self.rows)
        newRow = Row(self, rowNumber)
        self.rows.append(newRow)
        self.parent.rowForm.addRow(newRow.layout)
        return newRow

    def delRow(self):
        # can only delete rows if there are 2> rows.
        if len(self.rows) <= 1:
            return
        rowIntToDelete = len(self.rows) - 1
        self.parent.rowForm.removeRow(rowIntToDelete)
        self.rows.pop()

    def formatToTime(self, value=0):
        isNegative = value < 0
        value = abs(value)
        # rounds num to the nearest frame (if useFPS is on)
        if self.includeFPS:
            value += 0.001
            value = value - (value % 1) % (1 / self.fps)
        # create all the components
        milli = int(round(value % 1, 3) * 1000)
        seconds = int(value % 60)
        minutes = int((value / 60) % 60)
        hours = int((value / 3600) % 24)
        days = int((value / 86400) % 7)
        weeks = int((value / 604800))
        # new formatting technique
        formattedTime = ""
        if weeks != 0:
            formattedTime += f"{weeks}w "
        if days != 0:
            formattedTime += f"{days}d "
        if hours != 0:
            formattedTime += str(hours) + ":"
            formattedTime += "{:0>2d}".format(minutes) + ":"
        else:
            formattedTime += str(minutes) + ":"
        # add seconds
        formattedTime += "{:0>2d}".format(seconds)
        # add milliseconds
        if self.includeMilliseconds:
            print(milli)
            formattedTime += ".{:0>3d}".format(milli)
        # re-add the "-" if the num was originally neg.
        if isNegative:
            formattedTime = "–" + formattedTime
        return formattedTime

    def updateModTotalTime(self):
        finalTime = 0
        subLoadTime = 0
        allRowsEmpty = True
        for row in self.rows:
            if not row.textFinalTime.isEmpty():
                allRowsEmpty = False
                row.updateTotalTime(updateMod=False)
                finalTime += row.textFinalTime.getValue()
                subLoadTime += row.textSubLoad.getValue()
        if allRowsEmpty or finalTime == 0:
            self.parent.labelModMessage.setText("")
        else:
            finalTime = self.formatToTime(finalTime)
            if subLoadTime == 0:
                message = self.modMessage.format(finalTime)
            else:
                subLoadTime = self.formatToTime(subLoadTime)
                message = self.modMessageWithSubLoad.format(finalTime, subLoadTime)
            self.parent.labelModMessage.setText(message)

    def toggleIncludeMilliseconds(self):
        self.includeMilliseconds = not self.includeMilliseconds
        if self.includeMilliseconds:
            pass
        else:
            pass

    def toggleIncludeFPS(self):
        self.includeFPS = not self.includeFPS
        if self.includeFPS:
            self.parent.LabelFPS.show()
            self.parent.LineEditFPS.show()
        else:
            self.parent.LabelFPS.hide()
            self.parent.LineEditFPS.hide()

    def toggleIncludeSubLoads(self):
        self.includeSubLoads = not self.includeSubLoads
        for row in self.rows:
            if self.includeSubLoads:
                row.textSubLoad.show()
            else:
                row.textSubLoad.setText("")
                row.textSubLoad.hide()

    def toggleIncludePasteButtons(self):
        self.includePasteButtons = not self.includePasteButtons
        for row in self.rows:
            if self.includePasteButtons:
                row.buttonPaste1.show()
                row.buttonPaste2.show()
            else:
                row.buttonPaste1.hide()
                row.buttonPaste2.hide()

    def updateFPS(self):
        self.parent.LineEditFPS.isValid()
        self.fps = self.parent.LineEditFPS.getValue()
        if self.fps == 0:
            self.fps = 30
        self.updateModTotalTime()




class SubWindow:

    def __init__(self, parent):
        self.parent = parent
        self.rowManager = rowManager(self)
        self.saveFileName = "save.json"
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        # MAIN LAYOUT PARTS
        self.firstBar = QHBoxLayout()
        self.secondBar = QHBoxLayout()
        self.scrollArea = QScrollArea()
        self.layout.addLayout(self.firstBar)
        self.layout.addLayout(self.secondBar)
        self.layout.addWidget(self.scrollArea)

        # 1. first and second bar stuff
        self.bAddRow = QPushButton("Add Row")
        self.bAddRow.clicked.connect(self.rowManager.addRow)
        self.bAddRow.setFixedWidth(97)

        self.bDelRow = QPushButton("Del Row")
        self.bDelRow.clicked.connect(self.rowManager.delRow)
        self.bDelRow.setFixedWidth(97)

        self.LabelFPS = QLabel("FPS")
        self.LabelFPS.setFixedWidth(20)

        self.LineEditFPS = JLineEdit(self, text="30", maxLength=3, allowDecimalAndNegative=False, isRow=False)
        self.LineEditFPS.setFixedWidth(30)
        self.LineEditFPS.textChanged[str].connect(self.rowManager.updateFPS)

        self.buttonCopyMod = QPushButton("Copy Mod Message")
        self.buttonCopyMod.clicked.connect(self.copyModMessage)


        self.buttonClearSplits = QPushButton("Clear Splits")
        self.buttonClearSplits.clicked.connect(self.resetManager)

        self.labelModMessage = QLineEdit()
        self.labelModMessage.setStyleSheet("background-color: dark-grey;")
        self.labelModMessage.setReadOnly(True)


        self.firstBar.addWidget(self.bAddRow)
        self.firstBar.addWidget(self.LabelFPS)
        self.firstBar.addWidget(self.LineEditFPS)
        self.firstBar.addWidget(self.buttonCopyMod)
        self.firstBar.addWidget(self.buttonClearSplits)


        self.secondBar.addWidget(self.bDelRow)
        self.secondBar.addWidget(self.labelModMessage)


        # 3. scroll area stuff
        self.rowForm = QFormLayout()
        self.rowForm.setAlignment(Qt.AlignTop)

        self.scrollWidget = QWidget()
        self.scrollWidget.setLayout(self.rowForm)
        self.scrollArea.setWidget(self.scrollWidget)

        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setFixedHeight(300)
        self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

    def copyModMessage(self):
        cb = QApplication.clipboard()
        cb.clear(mode=cb.Clipboard)
        cb.setText(self.labelModMessage.text(), mode=cb.Clipboard)

    def resetManager(self):
        qm = QMessageBox()
        ret = qm.question(self.parent, '', "Are you sure to reset all the values?", qm.Yes | qm.No)
        if ret == qm.Yes:
            self.rowManager.resetRows()

    def openWebsite(self):
        url = 'https://jerrin.org'
        webbrowser.open(url)

    def openModHub(self):
        url = 'https://www.speedrun.com/modhub'
        webbrowser.open(url)


    def showCredits(self):
        msg = QMessageBox(self.parent)

        msg.setWindowTitle("Credits")
        msg.setText("UI + Coding : jerrinth3glitch#6280\n"
                    "Icon Design  : Alexis.#3047")
        msg.setInformativeText(rf"<b>Version {self.parent.version}<\b>")

        msg.setDetailedText("Haha made you look")
        msg.setStandardButtons(QMessageBox.Ok)

        retval = msg.exec_()

    def viewFile(self):
        self.saveTimes()
        subprocess.Popen(r'explorer /select,"{}"'.format(self.saveFileName))

    def saveTimes(self):
        # main settings
        data = {"fps": self.rowManager.fps,
                "includeMilliseconds": self.rowManager.includeMilliseconds,
                "includeFPS": self.rowManager.includeFPS,
                "includeSubLoads": self.rowManager.includeSubLoads,
                "includePasteButtons": self.rowManager.includePasteButtons}
        # saving rows
        rowData = []
        for row in self.rowManager.rows:
            rowDict = {"signType": row.signType,
                       "text1": row.textTime1.text(),
                       "subLoad": row.textSubLoad.text(),
                       "text2": row.textTime2.text()}
            rowData.append(rowDict)
        data["rows"] = rowData
        # write data to saveFileName
        with open(self.saveFileName, "w") as file:
            file.write(json.dumps(data, indent=4))

    def loadTimes(self):
        # create the file if not already there
        if not os.path.exists(self.saveFileName):
            with open(self.saveFileName, 'w') as file:
                file.write("{}")
        # reads the data
        with open(self.saveFileName, "r") as file:
            data = json.loads(file.read())
            if data == {}:
                self.rowManager.addRow()
                return
        # populates the settings
        self.rowManager.fps = data["fps"]
        self.LineEditFPS.setText(str(self.rowManager.fps))
        if not data["includeMilliseconds"]:
            self.rowManager.toggleIncludeMilliseconds()
        if not data["includeFPS"]:
            self.rowManager.toggleIncludeFPS()
        if not data["includeSubLoads"]:
            self.rowManager.toggleIncludeSubLoads()
        if not data["includePasteButtons"]:
            self.rowManager.toggleIncludePasteButtons()
        # populate the row data
        for rowData in data["rows"]:
            row = self.rowManager.addRow()
            if rowData["signType"] == -1:
                row.swapValueSign()
            row.textTime1.setText(rowData["text1"])
            row.textSubLoad.setText(rowData["subLoad"])
            row.textTime2.setText(rowData["text2"])




class MainWindow(QMainWindow):
    def __init__(self, version="1.0.0"):
        super().__init__()
        self.version = version
        self.latestVersion = version
        self.latestUrl = ""
        self.retimerWindow = SubWindow(self)
        self.alwaysOnTop = True
        self.initUI()
        self.initMenuBar()
        self.findLatestVersion()
        self.retimerWindow.loadTimes()

    def closeEvent(self, event):
        self.retimerWindow.saveTimes()
        event.accept()

    def initUI(self):
        self.setWindowTitle("Retimer v" + self.version)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedWidth(490)
        self.setFixedHeight(395)
        widget = QWidget()
        widget.setLayout(self.retimerWindow.layout)
        self.setCentralWidget(widget)

    def initMenuBar(self):
        self.menuBar = self.menuBar()

        barFile = self.menuBar.addMenu("File")
        _viewProgress = barFile.addAction("View Save File")
        _viewProgress.triggered.connect(self.retimerWindow.viewFile)

        barSettings = self.menuBar.addMenu("Settings")

        _toggleFPS = barSettings.addAction("Include FPS")
        _toggleFPS.setCheckable(True)
        _toggleFPS.setChecked(True)
        _toggleFPS.triggered.connect(self.retimerWindow.rowManager.toggleIncludeFPS)

        _toggleSubLoads = barSettings.addAction("Include Subloads")
        _toggleSubLoads.setCheckable(True)
        _toggleSubLoads.setChecked(True)
        _toggleSubLoads.triggered.connect(self.retimerWindow.rowManager.toggleIncludeSubLoads)

        _togglePasteButtons = barSettings.addAction("Include Paste Buttons")
        _togglePasteButtons.setCheckable(True)
        _togglePasteButtons.setChecked(True)
        _togglePasteButtons.triggered.connect(self.retimerWindow.rowManager.toggleIncludePasteButtons)

        barWebsites = self.menuBar.addMenu("Websites")


        _openModHub = QAction(QIcon("1st.png"), "Moderation Hub", self)
        barWebsites.addAction(_openModHub)

        _openModHub.triggered.connect(self.retimerWindow.openModHub)

        _openWebsite = barWebsites.addAction("Open Help")
        _openWebsite.triggered.connect(self.retimerWindow.openWebsite)

        barAbout = self.menuBar.addMenu("About")

        _openCredits = barAbout.addAction("Credits")
        _openCredits.triggered.connect(self.retimerWindow.showCredits)



    def findLatestVersion(self):
        url = "https://jerrin.org/downloads/retimer/latest.json"
        latest = requests.get(url).text.split("\n")
        self.latestVersion = latest[0]
        self.latestUrl = f"https://jerrin.org/downloads/retimer/{latest[1]}".replace(" ", "%20")
        if self.version < self.latestVersion:
            updateBar = self.menuBar.addMenu("Update")
            _updateButton = updateBar.addAction(f"Download {self.latestVersion}!")
            _updateButton.triggered.connect(self.downloadUpdate)

    def downloadUpdate(self):
        webbrowser.open(self.latestUrl)



class AppContext(ApplicationContext):
    def run(self):

        if True: # color palette lol
            app = QApplication([])
            app.setStyle("Fusion")
            palette = QPalette()
            palette.setColor(QPalette.Window, QColor(53, 53, 53))
            palette.setColor(QPalette.WindowText, Qt.white)
            palette.setColor(QPalette.Base, QColor(25, 25, 25))
            palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
            palette.setColor(QPalette.ToolTipBase, Qt.black)
            palette.setColor(QPalette.ToolTipText, Qt.white)
            palette.setColor(QPalette.Text, Qt.white)
            palette.setColor(QPalette.Button, QColor(53, 53, 53))
            palette.setColor(QPalette.ButtonText, Qt.white)
            palette.setColor(QPalette.BrightText, Qt.red)
            palette.setColor(QPalette.Link, QColor(42, 130, 218))
            palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
            palette.setColor(QPalette.HighlightedText, Qt.black)
            app.setPalette(palette)

        mainwindow = MainWindow("1.03.0")
        mainwindow.show()
        return self.app.exec_()




if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
