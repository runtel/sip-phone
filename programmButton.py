#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui, uic

class QProgrammButton(QtGui.QPushButton):
    __pyqtSignals__ = ("greenChanged(bool)")

    def __init__(self, parent = None):
        QtGui.QPushButton.__init__(self, parent)
        self.green = False
        
    def getGreen(self):
        return self.green

    @QtCore.pyqtSignature("setGreen(int)")
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
	
	greenLed = QtCore.pyqtProperty ("bool", getGreen, setGreen, resetGreen)
           
    def paintEvent(self, e):
        print "paint ", self.green
        QtGui.QPushButton.paintEvent(self, e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

        
    def drawWidget(self, qp):
        size = self.size()
        w = size.width()
        h = size.height()
        print "drawWidget", self.green
       
        if self.green:
            pen = QtGui.QPen(QtGui.QColor(20, 20, 20), 10, 
                QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), 10, 
                QtCore.Qt.SolidLine)
            
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
        qp.drawRect(0, 0, w-1, h-1)

