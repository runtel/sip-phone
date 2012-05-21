#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui, uic
#from mainwindow import Ui_MainWindow
 
class MyForm(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    uic.loadUi("mainwindow.ui", self)
    self.number = ""
    QtCore.QObject.connect(self.pushButtonKey1, QtCore.SIGNAL("clicked()"), self.digit_key_pressed )
    QtCore.QObject.connect(self.pushButtonKey2, QtCore.SIGNAL("clicked()"), self.digit_key_pressed )


  def digit_key_pressed(self):
    self.number = self.number + "1"
    self.plainTextEditDisplay.setPlainText(self.number)
    
#    QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("returnPressed()"), self.add_entry)
 
#  def add_entry(self):
#    self.ui.lineEdit.selectAll()
#    self.ui.lineEdit.cut()
#    self.ui.textEdit.append("")
#    self.ui.textEdit.paste()

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = MyForm()
  myapp.show()
  sys.exit(app.exec_())
