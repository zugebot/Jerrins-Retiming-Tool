# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
import requests
import webbrowser

# custom imports
from support import *
from row import Row
from jLineEdit import JLineEdit
from windowRetimer import WindowRetimer
from windowSettings import WindowSettings



class WindowMain(QMainWindow):
    def __init__(self, app, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app: QApplication = app
        self.settings = settings

        self.latestUrl: str = ""


        self.windowRetimer: WindowRetimer = WindowRetimer(self)
        self.windowSettings: WindowSettings = None

        self.initUI()
        self.menuBar: QMenuBar = self.menuBar()
        self.initMenuBar()

        # startup funcs
        self.findLatestVersion()
        self.windowRetimer.loadTimes()


    def iconify(self, filename):
        return self.settings.iconDir + filename


    def openWindowSettings(self):
        self.windowSettings = WindowSettings(self)

        # position the new window to the left of the main window
        new_window_width = 400
        new_window_height = 400
        screen = QApplication.desktop().screenGeometry()
        new_window_left = self.geometry().left() - new_window_width
        new_window_right = new_window_left + new_window_width
        new_window_top = self.geometry().top()

        # adjust the position of the new window if necessary to ensure it is fully visible on the screen
        if new_window_left < screen.left():
            new_window_right += (screen.left() - new_window_left)
            new_window_left = screen.left()
        elif new_window_right > screen.right():
            new_window_left -= (new_window_right - screen.right())
            new_window_right = screen.right()

        self.windowSettings.setGeometry(new_window_left, new_window_top, new_window_width, new_window_height)

        self.windowSettings.setWindowModality(Qt.ApplicationModal)
        self.windowSettings.show()



    def updateSettings(self):
        self.windowRetimer.updateSettings()
        self.app.setStyle(self.settings.getWindowStyle())


    def closeEvent(self, event):
        self.windowRetimer.saveTimes()
        self.settings.save()
        if self.windowSettings is not None:
            self.windowSettings.close()
        event.accept()


    def initUI(self):
        self.setWindowTitle("Retimer v" + self.settings.version)
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setFixedSize(490, 395)
        widget = QWidget()
        widget.setLayout(self.windowRetimer.layout)
        self.setCentralWidget(widget)


    def findLatestVersion(self):
        try:
            latest = requests.get(self.settings.latestDownload + "latest.json").text.split("\n")
            self.settings.latestDownloadUrl = f"{self.settings.latestDownload}{latest[1]}".replace(" ", "%20")
            if self.settings.version < latest[0]:
                update_bar = self.menuBar.addMenu("Update")
                addNewAction(update_bar, f"Download {self.settings.latest_ver}!", self.downloadUpdate)
        except Exception as e:
            print(e)
            "do nothing lol, no internet"


    def addWebsitePage(self):
        pass


    def downloadUpdate(self):
        webbrowser.open(self.latestUrl)


    def showCredits(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Credits")
        msg.setText("UI + Coding   : jerrinth3glitch#6280      \n"
                    "Icon Design    : Alexis.#3047\n"
                    "Early Support : Aiivan#8227")
        msg.setInformativeText(rf"<b>Version {self.settings.version}<\b>")
        msg.setDetailedText("1. Added \"Clear Times\" button\n"
                            "2. Fixed Toggle Settings on start-up\n"
                            "3. Added \"Github\" Page\n"
                            "4. Added \"Edit Mod Message\"")
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def openWebsite(self):
        webbrowser.open(self.settings.url_links["website"])


    def openModHub(self):
        webbrowser.open(self.settings.url_links["modhub"])


    def openGithub(self):
        webbrowser.open(self.settings.url_links["retimer"])


    def initMenuBar(self):

        barFile = self.menuBar.addMenu("File")
        addNewIconAction(self, barFile, QStyle.SP_DirIcon, "View Save File", self.windowRetimer.viewFile)
        addNewIconAction(self, barFile, QStyle.SP_DirIcon, "Open Row Template", None)
        barFile.addSeparator()
        barFile.addSeparator()
        addNewIconAction(self, barFile, QStyle.SP_FileDialogListView, "Save Rows as Template", None)
        barFile.addSeparator()
        barFile.addSeparator()
        addNewIconAction(self, barFile, self.iconify("gear.png"), "Settings", self.openWindowSettings)

        barWebsites = self.menuBar.addMenu("Websites")
        addNewIconAction(self, barWebsites, self.iconify("1st.png"), "Moderation Hub", self.openModHub)
        addNewIconAction(self, barWebsites, self.iconify("globe.png"), "Edit Pages", self.addWebsitePage)

        barAbout = self.menuBar.addMenu("About")
        addNewIconAction(self, barAbout, self.iconify("github.png"), "Github Page", self.openGithub)
        addNewAction(barAbout, "Help", self.openWebsite)
        addNewAction(barAbout, "Credits", self.showCredits)


