#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""
import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3

class infoDocWidgeta1(QtGui.QDockWidget):

    def __init__(self,  title, parent = None):
        QtGui.QDockWidget.__init__(self, title, parent)        
        uic.loadUi("infoshow.ui", self)
        
class infoDocWidgeta2(QtGui.QDockWidget):

    def __init__(self,  title, parent = None):
        QtGui.QDockWidget.__init__(self, title, parent)
        uic.loadUi("infoshow1ui.ui", self)



class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        uic.loadUi("test.ui", self)
        self.setLayout(self.gridLayout)
#        self.createDockWindows()

    def createDockWidget1(self, name, size):
        dock = infoDocWidgeta1(name, self)
#        dock.setWidget(vc)
        return dock;

    def createDockWidget2(self, name, size):
        dock = infoDocWidgeta2(name, self)
#        dock.setWidget(vc)
        return dock;

    def createDockWindows(self):
        dock1 = self.createDockWidget1("Dock1", (0.5, 0.75))
        self.addDockWidget(QtCore.Qt.TopDockWidgetArea, dock1)
        dock2 = self.createDockWidget2("Dock2", (0.5, 0.75))
        self.addDockWidget(QtCore.Qt.BottomDockWidgetArea, dock2)



if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = MainWindow()
#    widget = infoDocWidgeta("Dock1")
    widget.show()
    sys.exit(app.exec_())
    sys.exit(0)


