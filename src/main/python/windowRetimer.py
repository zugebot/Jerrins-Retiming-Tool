# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import webbrowser
import json
import os

# custom imports
from rowManager import RowManager
from jLineEdit import JLineEdit
from windowEditModMessage import WindowEditModMessage



class RetimerWindow:
    def __init__(self, parent):
        self.parent = parent
        self.rowManager: RowManager = RowManager(self)
        self.saveFileName: str = "save.json"
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)

        self.links = {
            "website": 'https://jerrin.org',
            "modhub": 'https://www.speedrun.com/modhub',
            "retimer": 'https://github.com/zugebot/Speedrun-Retimer'
        }

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
        self.buttonClearSplits.setFixedWidth(85)

        self.buttonClearTimes = QPushButton("Clear Times")
        self.buttonClearTimes.clicked.connect(self.resetManagerTimes)
        self.buttonClearTimes.setFixedWidth(85)

        self.labelModMessage = QLineEdit()
        self.labelModMessage.setStyleSheet("background-color: dark-grey;")
        self.labelModMessage.setReadOnly(True)

        self.firstBar.addWidget(self.bAddRow)
        self.firstBar.addWidget(self.LabelFPS)
        self.firstBar.addWidget(self.LineEditFPS)
        self.firstBar.addWidget(self.buttonCopyMod)
        self.firstBar.addWidget(self.buttonClearSplits)
        self.firstBar.addWidget(self.buttonClearTimes)

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
        ret = qm.question(self.parent, '', "Are you sure to remove all rows and times?", qm.Yes | qm.No)
        if ret == qm.Yes:
            self.rowManager.resetRows()


    def resetManagerTimes(self):
        qm = QMessageBox()
        ret = qm.question(self.parent, '', "Are you sure to remove all the times?", qm.Yes | qm.No)
        if ret == qm.Yes:
            self.rowManager.resetTimes()


    def openWebsite(self):
        webbrowser.open(self.links["website"])


    def openModHub(self):
        webbrowser.open(self.links["modhub"])


    def openGithub(self):
        webbrowser.open(self.links["retimer"])


    def showCredits(self):
        msg = QMessageBox(self.parent)
        msg.setWindowTitle("Credits")
        msg.setText("UI + Coding   : jerrinth3glitch#6280      \n"
                    "Icon Design    : Alexis.#3047\n"
                    "Early Support : Aiivan#8227")
        msg.setInformativeText(rf"<b>Version {self.parent.version}<\b>")
        msg.setDetailedText("1. Added \"Clear Times\" button\n"
                            "2. Fixed Toggle Settings on start-up\n"
                            "3. Added \"Github\" Page\n"
                            "4. Added \"Edit Mod Message\"")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def viewFile(self):
        self.saveTimes()
        subprocess.Popen(r'explorer /select,"{}"'.format(self.saveFileName))


    def saveTimes(self):
        # main settings
        data = {"fps": self.rowManager.fps,
                "includeSubLoads": self.rowManager.includeSubLoads,
                "includePasteButtons": self.rowManager.includePasteButtons}
        # saving rows
        rowData = []
        for row in self.rowManager.rows:
            rowDict = {"signType": row.signType,
                       "text1": row.textTime1.text(),
                       "subLoad": row.textSubLoad.text(),
                       "text2": row.textTime2.text()
                       }
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
        self.rowManager.toggleIncludeSubLoads(value=data["includeSubLoads"])
        self.rowManager.toggleIncludePasteButtons(value=data["includePasteButtons"])
        # populate the row data
        for rowData in data["rows"]:
            row = self.rowManager.addRow()
            if rowData["signType"] == -1:
                row.swapValueSign()
            row.textTime1.setText(rowData["text1"])
            row.textSubLoad.setText(rowData["subLoad"])
            row.textTime2.setText(rowData["text2"])
