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
        settings = Settings("1.04.0")

        palette = QPalette()

        palette.setColor(QPalette.Window, QColor(53, 53, 53))
        palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        palette.setColor(QPalette.Button, QColor(53, 53, 53))

        palette.setColor(QPalette.Base, QColor(25, 25, 25))

        palette.setColor(QPalette.HighlightedText, Qt.black)
        palette.setColor(QPalette.ToolTipBase, Qt.black)

        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.ButtonText, Qt.white)

        # settings.getTextQColor()
        text_color = settings.getTextQColor()
        palette.setColor(QPalette.BrightText, text_color)
        palette.setColor(QPalette.Link, text_color)
        palette.setColor(QPalette.Highlight, text_color)

        app.setPalette(palette)


        app.setStyle(settings.getWindowStyle())

        windowMain = WindowMain(app, settings, palette)
        windowMain.show()

        return self.app.exec_()


if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
