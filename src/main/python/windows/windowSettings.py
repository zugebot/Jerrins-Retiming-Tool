# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon
from functools import partial

# custom imports
from src.main.python.support import *
from src.main.python.frameTime import FrameTime



class WindowSettings(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle(f"Settings [{self.settings.version}]")

        self.setFixedWidth(350)

        # vars yay
        bold_text = makeStyle(bold=True, text_color=self.settings.get("text-color"))


        # SETTINGS, preset
        self.data = self.settings.getDict()

        # CREATES THE WINDOW
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # window option section (use self.windowSettingsGrid)
        self.windowOptionsGroup = QGroupBox("Window Options")
        self.windowOptionsGroup.setFlat(True)
        self.windowSettingsGrid = newQObject(QGridLayout, alignment=Qt.AlignTop)
        self.windowOptionsGroup.setLayout(self.windowSettingsGrid)
        self.layout.addWidget(self.windowOptionsGroup)


        # self.button.clicked.connect(partial(self.func, False))

        # window options
        self.styleLabel = QLabel("Window Style")
        self.styleCombo = QComboBox()
        self.styleCombo.addItems(self.settings.get("window-styles"))
        self.styleCombo.setCurrentIndex(self.data["window-style"])
        self.styleCombo.currentIndexChanged.connect(self.changeWindowStyle)

        self.textColorLabel = QLabel("Theme Color\n[Needs Restart]")
        self.textColorCombo = QComboBox()
        self.textColorCombo.addItems([i for i in self.settings.textThemes]) # self.settings.textColorList)
        self.textColorCombo.setCurrentIndex(self.data["text-color"])
        self.textColorCombo.currentIndexChanged.connect(partial(self.comboBoxChanged, "text-color"))

        self.checkPaste = QCheckBox("Show Paste Buttons")
        self.checkPaste.stateChanged.connect(partial(self.checkboxStateChanged, "show-paste-buttons"))

        self.checkSubload = QCheckBox("Show Sub-load Textboxes")
        self.checkSubload.stateChanged.connect(partial(self.checkboxStateChanged, "show-sub-loads"))

        self.checkShowHints = QCheckBox("Show Text Hints")
        self.checkShowHints.stateChanged.connect(partial(self.checkboxStateChanged, "show-hints"))




        self.windowSettingsGrid.addWidget(self.styleLabel, 0, 0)
        self.windowSettingsGrid.addWidget(self.styleCombo, 0, 1)
        self.windowSettingsGrid.addWidget(self.textColorLabel, 0, 2)
        self.windowSettingsGrid.addWidget(self.textColorCombo, 0, 3)
        self.windowSettingsGrid.addWidget(self.checkPaste, 2, 0, 1, 2)
        self.windowSettingsGrid.addWidget(self.checkSubload, 2, 2, 1, 2)
        self.windowSettingsGrid.addWidget(self.checkShowHints, 3, 0, 1, 2)




        # mod option section (use self.modSettingsGrid)
        self.modOptionsGroup = QGroupBox("Mod Message Options")
        self.modOptionsGroup.setFlat(True)
        self.modSettingsGrid = newQObject(QGridLayout, alignment=Qt.AlignTop)
        self.modOptionsGroup.setLayout(self.modSettingsGrid)
        self.layout.addWidget(self.modOptionsGroup)

        # mod options
        self.learnClickLabel = ClickableLabel("Formatting Guide", self.settings.url_links["mod-message-formatting"])
        self.learnClickLabel.setStyleSheet(bold_text)

        self.modMessageEdit = QTextEdit()
        self.modMessageEdit.textChanged.connect(self.modMessageChanged)
        self.modMessageEdit.verticalScrollBar().valueChanged.connect(self.modMessageEditScrolled)
        self.modMessageEdit.setStyleSheet("border-radius: 2px;")
        self.modMessageView = QTextEdit()
        self.modMessageView.setReadOnly(True)
        self.modMessageView.setStyleSheet("border-radius: 2px;")

        self.exampleFrameTime = FrameTime()
        self.exampleFrameTime.setMilliseconds(30100)
        self.exampleFrameTime.setStartAndEnd(5917, 36017)

        self.exampleLabel = newQObject(QLabel, text="Current Formatted Example", styleSheet=bold_text)


        self.modSettingsGrid.addWidget(self.learnClickLabel, 0, 1, 1, 1)
        self.modSettingsGrid.addWidget(self.modMessageEdit, 1, 1, 1, 1)
        self.modSettingsGrid.addWidget(self.exampleLabel, 2, 1, 1, 1)
        self.modSettingsGrid.addWidget(self.modMessageView, 3, 1, 1, 1)




        # bottom stuff
        self.bottomLayout = QHBoxLayout()

        self.leftSide = newQObject(QHBoxLayout, alignment=Qt.AlignLeft)
        self.bottomLayout.addLayout(self.leftSide)

        self.rightSide = newQObject(QHBoxLayout, alignment=Qt.AlignRight)
        self.bottomLayout.addLayout(self.rightSide)


        self.buttonRestore = newButton("Restore Defaults", None, self.restoreDefaults)
        self.leftSide.addWidget(self.buttonRestore)

        self.buttonSave = newButton("Save", None, self.saveSettings)
        self.buttonCancel = newButton("Cancel", None, self.closeSettings)
        self.buttonApply = newButton("Apply", None, self.applySettings)

        self.rightSide.addWidget(self.buttonSave)
        self.rightSide.addWidget(self.buttonCancel)
        self.rightSide.addWidget(self.buttonApply)

        self.layout.addLayout(self.bottomLayout)

        self.reloadSettingsScreen()



    def reloadSettingsScreen(self):
        self.textColorCombo.setCurrentIndex(self.data["text-color"])
        self.styleCombo.setCurrentIndex(self.data["window-style"])
        self.checkPaste.setChecked(self.data["show-paste-buttons"])
        self.checkSubload.setChecked(self.data["show-sub-loads"])
        self.checkShowHints.setChecked(self.data["show-hints"])
        self.modMessageEdit.setText(self.data["mod-message"])


    def checkboxStateChanged(self, key, state):
        self.data[key] = (state == Qt.Checked)


    def comboBoxChanged(self, key, index):
        self.data[key] = index


    def changeWindowStyle(self, i):
        self.data["window-style"] = i


    def modMessageChanged(self):
        self.data["mod-message"] = self.modMessageEdit.toPlainText()
        message = self.exampleFrameTime.createModMessage(self.data["mod-message"])
        self.modMessageView.setText(message)
        scroll_val = self.modMessageEdit.verticalScrollBar().value()
        self.modMessageView.verticalScrollBar().setValue(scroll_val)


    def modMessageEditScrolled(self, value):
        self.modMessageView.verticalScrollBar().setValue(value)


    def restoreDefaults(self):
        self.data = self.settings.default.copy()
        self.reloadSettingsScreen()


    def saveSettings(self):
        self.applySettings()
        self.closeSettings()


    def applySettings(self):
        for key in self.data:
            self.settings.set(key, self.data[key])
        self.settings.save()
        self.parent.updateSettings()


    def closeSettings(self):
        self.close()
