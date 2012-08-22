#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui

class QProgrammButton(QtGui.QPushButton):
    greenChanged = QtCore.pyqtSignal(bool)
    
    def __init__(self, parent = None):
        super(QProgrammButton, self).__init__(parent)
        self.number = -1
        self.green = False
        self.red = False
        self.opacity = 100
        self.timer = QtCore.QTimer()
        self.timer.setInterval(500)

        QtCore.QObject.connect(self.timer, QtCore.SIGNAL("timeout()"), self.updateTimer)
        
           
    def updateTimer(self):
        self.opacity = 100 if self.opacity == 50 else 50
        self.update()

    def paintEvent(self, e):
        QtGui.QPushButton.paintEvent(self, e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

    def drawWidget(self, qp):
        self.setStyleSheet("")
        if self.green:
            self.setStyleSheet("background-color: rgba(154, 205, 50, %d%s)" % (self.opacity, "%"))
        if self.red:
            self.setStyleSheet("background-color: rgba(255, 00, 00, %d%s)" % (self.opacity, "%"))

    def getGreen(self):
        return self.green

    @QtCore.pyqtSlot(bool)
    def setGreen(self, value):
        #print "setGreen", value
        self.red = False
        self.opacity = 100
        if self.green != value:
            self.green = value
            self.emit(QtCore.SIGNAL("greenChanged(bool)"), value)
            #self.setStyleSheet("QPushButton { background-color: %s }" % "green")
            self.update()

    def resetGreen(self):
        if self.green:
            self.green = False
            self.emit(QtCore.SIGNAL("greenChanged(bool)"), value)
            self.update()

    greenLed = QtCore.pyqtProperty (bool, getGreen, setGreen, resetGreen)
    
    def getRed(self):
        return self.red

    @QtCore.pyqtSlot(bool)
    def setRed(self, value):
        #print "setRed", value
        self.green = False
        self.opacity = 100
        if self.red != value:
            self.red = value
            self.emit(QtCore.SIGNAL("redChanged(bool)"), value)
            #self.setStyleSheet("QPushButton { background-color: %s }" % "red")
            self.update()

    def resetRed(self):
        if self.red:
            self.red = False
            self.emit(QtCore.SIGNAL("redChanged(bool)"), value)
            self.update()

    redLed = QtCore.pyqtProperty (bool, getRed, setRed, resetRed)
    
    def startFlash(self):
        self.timer.start()

    def stopFlash(self):
        self.timer.stop()

    # свойство порядковый номер
    def getNumber(self):
        return self.number

    def setNumber(self, value):
        self.number = value

    def resetNumber(self):
        self.number = -1

    numberButton = QtCore.pyqtProperty (int, getNumber, setNumber, resetNumber)


if __name__ == "__main__":

    import sys
    
    app = QtGui.QApplication(sys.argv)
    widget = QProgrammButton()
    widget.show()
    sys.exit(app.exec_())
