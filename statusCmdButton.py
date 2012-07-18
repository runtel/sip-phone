#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    Рисует кнопки с отображенем текущго состояния вкл/выкл

"""

import sys
from PyQt4 import QtCore, QtGui

class QStatusCmdButton(QtGui.QPushButton):
    status = QtCore.pyqtSignal(bool)

    def __init__(self, parent = None):
        super(QStatusCmdButton, self).__init__(parent)
        self.status = True
        self.trueIcon = ""
        self.falseIcon = ""
        
#	self.resetTrueIcon()
#	self.resetFalseIcon();
#	self.resetStatus()
           
    def paintEvent(self, e):
        QtGui.QPushButton.paintEvent(self, e)
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawWidget(qp)
        qp.end()

        
    def drawWidget(self, qp):
	pass
#        size = self.size()
#        w = size.width()
#        h = size.height()
       
#        if self.status:
#            pen = QtGui.QPen(QtGui.QColor(20, 20, 20), w/5, 
#                QtCore.Qt.SolidLine)
#        else:
#            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), w/5, 
#                QtCore.Qt.SolidLine)
#            
#        qp.setPen(pen)
#        qp.setBrush(QtCore.Qt.NoBrush)
#        qp.drawPoint(w - w/10, 40)
#	qp.drawLine(w - w/5, 0, w, 0)


    def getStatus(self):
        return self.status

    @QtCore.pyqtSlot(bool)
    def setStatus(self, value):
#        if self.status != value:
            self.status = value
            if self.status:
    		self.setIcon(QtGui.QIcon(self.trueIcon))
    	    else:
		self.setIcon(QtGui.QIcon(self.falseIcon))

            self.emit(QtCore.SIGNAL("statusChanged(bool)"), value)

            self.update()

    def resetStatus(self):
       self.setStatus(False)

    statusLed = QtCore.pyqtProperty (bool, getStatus, setStatus, resetStatus)


    def getTrueIcon(self):
        return self.trueIcon

    def setTrueIcon(self, value):
	self.trueIcon = value
	self.setStatus(self.status)

    def resetTrueIcon(self):
	self.trueIcon = ""
	self.setStatus(self.status)

    trueIconProp = QtCore.pyqtProperty ("QString", getTrueIcon, setTrueIcon, resetTrueIcon)

    def getFalseIcon(self):
        return self.falseIcon

    def setFalseIcon(self, value):
	self.falseIcon = value
	self.setStatus(self.status)
	

    def resetFalseIcon(self):
	self.falseIcon = ""
	self.setStatus(self.status)

    falseIconProp = QtCore.pyqtProperty ("QString", getFalseIcon, setFalseIcon, resetFalseIcon)


if __name__ == "__main__":

    import sys
    
    app = QtGui.QApplication(sys.argv)
    widget = QStatusCmdButton()
    widget.show()
    sys.exit(app.exec_())