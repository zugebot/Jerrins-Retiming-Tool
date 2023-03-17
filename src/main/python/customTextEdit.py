# Jerrin Shirks

from PyQt5.QtWidgets import QApplication, QTextEdit
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import QVariantAnimation


class CustomTextEdit(QTextEdit):
    def __init__(self, settings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.settings = settings

        self.orig_style = None
        self.color = None
        self._animation = None

    def _animate(self, value):
        r, g, b = (int(i) + (255 - int(i)) * value for i in self.color)
        self.setStyleSheet(self.orig_style + f"color: rgb({r},{g},{b})")

    def flash(self):
        if self.orig_style is None:
            self.orig_style = self.styleSheet()
            self.color = self.settings.getTextColorTuple()
        self.setStyleSheet(self.orig_style + f"color: {self.settings.getTextColorRGB()}")
        self._animation = QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=1000
        )
        self._animation.start()







