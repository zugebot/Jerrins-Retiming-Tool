# Jerrin Shirks

# native imports
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor, QIcon

# custom imports
from row import Row



class RowManager:
    def __init__(self, parent):
        self.parent = parent
        self.fps: int = 30
        self.modMessage: str = "Mod Note: Retimed to {}."
        self.modMessageWithSubLoad: str = "Mod Note: Retimed to {} ({} in subloads)."
        self.includeMilliseconds: bool = True
        self.includeFPS: bool = True
        self.includeSubLoads: bool = True
        self.includePasteButtons: bool = True
        self.rows: List[Row] = []


    def resetRows(self):
        while len(self.rows) > 1:
            self.delRow()
        self.rows[0].clear()


    def resetTimes(self):
        for row in self.rows:
            row.textTime1.setText("")
            row.textTime2.setText("")
            row.textSubLoad.setText("")


    def addRow(self):
        rowNumber = len(self.rows)
        newRow = Row(self, rowNumber)
        self.rows.append(newRow)
        self.parent.rowForm.addRow(newRow.layout)
        return newRow


    def delRow(self):
        # can only delete rows if there are 2> rows.
        if len(self.rows) <= 1:
            return
        rowIntToDelete = len(self.rows) - 1
        self.parent.rowForm.removeRow(rowIntToDelete)
        self.rows.pop()


    def formatToTime(self, value=0):
        isNegative = value < 0
        value = abs(value)
        # rounds num to the nearest frame (if useFPS is on)
        if self.includeFPS:
            value += 0.001
            value = value - (value % 1) % (1 / self.fps)
        # create all the components
        milli = int(round(value % 1, 3) * 1000)
        seconds = int(value % 60)
        minutes = int((value / 60) % 60)
        hours = int((value / 3600) % 24)
        days = int((value / 86400) % 7)
        weeks = int((value / 604800))
        # new formatting technique
        formattedTime = ""
        if weeks != 0:
            formattedTime += f"{weeks}w "
        if days != 0:
            formattedTime += f"{days}d "
        if hours != 0:
            formattedTime += str(hours) + ":"
            formattedTime += "{:0>2d}".format(minutes) + ":"
        else:
            formattedTime += str(minutes) + ":"
        # add seconds
        formattedTime += "{:0>2d}".format(seconds)
        # add milliseconds
        if self.includeMilliseconds:
            print(milli)
            formattedTime += ".{:0>3d}".format(milli)
        # re-add the "-" if the num was originally neg.
        if isNegative:
            formattedTime = "–" + formattedTime
        return formattedTime


    def updateModTotalTime(self):
        finalTime = 0
        subLoadTime = 0
        allRowsEmpty = True
        for row in self.rows:
            if not row.textFinalTime.isEmpty():
                allRowsEmpty = False
                row.updateTotalTime(updateMod=False)
                finalTime += row.textFinalTime.getValue()
                subLoadTime += row.textSubLoad.getValue()
        if allRowsEmpty or finalTime == 0:
            self.parent.labelModMessage.setText("")
        else:
            finalTime = self.formatToTime(finalTime)
            if subLoadTime == 0:
                message = self.modMessage.format(finalTime)
            else:
                subLoadTime = self.formatToTime(subLoadTime)
                message = self.modMessageWithSubLoad.format(finalTime, subLoadTime)
            self.parent.labelModMessage.setText(message)



    def toggleIncludeSubLoads(self, value=None):
        if value is None:
            self.includeSubLoads = not self.includeSubLoads
        else:
            self.includeSubLoads = value

        for row in self.rows:
            if self.includeSubLoads:
                row.textSubLoad.show()
            else:
                row.textSubLoad.clear()
                row.textSubLoad.hide()


    def toggleIncludePasteButtons(self, value=None):
        if value is None:
            self.includePasteButtons = not self.includePasteButtons
        else:
            self.includePasteButtons = value

        for row in self.rows:
            if self.includePasteButtons:
                row.buttonPaste1.show()
                row.buttonPaste2.show()
            else:
                row.buttonPaste1.hide()
                row.buttonPaste2.hide()


    def updateFPS(self):
        self.parent.LineEditFPS.isValid()
        self.fps = self.parent.LineEditFPS.getValue()
        if self.fps == 0:
            self.fps = 30
        self.updateModTotalTime()
