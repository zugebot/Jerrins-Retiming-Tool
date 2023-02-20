# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon, QKeyEvent
import requests
import webbrowser
from functools import partial

# custom imports
from support import *
from row import Row
from timeLineEdit import TimeLineEdit
from windowRetimer import WindowRetimer
from windowSettings import WindowSettings
from windowAddPage import WindowAddPage
from windowAddTemplate import WindowAddTemplate



class WindowMain(QMainWindow):
    def __init__(self, app, settings, palette, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.openRowTemplateAction = None
        self.app: QApplication = app
        self.settings = settings
        self.palette: QPalette = palette

        self.latestUrl: str = ""
        self.updateThread: Thread = None


        self.windowRetimer: WindowRetimer = WindowRetimer(self)
        self.windowSettings: WindowSettings = None
        self.windowAddPage: WindowAddPage = None

        self.initUI()
        self.menuBar: QMenuBar = self.menuBar()
        self.initMenuBar()

        # startup funcs
        self.findLatestVersion()
        self.windowRetimer.loadSaveFile()


    def iconify(self, filename):
        return self.settings.iconDir + filename


    def openWindowAddPage(self):
        self.windowAddPage = WindowAddPage(self)
        self.windowAddPage.setWindowModality(Qt.ApplicationModal)
        self.windowAddPage.show()


    def openWindowAddTemplate(self):
        self.windowAddTemplate = WindowAddTemplate(self)
        self.windowAddTemplate.setWindowModality(Qt.ApplicationModal)
        self.windowAddTemplate.show()


    def openWindowSettings(self):
        self.windowSettings = WindowSettings(self)

        # position the new window to the left of the main window
        new_window_width = 350
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
        self.windowRetimer.saveFile()
        self.settings.save()
        if self.windowSettings is not None:
            self.windowSettings.close()
        event.accept()


    def keyPressEvent(self, event: QKeyEvent):
        print(event.key())
        super().keyPressEvent(event)


    def initUI(self):
        self.setTitle("Speedrun Retimer")
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        # self.setMaximumSize(470, 400)
        widget = QWidget()
        widget.setLayout(self.windowRetimer.layout)
        self.setCentralWidget(widget)


    def setTitle(self, *args):
        title = "Speedrun Retimer"
        for arg in args:
            if arg is None:
                continue
            title += f" [{arg}]"
        self.setWindowTitle(title)


    def findLatestVersion(self):
        try:
            latest = requests.get(self.settings.latestVersionLink).text.split("\n")
            self.settings.latestDownloadUrl = f"{self.settings.latestVersionLink}{latest[1]}".replace(" ", "%20")
            print(self.settings.version, latest[0])
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
        msg.setDetailedText(
                            "1. Added Settings!"
                            "\n  - Toggles for theme style and color"
                            "\n  - Settings on startup actually work"
                            "\n2. Added Custom Mod Messages!"
                            "\n3. Added Templates!"
                            "\n  - Templates allow for saving and "
                            "\n    loading row presets."

                            )
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()


    def openWebsite(self):
        webbrowser.open(self.settings.url_links["website"])


    def openModHub(self):
        webbrowser.open(self.settings.url_links["modhub"])


    def openGithub(self):
        webbrowser.open(self.settings.url_links["retimer"])


    def viewTemplateFolder(self):
        self.settings.openFileDialog(self.settings.templateFolder)


    def initMenuBar(self):
        self.menuBar.setStyleSheet("QMenu::separator { background-color: red; }")
        self.menuBar.setFocusPolicy(Qt.StrongFocus)


        fileMenu: QMenu = self.menuBar.addMenu("File")

        addNewIconAction(self, fileMenu, self.iconify("document"), "&Open Folder", self.windowRetimer.viewDocumentFolder, "Ctrl+O")
        addNewIconAction(self, fileMenu, self.iconify("X.png"), "Clear Splits", self.windowRetimer.resetSplits, "Ctrl+Z")
        addNewIconAction(self, fileMenu, self.iconify("X.png"), "Clear Times", self.windowRetimer.resetTimes, "Ctrl+X")
        addNewIconAction(self, fileMenu, self.iconify("gear2.png"), "&Settings", self.openWindowSettings, "Ctrl+S")


        templateMenu: QMenu = self.menuBar.addMenu("Templates")
        # addNewIconAction(self, templateMenu, self.iconify("document"), "View &Template Folder", self.viewTemplateFolder, "Ctrl+T")

        self.openRowTemplateAction = addNewIconAction(self, templateMenu, self.iconify("document"), "&Open Template", None)
        addNewIconAction(self, templateMenu, self.iconify("plus.png"), "&New Template", self.openWindowAddTemplate, "Ctrl+N")
        self.populateTemplates()


        websiteMenu: QMenu = self.menuBar.addMenu("Websites")
        addNewIconAction(self, websiteMenu, self.iconify("trophy2.png"), "&Moderation Hub", self.openModHub, "Ctrl+M")
        addNewIconAction(self, websiteMenu, self.iconify("globe2.png"), "&Edit Pages [TBD]", self.openWindowAddPage, "Ctrl+E")


        aboutMenu: QMenu = self.menuBar.addMenu("About")
        addNewIconAction(self, aboutMenu, self.iconify("github2.png"), "&Github Page", self.openGithub, "Ctrl+G")
        addNewAction(aboutMenu, "&Help", self.openWebsite, "Ctrl+H")
        addNewAction(aboutMenu, "C&redits", self.showCredits, "Ctrl+R")



    def populateTemplates(self):
        files = os.listdir(self.settings.templateFolder)
        print("templates:", files)
        templates = []
        for file in files:
            filename = self.settings.dirJoiner(self.settings.templateFolder, file)
            if not os.path.isfile(filename):
                continue
            if not file.endswith(".rt"):
                continue
            templates.append(file)


        menu = QMenu()
        for template in templates:
            filename = self.settings.dirJoiner(self.settings.templateFolder, template)


            data = read_json(filename)
            name = data.get("display-name", "N/A")


            addNewAction(menu, name, partial(self.windowRetimer.loadTemplate, filename))
            print("added", name)

        self.openRowTemplateAction.setMenu(menu)
