# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon



class WindowEditModMessage(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.WindowStaysOnTopHint)
        self.setWindowTitle("Edit Mod Message")
        self.width = 490
        self.setFixedSize(self.width, 395)

        # Create a button and add it to the main window
        self.textBox = QPlainTextEdit(self)

        font = self.textBox.font()
        font.setPointSize(16)
        self.textBox.setFont(font)
        self.textBox.setFixedSize(self.width, 87)

        self.textBox.setPlaceholderText("Line 1\nLine 2\nLine 3\nLine 4\nLine 5")


"""


Mod Note: Retimed to 30.100 (Start 0:05.917, End: 0:36.017)


H     : hours,
M     : minutes,
S     : seconds,
MS    : milliseconds,
PM    : padded_minutes,
PS    : padded_seconds,
1MS   : one_prec_millis,
2MS   : two_prec_millis,
3MS   : three_prec_millis,
ST    : start_time,
ET    : end_time,
TT    : total_time,
SF    : start_frame,
EF    : end_frame,
TF    : total_frames,
FPS   : fps

SL_H  
SL_M  
SL_S  
SL_MS 
SL_PM 
SL_PS 
SL_1MS
SL_2MS
SL_3MS





"""
