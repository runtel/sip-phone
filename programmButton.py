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
           
    def paintEvent(self, e):
        QtGui.QPushButton.paintEvent(self, e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

        
    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
       
        if self.green:
            pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 10, 
                QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 10, 
                QtCore.Qt.SolidLine)
            
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)


    def getGreen(self):
        return self.green

    @QtCore.pyqtSlot(bool)
    def setGreen(self, value):
        print "setGreen", value
        if self.green != value:
            self.green = value
            self.emit(QtCore.SIGNAL("greenChanged(bool)"), value)
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
        print "setRed", value
        if self.red != value:
            self.red = value
            self.emit(QtCore.SIGNAL("redChanged(bool)"), value)
            self.update()

    def resetRed(self):
        if self.red:
            self.red = False
            self.emit(QtCore.SIGNAL("redChanged(bool)"), value)
            self.update()

    redLed = QtCore.pyqtProperty (bool, getRed, setRed, resetRed)
    

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
