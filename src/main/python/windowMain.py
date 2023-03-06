# Jerrin Shirks

# native imports
from PyQt5.QtCore import Qt
import webbrowser
from functools import partial

# custom imports
from support import *
from windowRetimer import WindowRetimer
from windowSettings import WindowSettings
from windowAddPage import WindowAddPage
from windowAddTemplate import WindowAddTemplate
from windowRetimerTiny import WindowRetimerTiny



class WindowMain(QMainWindow):
    def __init__(self, app, settings, resources, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.openRowTemplateAction = None
        self.app: QApplication = app
        self.settings = settings
        self.resources = resources

        self.app.setPalette(self.settings.palette)
        self.app.setStyle(self.settings.getWindowStyle())


        # self.setWindowOpacity(1)

        self.latestUrl: str = ""

        self.windowRetimer: WindowRetimer = WindowRetimer(self)
        self.windowAddTemplate: WindowAddTemplate = None
        self.windowSettings: WindowSettings = None
        self.windowAddPage: WindowAddPage = None
        self.windowRetimerTiny: WindowRetimerTiny = None


        self.initUI()

        self.menuBar: QMenuBar = self.menuBar()
        self.initMenuBar()

        # startup funcs
        self.findLatestVersion()
        self.windowRetimer.loadSaveFile()


    def initUI(self):
        self.setTitle()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setMaximumSize(450, 360)
        self.setCentralWidget(self.windowRetimer.widget)

        shortcut = QShortcut(QKeySequence(Qt.CTRL + Qt.Key_Q), self)
        shortcut.activated.connect(self.close)


    def initFont(self):
        font = QFont()
        font.setPointSize(8)
        app.setFont(font)



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
        self.windowSettings.setGeometry(*placeOnSide(self, 350, 400, "left"))
        self.windowSettings.setWindowModality(Qt.ApplicationModal)
        self.windowSettings.show()


    def openWindowRetimerTiny(self):
        self.windowRetimerTiny = WindowRetimerTiny(self)
        self.hide()
        self.windowRetimerTiny.show()




    def updateSettings(self):
        self.windowRetimer.updateSettings()
        self.app.setStyle(self.settings.getWindowStyle())




    def closeEvent(self, event):
        self.windowRetimer.saveFile()
        self.settings.save()
        if self.windowSettings is not None:
            self.windowSettings.close()
        event.accept()


    def setTitle(self, *args):
        title = "Jerrin's Retiming Tool"
        for arg in args:
            if arg is None:
                continue
            title += f" [{arg}]"
        self.setWindowTitle(title)


    def findLatestVersion(self):
        try:
            latest = requests.get(self.settings.websiteLatest).text
            self.settings.latest_ver = latest



            if self.settings.version < latest:
                update_bar = self.menuBar.addMenu("Update")
                addNewAction(update_bar, f"Download {latest} !", self.downloadUpdate)
        except Exception as e:
            print(e)
            "do nothing lol, no internet"


    def addWebsitePage(self):
        pass


    def downloadUpdate(self):
        webbrowser.open(self.settings.websiteDir)


    def showCredits(self):
        msg = QMessageBox(self)
        msg.setWindowTitle("Credits")
        msg.setText("UI + Coding   : jerrinth3glitch#6280      "
                    "\nIcon Design    : Alexis.#3047"
                    "\nEarly Support : Aiivan#8227"
                    "\n"
                    f"\nReleased {self.settings.date}")

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


    def viewTemplateFolder(self):
        self.settings.openFileDialog(self.settings.templateFolder)


    def initMenuBar(self):
        self.menuBar.setStyleSheet("QMenu::separator { background-color: red; }")
        self.menuBar.setFocusPolicy(Qt.StrongFocus)


        fileMenu: QMenu = self.menuBar.addMenu("File")

        addNewIconAction(self, "Ctrl+O", fileMenu, self.resources["document"], "&Open Folder", self.windowRetimer.viewDocumentFolder)
        addNewIconAction(self, "Ctrl+F", fileMenu, self.resources["eraser"], "Single Row Mode", self.openWindowRetimerTiny)
        addNewIconAction(self, "Ctrl+S", fileMenu, self.resources["gear2"], "Settings", self.openWindowSettings)


        editMenu: QMenu = self.menuBar.addMenu("Edit")

        addNewIconAction(self, "Ctrl+D", editMenu, self.resources["copy"], "Copy Rows as Text", self.windowRetimer.copyRowsAsText)
        addNewIconAction(self, "Ctrl+A", editMenu, self.resources["copy"], "Copy Mod Message", self.windowRetimer.copyModMessage)
        addNewIconAction(self, "Ctrl+Z", editMenu, self.resources["trash"], "Clear Rows", self.windowRetimer.resetSplits)
        addNewIconAction(self, "Ctrl+X", editMenu, self.resources["skull"], "Clear Times", self.windowRetimer.resetTimes)

        # gif = self.settings.iconDir + "spinning.gif"
        # self.actionClearRows = AnimatedIconAction(gif, "Clear Times")
        # self.actionClearRows.addToMenu(editMenu, self.windowRetimer.resetTimes, "Ctrl+X")


        templateMenu: QMenu = self.menuBar.addMenu("Templates")
        # addNewIconAction(self, templateMenu, self.iconify("document"), "View &Template Folder", self.viewTemplateFolder, "Ctrl+T")

        self.openRowTemplateAction: QAction = addNewIconAction(self, None, templateMenu, self.resources["document"], "&Open Template")
        if len(self.getTemplates()) == 0:
            self.openRowTemplateAction.setVisible(False)

        addNewIconAction(self, "Ctrl+N", templateMenu, self.resources["plus"], "&New Template", self.openWindowAddTemplate)
        self.populateTemplates()


        websiteMenu: QMenu = self.menuBar.addMenu("Websites")
        addNewIconAction(self, "Ctrl+W", websiteMenu, self.resources["trophy2"], "Moderation Hub", partial(self.settings.openLink, "modhub"))
        # addNewIconAction(self, websiteMenu, self.resources["globe2"], "Edit Pages [TBD]", self.openWindowAddPage, "Ctrl+E")


        aboutMenu: QMenu = self.menuBar.addMenu("About")
        addNewIconAction(self, None, aboutMenu, self.resources["github2"], "Github Page", partial(self.settings.openLink, "github"))
        # addNewAction(aboutMenu, "How to Use [WIP]", partial(self.settings.openLink, "website"))
        addNewAction(aboutMenu, "Credits", self.showCredits)



    def getTemplates(self):
        files = os.listdir(self.settings.templateFolder)
        templates = []
        for file in files:
            filename = self.settings.dirJoiner(self.settings.templateFolder, file)
            if not os.path.isfile(filename):
                continue
            if not file.endswith(".rt"):
                continue
            templates.append(file)
        return templates


    def populateTemplates(self):
        templates = self.getTemplates()

        menu = QMenu()
        for template in templates:
            filename = self.settings.dirJoiner(self.settings.templateFolder, template)
            data = read_json(filename)
            name = data.get("display-name", "N/A")
            addNewAction(menu, name, partial(self.windowRetimer.loadTemplate, filename))
        self.openRowTemplateAction.setMenu(menu)
