# Jerrin Shirks

# native imports

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPalette, QColor, QIcon, QDesktopServices
from bs4 import BeautifulSoup
import requests
import math
import json
import os



bkg_grey = "background-color: dark-grey;"
bold_green = "font: bold; color: rgb(0,150,0);"
text_green = "color: rgb(0,150,0);"
text_red = "color: red;"
bold_red = "font: bold; color: rgb(180,0,0);"
bold_cyan = "font: bold; color: rgb(42,130,218);"
bold_text = "font: bold;"
text_cyan = QColor(42, 130, 218)



def write_json(data, filename):
    with open(filename, "w") as file:
        file.write(json.dumps(data, indent=4))


def read_json(filename):
    # create the file if not already there
    if not os.path.exists(filename):
        with open(filename, 'w') as file:
            file.write("{}")
    # reads the data
    with open(filename, "r") as file:
        data = json.loads(file.read())
    return data


def getFaviconFromUrl(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    favicon = soup.find('link', rel='icon')
    if favicon:
        return favicon['href']
    return None


def getGameNameFromUrl(url):
    response = requests.get(url)
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    og_title = soup.find('meta', attrs={'name': 'og:title'})
    if og_title:
        return og_title['content'].replace(" - speedrun.com", "")
    return None



def addNewAction(menu, text_str="", func=None):
    action = menu.addAction(text_str)
    if callable(func):
        action.triggered.connect(func)
    return action


def addNewIconAction(root, menu, icon, text_str="", func=None):
    if isinstance(icon, str):
        icon = QIcon(icon)
    if isinstance(icon, QStyle.StandardPixmap):
        icon = QWidget().style().standardIcon(icon)

    action = QAction(icon, text_str, root)
    if callable(func):
        action.triggered.connect(func)
    menu.addAction(action)
    return action


def addNewIconMenu(root, menu, icon, text_str=""):
    if isinstance(icon, str):
        icon = QIcon(icon)
    if isinstance(icon, QStyle.StandardPixmap):
        icon = QWidget().style().standardIcon(icon)

    action = QMenu(icon, text_str, root)
    menu.addMenu(action)
    return action


def newCheckbox(menu, text_str="", checkable=True, checked=True, func=None):
    action = menu.addAction(text_str)
    action.setCheckable(checkable)
    action.setChecked(checked)
    if callable(func):
        action.triggered.connect(func)



def newButton(text="", fixed_width=None, func=None, hide=None, style_sheet=None):
    button: QPushButton = QPushButton(text)
    if fixed_width is not None:
        button.setFixedWidth(fixed_width)
    if callable(func):
        button.clicked.connect(func)
    if hide:
        button.hide()
    if style_sheet is not None:
        button.setStyleSheet(style_sheet)
    return button


def newQuestionBox(root, title="", message="", funcYes=None, funcNo=None, argsYes=(), argsNo=()):
    qm: QMessageBox = QMessageBox()
    ret = qm.question(root, title, message, qm.Yes | qm.No)
    if ret == qm.Yes:
        if callable(funcYes):
            if argsYes != ():
                if isinstance(argsYes, tuple):
                    return funcYes(*argsYes)
                else:
                    return funcYes(argsYes)
            else:
                return funcYes()
    elif ret == qm.No:
        if callable(funcNo):
            if argsNo != ():
                if isinstance(argsNo, tuple):
                    return funcNo(*argsNo)
                else:
                    return funcNo(argsNo)
            else:
                return funcNo()






class ClickableLabel(QLabel):
    def __init__(self, text, link):
        super().__init__()
        self.setText(f'<a href="{link}">{text}</a>')
        self.setOpenExternalLinks(True)
        self.link = link

    def mousePressEvent(self, event):
        QDesktopServices.openUrl(QUrl(self.link))








