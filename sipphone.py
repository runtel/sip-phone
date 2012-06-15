#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui, uic

from programmButton import QProgrammButton
from statusCmdEventFilter import installEventFilter


class SIPPhone(QtGui.QMainWindow):
  def __init__(self, parent = None):
    QtGui.QWidget.__init__(self, parent)
    uic.loadUi("sipphone.ui", self)
    self.number = ""
    # назначаем обработчики кнопок
    # цифровых
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

    # кнопка #, позвонить
    QtCore.QObject.connect(self.pushButtonDigitGrid, QtCore.SIGNAL("clicked()"), lambda:self.dial() )
    
    # командные кнопки 
    QtCore.QObject.connect(self.pushButton_CmdClear, QtCore.SIGNAL("clicked()"), lambda:self.clear() )
    QtCore.QObject.connect(self.pushButton_CmdRedial, QtCore.SIGNAL("clicked()"), lambda:self.redial() )
    QtCore.QObject.connect(self.pushButton_CmdMute, QtCore.SIGNAL("clicked()"), lambda:self.mute() )
    QtCore.QObject.connect(self.pushButton_CmdDND, QtCore.SIGNAL("clicked()"), lambda:self.dnd() )
    QtCore.QObject.connect(self.pushButton_CmdConf, QtCore.SIGNAL("clicked()"), lambda:self.conf() )
    QtCore.QObject.connect(self.pushButton_CmdHangUp, QtCore.SIGNAL("clicked()"), lambda:self.hangup() )
    QtCore.QObject.connect(self.pushButton_CmdRecord, QtCore.SIGNAL("clicked()"), lambda:self.record() )
    QtCore.QObject.connect(self.pushButton_CmdBackspace, QtCore.SIGNAL("clicked()"), lambda:self.backspace() )
    QtCore.QObject.connect(self.pushButton_CmdDial, QtCore.SIGNAL("clicked()"), lambda:self.dial() )
    QtCore.QObject.connect(self.pushButton_CmdRegister, QtCore.SIGNAL("clicked()"), lambda:self.register() )



    # программируемые кнопки
    # создаем список наших кнопок
    self.programmButtons = self.groupBoxProgrammButton.findChildren(QProgrammButton)

#    clicked_function = [lambda i = i: self.clickedProgrammButton(i) for i in xrange(len(self.programmButtons))]
#    rightclicked_function = [lambda i = i: self.rightclickedProgrammButton(i) for i in xrange(len(self.programmButtons))]
#    mouseleave_function = [lambda i = i: self.mouseleaveProgrammButton(i) for i in xrange(len(self.programmButtons))]

#    eventfilter = statusCmdEventFilter(self)

    for i in xrange(0, len(self.programmButtons)):
	if self.programmButtons[i].numberButton >= 0:
	    eventfilter = installEventFilter(self.programmButtons[i])
	    eventfilter.clicked.connect(self.clickedProgrammButton)
	    eventfilter.rightclicked.connect(self.rightclickedProgrammButton)
	    eventfilter.mouseleave.connect(self.mouseleaveProgrammButton)

	
#		eventfilter.clicked.connect(clicked_function[i])
#		eventfilter.rightclicked.connect(rightclicked_function[i])
#		eventfilter.mouseleave.connect(mouseleave_function[i])
	
    # обработчики событий
    # изменение состояния регистрации
    QtCore.QObject.connect(self.pushButton_CmdRegister, QtCore.SIGNAL("statusChanged(bool)"), self.registerStatusChanged )

    

    QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.test )

  # обработчик сообщений от клавы
  def event(self,e):
    if e.type() == QtCore.QEvent.KeyPress:
        # проверяем на нажатие 0-9, добавляем к нашей строке
        if e.key() in xrange(QtCore.Qt.Key_0, QtCore.Qt.Key_9):
	    self.number = self.number + '%c' % e.key()
	    self.plainTextEditDisplay.setPlainText(self.number)
	elif e.key() == QtCore.Qt.Key_Backspace: 	# забой
            self.backspace()
	elif e.key() == QtCore.Qt.Key_Return:	# собственно позвонить
	    self.dial()
	    
    return QtGui.QMainWindow.event(self,e)

  def test(self):
    self.programmButton.greenLed = not self.programmButton.greenLed    
    print len(self.groupBoxProgrammButton.findChildren(QProgrammButton))
    

  # обработчик сообщений от цифровых кнопок
  def digit_key_pressed(self, par1):
    self.number = self.number + par1
    self.plainTextEditDisplay.setPlainText(self.number)
    

  # обработчик нажатий программируемых кнопок
  def clickedProgrammButton(self, number):
    print "programm button left click", number
    
  def rightclickedProgrammButton(self, number):
    print "programm button right click", number

  def mouseleaveProgrammButton(self, number):
    print "mouseleave button", number
    
  # звонит по SIP
  def dial(self):
    # тут вписываемся для звонка
    if len(self.number):
	self.plainTextEditDisplay.setPlainText("Dial to :" + self.number)
    else: 
	self.plainTextEditDisplay.setPlainText("Need number")

  # очистка набранного номера
  def clear(self):
    self.number = ""
    self.plainTextEditDisplay.setPlainText(self.number)

  # перезвонить
  def redial(self):
    # тут вписываемся для перезвона
    self.plainTextEditDisplay.setPlainText("Redial to :" + self.number)
    
  
  # включить/отключть микрофон
  def mute(self):
     # проверить на наличие разговора
     self.pushButton_CmdMute.statusLed = not self.pushButton_CmdMute.statusLed
     if self.pushButton_CmdMute.statusLed:
        print u"микрофон отключен"
     else: 
        print u"микрофон включен"

  # включить/выключить режим не беспокоить
  def dnd(self):
     self.pushButton_CmdDND.statusLed = not self.pushButton_CmdDND.statusLed
     if self.pushButton_CmdDND.statusLed:
        print u"включен режим не беспокоить"
     else: 
        print u"выключен режим не беспокоить"

  # организовать конференцию
  def conf(self):
     print u"конференция"

  # закончить вызов
  def hangup(self):
     print u"конец разговора"
  
  # начать запись разговора
  def record(self):     
     # проверить на наличие разговора
     self.pushButton_CmdRecord.statusLed = not self.pushButton_CmdRecord.statusLed
     if self.pushButton_CmdRecord.statusLed:
        print u"началась запись разговора"
     else: 
        print u"закончилась запись разговора"

  def backspace(self):
    self.number = self.number[:-1]
    self.plainTextEditDisplay.setPlainText(self.number)
    
  def register(self):
    # проверить что еще не зарегистрирован
    # выплняем регистрацию, в случа успеха зажигаем led и меняем надпись на кнопке
    # изменение статуса пораждает событие которое изменит надпись на кнопке
    self.pushButton_CmdRegister.statusLed = not self.pushButton_CmdRegister.statusLed

  def registerStatusChanged(self, value):
    if self.pushButton_CmdRegister.statusLed:
       self.pushButton_CmdRegister.setText("unregister")
    else:
       self.pushButton_CmdRegister.setText("register")
      
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
