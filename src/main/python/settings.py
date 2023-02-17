# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import QStyleFactory
import platform

# custom imports
from support import *
import subprocess
import os



class Settings:
    def __init__(self, version="1.0.0"):
        self.os_index = 0
        self.documentFolder: str = ""
        self.prepareOS()


        self.filename = self.documentFolder + "settings.json"



        self.data: dict = read_json(self.filename)

        self.version = version
        self.latest_ver = version


        self.iconDir: str = self.data.get("icon-dir", "../../../icons/")
        self.latestDownload: str = "https://jerrin.org/downloads/retimer/latest.json"

        self.url_links = {
            "website": 'https://jerrin.org',
            "modhub": 'https://www.speedrun.com/modhub',
            "retimer": 'https://github.com/zugebot/Speedrun-Retimer',
            "mod-message-formatting": "https://github.com/zugebot/Speedrun-Retimer/blob/main/MOD_FORMAT.md"
        }


        self.default = {
            "fps": 30,
            "include-sub-loads": False,
            "include-paste-buttons": True,
            "show-hints": True,
            "window-style": 0,
            "mod-message": "Mod Note: Retimed to {TT}.",
        }

        self.windowStyleList = QStyleFactory.keys()
        if "Fusion" in self.windowStyleList:
            self.default["window-style"] = self.windowStyleList.index("Fusion")


    def get(self, key):
        return self.data.get(key, self.default.get(key, None))


    def set(self, key, value):
        self.data[key] = value



    def prepareOS(self):
        os_name = platform.system()
        if os_name == "Windows":
            self.os_index = 0
        elif os_name == "Linux":
            self.os_index = 1
        elif os_name == "Darwin":
            self.os_index = 2
        else:
            self.os_index = 3
        # finds the documents folder
        self.documentFolder = {
            0: "C:\\Users\\{}\\Documents\\Speedrun-Retimer\\",
            1: "/home/{}/Documents/Speedrun-Retimer/",
            2: "/Users/{}/Documents/Speedrun-Retimer/",
            3: ""
        }[self.os_index].format(os.getlogin())
        os.makedirs(os.path.dirname(self.documentFolder), exist_ok=True)
        os.makedirs(os.path.dirname(self.dirJoiner([self.documentFolder, "rowTemplates", ""])), exist_ok=True)


    def dirJoiner(self, items: list) -> str:
        segment = ["\\", "/", "/", "/"][self.os_index]
        return segment.join(items)


    def save(self):
        write_json(self.data, self.filename)


    def getWindowStyle(self):
        return self.windowStyleList[self.get("window-style")]


    def openFileDialog(self, filename):
        if self.os_index == 0:  # windows
            subprocess.Popen(r'explorer /select,"{}"'.format(filename))
        elif self.os_index == 1:  # linux
            subprocess.Popen(["xdg-open", "--select", filename])
        elif self.os_index == 2:  # Mac
            subprocess.Popen(["open", "-R", filename])
