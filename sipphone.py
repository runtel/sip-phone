#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui, uic
 
class SIPPhone(QtGui.QMainWindow):
  def __init__(self, parent=None):
    QtGui.QWidget.__init__(self, parent)
    uic.loadUi("sipphone.ui", self)
    self.number = ""
#    QtCore.QObject.connect(self.pushButtonDigit1, QtCore.SIGNAL("clicked()"), self.digit_key_pressed )
#    QtCore.QObject.connect(self.pushButtonDigit2, QtCore.SIGNAL("clicked()"), self.digit_key_pressed )
    QtCore.QObject.connect(self.pushButtonDigit1, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("1") )
    QtCore.QObject.connect(self.pushButtonDigit2, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("2") )
    QtCore.QObject.connect(self.pushButtonDigit3, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("3") )
    QtCore.QObject.connect(self.pushButtonDigit4, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("4") )
    QtCore.QObject.connect(self.pushButtonDigit5, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("5") )
    QtCore.QObject.connect(self.pushButtonDigit6, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("6") )
    QtCore.QObject.connect(self.pushButtonDigit7, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("7") )
    QtCore.QObject.connect(self.pushButtonDigit8, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("8") )
    QtCore.QObject.connect(self.pushButtonDigit9, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("9") )
    QtCore.QObject.connect(self.pushButtonDigit0, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("0") )

    QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.test )



  def test(self):
     #self.programmButton.setGreen(not self.programmButton.getGreen())
     self.programmButton.greenLed = not self.programmButton.greenLed
     print "test", self.programmButton.green

  def digit_key_pressed(self, par1):
    self.number = self.number + par1
    self.plainTextEditDisplay.setPlainText(self.number)
    
#    QtCore.QObject.connect(self.ui.lineEdit, QtCore.SIGNAL("returnPressed()"), self.add_entry)
 
#  def add_entry(self):
#    self.ui.lineEdit.selectAll()
#    self.ui.lineEdit.cut()
#    self.ui.textEdit.append("")
#    self.ui.textEdit.paste()

if __name__ == "__main__":
  app = QtGui.QApplication(sys.argv)
  myapp = SIPPhone()
  myapp.show()
  sys.exit(app.exec_())
