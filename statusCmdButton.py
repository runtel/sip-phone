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
        self.status = False
        
           
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
       
        if self.status:
            pen = QtGui.QPen(QtGui.QColor(20, 20, 20), w/5, 
                QtCore.Qt.SolidLine)
        else:
            pen = QtGui.QPen(QtGui.QColor(0, 255, 0), w/5, 
                QtCore.Qt.SolidLine)
            
        qp.setPen(pen)
        qp.setBrush(QtCore.Qt.NoBrush)
#        qp.drawPoint(w - w/10, 40)
	qp.drawLine(w - w/5, 0, w, 0)


    def getStatus(self):
        return self.status

    @QtCore.pyqtSlot(bool)
    def setStatus(self, value):
        if self.status != value:
            self.status = value
            self.emit(QtCore.SIGNAL("statusChanged(bool)"), value)
            self.update()

    def resetStatus(self):
        if self.status:
            self.status = False
            self.emit(QtCore.SIGNAL("statusChanged(bool)"), value)
            self.update()

    statusLed = QtCore.pyqtProperty (bool, getStatus, setStatus, resetStatus)

if __name__ == "__main__":

    import sys
    
    app = QtGui.QApplication(sys.argv)
    widget = QStatusCmdButton()
    widget.show()
    sys.exit(app.exec_())