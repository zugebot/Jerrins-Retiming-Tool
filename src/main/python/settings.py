# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import QStyleFactory
import subprocess
import webbrowser
import platform
import os

# custom imports
from support import *
import release


class Settings:
    def __init__(self):
        self.os_index = 3
        self.documentFolder: str = ""
        self.templateFolder: str = ""
        self.iconFolder: str = ""
        self.fontSize: int = 0
        self.prepareOS()

        self.filename_settings = self.documentFolder + "settings.json"
        self.filename_pages = self.documentFolder + "pages.json"
        self.data: dict = read_json(self.filename_settings)

        self.version = release.version
        self.latest_ver = release.version
        self.date = release.date

        self.iconDir: str = self.data.get("icon-dir", "../resources/")

        self.websiteBase = "https://jerrin.org/downloads/retimer/"
        self.websiteDir = f"{self.websiteBase}download_page.html"
        self.websiteLatest = f"{self.websiteBase}latest.json"


        self.url_links = {
            "website": 'https://www.jerrin.org',
            "modhub": 'https://www.speedrun.com/modhub',
            "github": 'https://github.com/zugebot/Speedrun-Retimer',
            "mod-message-formatting": "https://github.com/zugebot/Speedrun-Retimer/blob/main/MOD_FORMAT.md"
        }

        self.default = {
            "fps": 30,
            "show-sub-loads": False,
            "show-paste-buttons": True,
            "show-hints": True,
            "decimal-accuracy": 3,
            "mod-message": "Mod Note: Retimed to {TT}.",

            "window-styles": QStyleFactory.keys(),
            "window-style": None,
            "text-color": 0,

            "grey1": [53, 53, 53],
            "grey2": [40, 40, 40],
            "grey3": [25, 25, 25],
            "black": [0, 0, 0]
        }

        self.getWindowStyle()

        # self.textColorList = ["Green", "Cyan"]
        # self.textColorValues = [[78, 228, 78], "cyan"]

        self.textThemes = {
            "Green": {
                "text": [78, 228, 78],
                "anti-text": [200, 30, 30],
                "highlight": [140, 228, 140]
            },
            "Cyan": {
                "text": [0, 238, 238],
                "anti-text": [200, 30, 30],
                "highlight": [0, 180, 180]
            },
            "Yellow": {
                "text": [255, 213, 36],
                "anti-text": [200, 30, 30],
                "highlight": [139, 128, 0]
            },
            "Purple": {
                "text": [163, 134, 217],
                "anti-text": [200, 30, 30],
                "highlight": [120, 69, 217]
            }
        }

        self.palette: QPalette = self.makePalette()


    def get(self, key):
        return self.data.get(key, self.default.get(key, None))


    def getDict(self):
        data = dict()
        for key in self.default:
            data[key] = self.get(key)
        return data


    def getColorRGB(self, key):
        return "rgb({},{},{})".format(*(i for i in self.get(key)))

    def getQColor(self, key):
        return QColor(*self.get(key))


    def getTextTheme(self):
        return self.textThemes[[i for i in self.textThemes][self.get("text-color")]]


    def getTextColorTuple(self):
        theme = self.getTextTheme()
        return tuple(theme["text"])


    def getTextColorRGB(self):
        theme = self.getTextTheme()
        return "rgb({},{},{})".format(*(i for i in theme["text"]))

    def getTextQColor(self):
        theme = self.getTextTheme()
        return QColor(*theme["text"])

    def getHighlightRGB(self):
        theme = self.getTextTheme()
        return "rgb({},{},{})".format(*(i for i in theme["highlight"]))

    def getHighlightQColor(self):
        theme = self.getTextTheme()
        return QColor(*theme["highlight"])

    def getAntiTextColorRGB(self):
        theme = self.getTextTheme()
        return "rgb({},{},{})".format(*(i for i in theme["anti-text"]))

    def getAntiTextQColor(self):
        theme = self.getTextTheme()
        return QColor(*theme["anti-text"])




    def set(self, key, value):
        self.data[key] = value


    def prepareOS(self):
        os_name = platform.system()
        # find which os
        OS_NAMES = ["Windows", "Linux", "Darwin"]
        if os_name in OS_NAMES:
            self.os_index = OS_NAMES.index(os_name)
        # each platform has different default-font sizes (cringe)
        self.fontSize = {0: 8, 1: 8, 2: 11, 3: 8}[self.os_index]
        # finds the documents folder
        self.documentFolder = {
            0: "C:\\Users\\{}\\Documents\\Speedrun-Retimer\\",
            1: "/home/{}/Documents/Speedrun-Retimer/",
            2: "/Users/{}/Documents/Speedrun-Retimer/",
            3: ""
        }[self.os_index].format(os.getlogin())
        # create the directories
        self.templateFolder = self.dirJoiner(self.documentFolder, "rowTemplates", "")
        self.iconFolder = self.dirJoiner(self.documentFolder, "srcIcons", "")
        os.makedirs(os.path.dirname(self.documentFolder), exist_ok=True)
        os.makedirs(os.path.dirname(self.templateFolder), exist_ok=True)
        os.makedirs(os.path.dirname(self.iconFolder), exist_ok=True)


    def dirJoiner(self, *args) -> str:
        segment = ["\\", "/", "/", "/"][self.os_index]
        return segment.join(list(args))


    def save(self):
        write_json(self.data, self.filename_settings)


    def getWindowStyle(self):

        # defaults
        if self.get("window-style") is None:
            if "Fusion" in self.get("window-styles"):
                index = self.get("window-styles").index("Fusion")
                self.default["window-style"] = index
                self.data["window-style"] = index
            else:
                self.default["window-style"] = 0
                self.data["window-style"] = 0

        return self.get("window-styles")[self.get("window-style")]


    def openFileDialog(self, filename):
        if self.os_index == 0:  # windows
            subprocess.Popen(r'explorer /select,"{}"'.format(filename))
        elif self.os_index == 1:  # linux
            subprocess.Popen(["xdg-open", "--select", filename])
        elif self.os_index == 2:  # Mac
            subprocess.Popen(["open", "-R", filename])
        else:
            print("Unsupported OS")


    def _toQColor(self, color):
        if isinstance(color, str):
            color = QColor(color)
        else:
            color = QColor(color[0], color[1], color[2])
        return color

    """
    def getTextQColor(self):
        return self._toQColor(self.textColorValues[self.get("text-color")])
    """


    def openLink(self, link):
        webbrowser.open(self.url_links[link])

    def makePalette(self):
        palette: QPalette = QPalette()

        grey1 = self.getQColor("grey1")
        grey3 = self.getQColor("grey3")
        text = self.getTextQColor()
        highlight = self.getHighlightQColor()

        palette.setColor(QPalette.Window, grey1)
        palette.setColor(QPalette.AlternateBase, grey1)
        palette.setColor(QPalette.Button, grey1)
        palette.setColor(QPalette.Base, grey3)
        palette.setColor(QPalette.HighlightedText, Qt.black)
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.ButtonText, Qt.white)

        palette.setColor(QPalette.BrightText, text)
        palette.setColor(QPalette.Link, text)
        palette.setColor(QPalette.Highlight, highlight)

        # palette.setColor(QPalette.Background, highlight)
        # palette.setColor(QPalette.Foreground, Qt.white)

        return palette
