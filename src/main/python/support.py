# Jerrin Shirks
import typing

# native imports

from PyQt5.QtWidgets import *
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QPalette, QColor, QIcon, QDesktopServices
from bs4 import BeautifulSoup
import requests
import math
import json
import os

"""
bkg_grey = "background-color: dark-grey;"
text_red = "color: red;"
bold_red = "font: bold; color: rgb(180,0,0);"
bold_cyan = "font: bold; color: rgb(42,130,218);"
bold_text = "font: bold;"
text_cyan = "color: rgb(42,130,218);" # QColor(42, 130, 218)
"""


def makeStyle(bold=False, text_color=None, bkg_color=None):
    style_str: str = ""

    if bold:
        style_str += "font: bold; "

    if text_color is not None:
        if isinstance(text_color, QColor):
            text_color = list(text_color.getRgb()[:3])

        if isinstance(text_color, str):
            style_str += f"color: {text_color}"
        elif type(text_color) in [tuple, list]:
            style_str += f"color: rgb({text_color[0]},{text_color[1]},{text_color[2]});"

    if bkg_color is not None:
        if isinstance(bkg_color, str):
            style_str += f"background-color: {bkg_color}"
        elif type(bkg_color) in [tuple, list]:
            style_str += f"background-color: rgb({bkg_color[0]},{bkg_color[1]},{bkg_color[2]});"

    return style_str


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


def addNewAction(menu, text_str="", func=None, shortcut=None):
    action: QAction = menu.addAction(text_str)
    if callable(func):
        action.triggered.connect(func)
    if shortcut is not None:
        action.setShortcut(shortcut)
    return action


def addNewIconAction(root, menu, icon, text_str="", func=None, shortcut=None):
    if isinstance(icon, str):
        icon = QIcon(icon)
    if isinstance(icon, QStyle.StandardPixmap):
        icon = QWidget().style().standardIcon(icon)

    action: QAction = QAction(icon, text_str, root)
    if callable(func):
        action.triggered.connect(func)
    if shortcut is not None:
        action.setShortcut(shortcut)
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


def newButton(text="", width=None, func=None, hide=None,
              styleSheet=None, minWidth=None, maxWidth=None):
    button: QPushButton = QPushButton(text)

    if width is not None:
        button.setFixedWidth(width)

    if minWidth:
        button.setMinimumWidth(minWidth)
    elif width:
        button.setMinimumWidth(width)

    if maxWidth:
        button.setMaximumWidth(maxWidth)
    elif width:
        button.setMaximumWidth(width)

    if callable(func):
        button.clicked.connect(func)
    if hide:
        button.hide()
    if styleSheet is not None:
        button.setStyleSheet(styleSheet)
    return button


def newQuestionBox(root, title="", message="", funcYes=None, funcNo=None, argsYes=(), argsNo=()):
    qm: QMessageBox = QMessageBox()
    ret = qm.question(root, title, message, qm.Yes | qm.No)
    if ret == qm.Yes:
        if not callable(funcYes):
            return True
        if argsYes != ():
            if isinstance(argsYes, tuple):
                return funcYes(*argsYes)
            else:
                return funcYes(argsYes)
        else:
            return funcYes()

    elif ret == qm.No:
        if not callable(funcNo):
            return False
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


def placeOnSide(root, newWidth, newHeight, direction):
    screen = QApplication.desktop().screenGeometry()
    newTop = root.geometry().top()

    if direction == "left":
        newLeft = root.geometry().left() - newWidth

        if newLeft < screen.left():
            newLeft = root.geometry().right()

        return newLeft, newTop, newWidth, newHeight


def removeChildren(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        if widget:
            widget.deleteLater()


def newQObject(
        self=None,

        text: str = "",
        temp: str = None,

        readOnly: bool = None,

        func=None,

        width: int = None,
        height: int = None,

        spacing: int = None,
        alignment=None,
        sizeConstraint=None,

        minWidth: int = None,
        maxWidth: int = None,
        minHeight: int = None,
        maxHeight: int = None,

        margins: list = None,

        styleSheet: str = None,
        hidden: bool = None):

    self = self()

    if text:
        self.setText(text)
    if temp:
        self.setPlaceholderText(temp)

    if hidden is not None:
        if hidden is True:
            self.setHidden(hidden)

    if isinstance(self, QLayout):
        if spacing:
            self.setSpacing(spacing)
        if alignment:
            self.setAlignment(alignment)
        if sizeConstraint:
            self.setSizeConstraint(sizeConstraint)


    if width is not None:
        self.setFixedWidth(width)

    if minWidth:
        self.setMinimumWidth(minWidth)
    elif width:
        self.setMinimumWidth(width)

    if maxWidth:
        self.setMaximumWidth(maxWidth)
    elif width:
        self.setMaximumWidth(width)

    if height:
        self.setFixedHeight(height)

    if minHeight:
        self.setMinimumHeight(minHeight)
    elif height:
        self.setMinimumHeight(height)

    if maxHeight:
        self.setMaximumHeight(maxHeight)
    elif height:
        self.setMaximumHeight(height)

    if margins:
        self.setContentsMargins(*margins)

    if readOnly is not None:
        self.setReadOnly(readOnly)

    if styleSheet:
        self.setStyleSheet(styleSheet)

    if callable(func):
        if isinstance(self, QLineEdit):
            self.textChanged[str].connect(func)
        elif isinstance(self, QPushButton):
            self.clicked.connect(func)

    return self

