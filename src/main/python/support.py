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

from typing import List

"""
bkg_grey = "background-color: dark-grey;"
text_red = "color: red;"
bold_red = "font: bold; color: rgb(180,0,0);"
bold_cyan = "font: bold; color: rgb(42,130,218);"
bold_text = "font: bold;"
text_cyan = "color: rgb(42,130,218);" # QColor(42, 130, 218)
"""


def makeStyle(text_color=None, bkg_color=None, bold=False):
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

    if icon is None:
        action: QAction = QAction(text_str, root)
    else:
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


def removeLastChild(layout):
    widget = layout.takeAt(layout.count() - 1).widget()
    widget.setParent(None)


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










def makeTable(data,
              boldRow: int or List[int] = None,
              boldCol: int or List[int] = None,
              code: int or List[int] = None,
              sep: int or dict = None,
              show_index: bool = False,
              direction: int or str = 0,
              separation: int = 1,
              vert_line=None,
              debug: bool = False) -> str:
    """
    :param vert_line:
    :type vert_line:
    :param separation:
    :type separation:
    :param data: a list of objects, lists, or other data.
    :param boldRow: real
    :param boldCol: real
    :param code: horizontal indexes of items that should be surrounded by ``.
    :param sep: dict of horizontal indexes with str's to separate args.
    :param show_index: a bool that adds an index to the first item if true.
    :param direction: justifies or centers text in code blocks this direction.
    :param debug: prints stuff to terminal
    :return: A table of all represented data parsed with above arguments.
    """

    # parsing data
    if vert_line is None:
        vert_line = []
    if data is []:
        return None
    if not isinstance(data, list):
        data = [data]

    # parsing boldRow
    if boldRow is None:
        boldRow = []
    if isinstance(boldRow, int):
        boldRow = [boldRow]

    # parsing boldCol
    if boldCol is None:
        boldCol = []
    if isinstance(boldCol, int):
        boldCol = [boldCol]

    # parsing code
    if code is None:
        code = []
    if isinstance(code, int):
        code = [code]

    # parsing sep arg
    if sep is None:
        sep = {}
    if isinstance(sep, int):
        sep = [sep]

    # 0: right, 1: left, 2: center
    # parsing direction arg
    if isinstance(direction, str):
        if direction.lower() in ["r", "right"]:
            direction = 0
        elif direction.lower() in ["l", "left"]:
            direction = 1
        elif direction.lower() in ["c", "center"]:
            direction = 2
    elif not isinstance(direction, int):
        direction = 0

    # Step 1: make sure that every item in the data is a list
    # also get the longest list in data
    max_size = 0
    for index, item in enumerate(data):
        if type(item) == tuple:
            item = list(item)

        if isinstance(item, list):
            size = len(item)
        else:
            item = [item]
            size = 0

        if size > max_size:
            max_size = size

        data[index] = item

    # Step 2: make sure every item in data is the same length (row wise per item, not str)
    show_index_length = len(str(len(data)))
    if show_index:
        max_size += 1
        code = [i + 1 for i in code]
        code.insert(0, 0)

    for index, item in enumerate(data):

        if show_index:
            item.insert(0, f"{index+1}.".rjust(show_index_length))

        if len(item) < max_size:
            to_add = max_size - len(item)
            data[index].extend([None] * to_add)

    # Step 3: this gets the longest items per vertical index
    line_segments = len(data[0])
    max_length_list = []

    for index in range(line_segments):
        max_length = 0

        for item in range(len(data)):
            if data[item][index] is None:
                continue

            length: int = len(str(data[item][index]))
            if length > max_length:
                max_length = length

        max_length_list.append(max_length)


    # Step 3.3, stretches a line horizontally from vert_line arg
    for vert_index in vert_line:
        print(data[vert_index])
        print(len(data), print(len(data[0])), len(max_length_list))
        data[vert_index] = [(i * max_length_list[n])[:max_length_list[n]] for n, i in enumerate(data[vert_index])]


    # step 3.5
    if debug:
        for i in data:
            print(i)
        print("lengths", max_length_list)
        print("boxed", code)
        input()

    # final step 4
    final_string = []
    for index, item in enumerate(data, start=0):
        string: str = ""

        is_code_block = False

        # add each segment
        for seg_index in range(max_size):
            seg_part = ""

            segment = data[index][seg_index]

            if segment is None:
                segment = ""

            # if current is NOT block and last is block <3
            elif not is_code_block and seg_index in code:
                seg_part += "``"

            is_code_block = seg_index in code

            # add the main part of the string
            if direction == 0: # right
                seg_part += f"{str(segment).rjust(max_length_list[seg_index])}"
            elif direction == 1: # left
                seg_part += f"{str(segment).ljust(max_length_list[seg_index])}"
            elif direction == 2:  # center
                seg_part += f"{str(segment).center(max_length_list[seg_index])}"

            # add if this is code block but next isn't, finishing it
            if seg_index in code and seg_index + 1 not in code:
                seg_part += "``"

            # vertical bold
            if seg_index in boldCol:
                seg_part = f"**{seg_part}**"

            string += seg_part


            # add the spacer
            if seg_index < line_segments:

                if seg_index in sep:
                    if data[index][seg_index + 1] is None:
                        string += " "*len(sep[seg_index])
                    else:
                        string += f"{sep[seg_index]}"
                else:
                    string += " " * separation

        if index in boldRow:
            string = f"**{string}**"

        final_string.append(string)

    text = "\n".join(final_string)
    return text

















