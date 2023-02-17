# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from support import *








class WindowSettings(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.settings = parent.settings

        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Settings")
        self.width = 400
        self.setFixedSize(self.width, 400)


        # SETTINGS, preset
        self._windowStyle = self.settings.get("window-style")
        self._includePasteButtons = self.settings.get("include-paste-buttons")
        self._includeSubLoads = self.settings.get("include-sub-loads")
        self._showHints = self.settings.get("show-hints")
        self._modMessage = self.settings.get("mod-message")



        # CREATES THE WINDOW
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # window option section (use self.windowSettingsGrid)
        self.windowOptionsGroup = QGroupBox("Window Options")
        self.windowOptionsGroup.setFlat(True)
        self.windowSettingsGrid = QGridLayout()
        self.windowSettingsGrid.setAlignment(Qt.AlignTop)
        self.windowOptionsGroup.setLayout(self.windowSettingsGrid)
        self.layout.addWidget(self.windowOptionsGroup)



        # window options
        self.styleLabel = QLabel("Window Style")
        self.styleCombo = QComboBox()
        self.styleCombo.addItems(self.settings.windowStyleList)
        self.styleCombo.setCurrentIndex(self._windowStyle)
        self.styleCombo.currentIndexChanged.connect(self.changeWindowStyle)
        self.checkPaste = QCheckBox("Include Paste Buttons")
        self.checkPaste.stateChanged.connect(self.checkboxChangedPasteButtons)
        self.checkSubload = QCheckBox("Include Sub-load Textboxes")
        self.checkSubload.stateChanged.connect(self.checkboxChangedSubLoads)
        self.checkShowHints = QCheckBox("Show Text Hints")
        self.checkShowHints.stateChanged.connect(self.checkboxChangedShowHints)



        self.windowSettingsGrid.addWidget(self.styleLabel, 0, 0)
        self.windowSettingsGrid.addWidget(self.styleCombo, 0, 1)
        self.windowSettingsGrid.addWidget(self.checkPaste, 1, 0, 1, 4)
        self.windowSettingsGrid.addWidget(self.checkSubload, 2, 0, 1, 4)
        self.windowSettingsGrid.addWidget(self.checkShowHints, 3, 0, 1, 4)




        # mod option section (use self.modSettingsGrid)
        self.modOptionsGroup = QGroupBox("Mod Message Options")
        self.modOptionsGroup.setFlat(True)
        self.modSettingsGrid = QGridLayout()
        self.modSettingsGrid.setAlignment(Qt.AlignTop)
        self.modOptionsGroup.setLayout(self.modSettingsGrid)
        self.layout.addWidget(self.modOptionsGroup)

        # mod options

        self.learnClickLabel = ClickableLabel("How to format your mod message...", self.settings.url_links["mod-message-formatting"])

        self.modMessageEdit = QTextEdit()
        self.modMessageEdit.textChanged.connect(self.modMessageChanged)

        self.modSettingsGrid.addWidget(self.learnClickLabel, 0, 0, 1, 1)
        self.modSettingsGrid.addWidget(self.modMessageEdit, 1, 0, 1, 1)





        # bottom stuff
        self.bottomLayout = QHBoxLayout()

        self.leftSide = QHBoxLayout()
        self.leftSide.setAlignment(Qt.AlignLeft)
        self.bottomLayout.addLayout(self.leftSide)

        self.rightSide = QHBoxLayout()
        self.rightSide.setAlignment(Qt.AlignRight)
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
        self.styleCombo.setCurrentIndex(self._windowStyle)
        self.checkPaste.setChecked(self._includePasteButtons)
        self.checkSubload.setChecked(self._includeSubLoads)
        self.checkShowHints.setChecked(self._showHints)
        self.modMessageEdit.setText(self._modMessage)


    def changeWindowStyle(self, i):
        self._windowStyle = i


    def checkboxChangedPasteButtons(self, state):
        self._includePasteButtons = (state == Qt.Checked)


    def checkboxChangedSubLoads(self, state):
        self._includeSubLoads = (state == Qt.Checked)


    def checkboxChangedShowHints(self, state):
        self._showHints = (state == Qt.Checked)


    def modMessageChanged(self):
        self._modMessage = self.modMessageEdit.toPlainText()


    def restoreDefaults(self):
        self._windowStyle = self.settings.default["window-style"]
        self._includePasteButtons = self.settings.default["include-paste-buttons"]
        self._includeSubLoads = self.settings.default["include-sub-loads"]
        self._showHints = self.settings.default["show-hints"]
        self._modMessage = self.settings.default["mod-message"]
        self.reloadSettingsScreen()


    def saveSettings(self):
        self.applySettings()
        self.closeSettings()


    def closeSettings(self):
        self.close()


    def applySettings(self):
        self.settings.set("window-style", self._windowStyle)
        self.settings.set("include-sub-loads", self._includeSubLoads)
        self.settings.set("include-paste-buttons", self._includePasteButtons)
        self.settings.set("show-hints", self._showHints)
        self.settings.set("mod-message", self._modMessage)
        self.settings.save()
        self.parent.updateSettings()
