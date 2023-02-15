# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import requests
import webbrowser

# custom imports
from jLineEdit import JLineEdit
from row import Row
from windowRetimer import RetimerWindow
from windowEditModMessage import WindowEditModMessage



class WindowMain(QMainWindow):
    def __init__(self, version="1.0.0", *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.version: str = version
        self.latestVersion: str = version
        self.latestUrl: str = ""


        self.retimerWindow: RetimerWindow = RetimerWindow(self)
        self.windowEditModMessage = None

        self.alwaysOnTop: bool = True
        self.initUI()
        self.menuBar = self.menuBar()
        self.findLatestVersion()
        self.retimerWindow.loadTimes()
        self.initMenuBar()

        self.menuToggleFPS = None
        self.menuToggleSubLoads = None
        self.menuTogglePasteButtons = None
        self.menuEditModMessage = None
        self.menuOpenWebsite = None
        self.menuOpenGithub = None
        self.menuOpenModHub = None


    def openWindowEditModMessage(self):
        self.windowEditModMessage = WindowEditModMessage()
        self.windowEditModMessage.show()


    def closeEvent(self, event):
        self.retimerWindow.saveTimes()
        if self.windowEditModMessage is not None:
            self.windowEditModMessage.close()
        event.accept()


    def initUI(self):
        self.setWindowTitle("Retimer v" + self.version)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(490, 395)
        widget = QWidget()
        widget.setLayout(self.retimerWindow.layout)
        self.setCentralWidget(widget)


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


    def initMenuBar(self):
        barFile = self.menuBar.addMenu("File")
        _viewSaveFile = barFile.addAction("View Save File")
        _viewSaveFile.triggered.connect(self.retimerWindow.viewFile)

        barSettings = self.menuBar.addMenu("Settings")

        self.menuEditModMessage = QAction(QIcon("../../../icons/gear.png"), "Edit Mod Message", self)
        self.menuEditModMessage.triggered.connect(self.openWindowEditModMessage)
        barSettings.addAction(self.menuEditModMessage)


        self.menuToggleSubLoads = barSettings.addAction("Include Subloads")
        self.menuToggleSubLoads.setCheckable(True)
        self.menuToggleSubLoads.setChecked(self.retimerWindow.rowManager.includeSubLoads)
        self.menuToggleSubLoads.triggered.connect(self.retimerWindow.rowManager.toggleIncludeSubLoads)

        self.menuTogglePasteButtons = barSettings.addAction("Include Paste Buttons")
        self.menuTogglePasteButtons.setCheckable(True)
        self.menuTogglePasteButtons.setChecked(self.retimerWindow.rowManager.includePasteButtons)
        self.menuTogglePasteButtons.triggered.connect(self.retimerWindow.rowManager.toggleIncludePasteButtons)

        barWebsites = self.menuBar.addMenu("Websites")

        self.menuOpenModHub = QAction(QIcon("../../../icons/1st.png"), "Moderation Hub", self)
        self.menuOpenModHub.triggered.connect(self.retimerWindow.openModHub)
        barWebsites.addAction(self.menuOpenModHub)

        self.menuOpenWebsite = barWebsites.addAction("Open Help")
        self.menuOpenWebsite.triggered.connect(self.retimerWindow.openWebsite)

        barAbout = self.menuBar.addMenu("About")

        self.menuOpenGithub = QAction(QIcon("../../../icons/git-white.png"), "Github Page", self)
        self.menuOpenGithub.triggered.connect(self.retimerWindow.openGithub)
        barAbout.addAction(self.menuOpenGithub)

        _openCredits = barAbout.addAction("Credits")
        _openCredits.triggered.connect(self.retimerWindow.showCredits)
