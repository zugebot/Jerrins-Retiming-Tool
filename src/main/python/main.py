# Jerrin Shirks

# native imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor
import sys

# custom imports
from support import *
from settings import Settings
from windowMain import WindowMain


class AppContext(ApplicationContext):
    def run(self):
        app = QApplication([])

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor(25, 25, 25))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.ToolTipBase, Qt.black)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor(53, 53, 53))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Link, text_cyan)
        palette.setColor(QPalette.Highlight, text_cyan)

        palette.setColor(QPalette.HighlightedText, Qt.black)
        app.setPalette(palette)

        settings = Settings("1.04.0")
        app.setStyle(settings.getWindowStyle())

        windowMain = WindowMain(app, settings)
        windowMain.show()

        return self.app.exec_()


if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
