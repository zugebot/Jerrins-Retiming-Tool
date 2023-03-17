# Jerrin Shirks

# native imports
from fbs_runtime.application_context.PyQt5 import ApplicationContext, cached_property
from PyQt5.QtCore import Qt
import sys

# custom imports
from _support import *
from _settings import Settings
from windowMain import WindowMain


class AppContext(ApplicationContext):

    @cached_property
    def ready_resources(self):
        return {
            "1st": self.get_resource("images/1st.png"),
            "copy": self.get_resource("images/copy.png"),
            "document": self.get_resource("images/document.png"),
            "eraser": self.get_resource("images/eraser.png"),
            "gear": self.get_resource("images/gear.png"),
            "gear2": self.get_resource("images/gear2.png"),
            "github": self.get_resource("images/github.png"),
            "github2": self.get_resource("images/github2.png"),
            "globe": self.get_resource("images/globe.png"),
            "globe2": self.get_resource("images/globe2.png"),
            "plus": self.get_resource("images/plus.png"),
            "plus2": self.get_resource("images/plus2.png"),
            "skull": self.get_resource("images/skull.png"),
            "trash": self.get_resource("images/trash.png"),
            "trophy2": self.get_resource("images/trophy2.png"),
            "X": self.get_resource("images/X.png")
        }


    def run(self):
        app: QApplication = QApplication([])
        settings = Settings()
        resources = self.ready_resources

        windowMain = WindowMain(app, settings, resources)
        windowMain.show()

        return self.app.exec_()


if __name__ == "__main__":
    appctxt = AppContext()
    exit_code = appctxt.run()
    sys.exit(exit_code)
