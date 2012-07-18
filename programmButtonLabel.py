#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui

class QProgrammButtonLabel(QtGui.QLabel):

    def __init__(self, parent = None):
        super(QProgrammButtonLabel, self).__init__(parent)
	self.number = -1
    
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
    widget = QProgrammButtonLabel()
    widget.show()
    sys.exit(app.exec_())
