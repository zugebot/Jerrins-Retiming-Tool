# Jerrin Shirks

# native imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext
from PyQt5.QtCore import Qt
import sys

# custom imports
from src.main.python.support import *
from src.main.python.settings import Settings
from src.main.python.windows.windowMain import WindowMain


class AppContext(ApplicationContext):
    def run(self):
        app = QApplication([])
        settings = Settings("1.04.0")

        windowMain = WindowMain(app, settings)
        windowMain.show()

        return self.app.exec_()


if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
