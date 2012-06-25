#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
import pickle
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

#       clicked_function = [lambda i = i: self.clickedProgrammButton(i) for i in xrange(len(self.programmButtons))]
#       rightclicked_function = [lambda i = i: self.rightclickedProgrammButton(i) for i in xrange(len(self.programmButtons))]
#       mouseleave_function = [lambda i = i: self.mouseleaveProgrammButton(i) for i in xrange(len(self.programmButtons))]

        for i in xrange(0, len(self.programmButtons)):
            if self.programmButtons[i].numberButton >= 0:
                eventfilter = installEventFilter(self.programmButtons[i])
                eventfilter.mouseenter.connect(self.mouseenterProgrammButton)
                eventfilter.mouseleave.connect(self.mouseleaveProgrammButton)

                QtCore.QObject.connect(self.programmButtons[i], QtCore.SIGNAL("clicked()"), self.clickedProgrammButton)

                # обработчик контекстного меню
                self.programmButtons[i].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                QtCore.QObject.connect(self.programmButtons[i], QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.programmButtonsContextMenu )

        # обработчики событий
        # изменение состояния регистрации
        QtCore.QObject.connect(self.pushButton_CmdRegister, QtCore.SIGNAL("statusChanged(bool)"), self.registerStatusChanged )

        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL("clicked()"), self.test )

        # инициализаируем конфигурацию
        self.cfgInit()


    def cfgInit(self):
        """
        метод инициализирует и
        читает конфигурацию из файла
        """
        self.cfg = {}

        # потом загружаем из файла     
        with open('cfg.pick', 'rb') as f:
            self.cfg = pickle.load(f)


    def saveCfg(self):
        """
        метод записывает всю конфигурацию в файл
        """

        with open('cfg.pick', 'wb') as f:
            pickle.dump(self.cfg, f)


    def programmButtonsContextMenu(self, position):
        """
        метод обработчик сообщения контекстного меню от программных кнопок
        """

        # получили отправителя сообщения
        programmButton = self.sender()

        # создаем QLineEdit для ввода инфы
        editWidget = QtGui.QLineEdit()
        callNumber = self.getCallNumberProgrammButton(programmButton.numberButton)
        if callNumber:
            editWidget.setText(callNumber)

        # создаем контекстное меню
        menu = QtGui.QMenu()

        # создаем action для добавления в меню
        wac = QtGui.QWidgetAction(menu)
        wac.setDefaultWidget(editWidget)

        # добаляем созданый action в меню
        menu.addAction(wac)


        def editOk(menu, edit, numberButton):
            """
            обработчик нажатия enter на QLineEdit в меню, возможно криво, по другому не придумал
            """
            # сохраняем введенный текст в нашей конфиге
            if not self.cfg.has_key("buttons"):
                self.cfg["buttons"] = {}
            self.cfg["buttons"][numberButton] = edit.text().__str__()
            menu.close()
            self.saveCfg()

        # связываем обработчик и сигнал
        QtCore.QObject.connect(editWidget, QtCore.SIGNAL("returnPressed()"), lambda:editOk(menu, editWidget, programmButton.numberButton))

        # открываем меню
        menu.exec_(programmButton.mapToGlobal(position))


    def getCallNumberProgrammButton(self, numberButton):
        """
        метод возвращает значение кнопки
        Nono если на кнопке ни чего не прописано
        """
        # в словаре есть ключ "buttons"
        if self.cfg.has_key("buttons"):
            # есть ключ по номеру кнопки
            if self.cfg["buttons"].has_key(numberButton):
                return self.cfg["buttons"][numberButton]
        return None


    def event(self,e):
        """
        обработчик сообщений от клавиатуры
        """
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


    def on_menuProperts_triggered(self, checked = None):
        """
        обработчик сообщения от меню "menuProperts"
        """
        # тут создадим окошко с настройками
        print "action3"


    def test(self):
        self.programmButton.greenLed = not self.programmButton.greenLed    
        print len(self.groupBoxProgrammButton.findChildren(QProgrammButton))


    def digit_key_pressed(self, par1):
        """
        обработчик сообщений от цифровых кнопок
        """
        self.number = self.number + par1
        self.plainTextEditDisplay.setPlainText(self.number)


    def clickedProgrammButton(self):
        """
        обработчик нажатий программируемых кнопок
        """
        # узнаем номер закрепленный за кнопкой и звонм на него
        callNumber = self.getCallNumberProgrammButton(self.sender().numberButton)
        if callNumber:
            self.number = callNumber
            self.dial()


    def mouseenterProgrammButton(self, number):
        """
        обработчик сообщения мышь над программируемой кнопокой
        """
        # узнаем номер закрепленный за кнопкой
        callNumber = self.getCallNumberProgrammButton(number)
        if callNumber:
            self.statusBar.showMessage("call to:" + callNumber)


    def mouseleaveProgrammButton(self, number):
        """
        обработчик сообщения мышь покинула программиуемую кнопку
        """
        self.statusBar.clearMessage()


    def dial(self):
        """
        метод инициализируем вызов по SIP
        """
        # тут вписываемся для звонка
        if len(self.number):
            self.plainTextEditDisplay.setPlainText("Dial to :" + self.number)
        else: 
            self.plainTextEditDisplay.setPlainText("Need number")


    def clear(self):
        """
        метод обработчик кнопки clear
        очищает набранный номер
        """
        self.number = ""
        self.plainTextEditDisplay.setPlainText(self.number)


    def redial(self):
        """        
        метод обработчик кнопки redial
        перезванивает по последнему номеру
        """
        # тут вписываемся для перезвона
        self.plainTextEditDisplay.setPlainText("Redial to :" + self.number)


    def mute(self):
        """
        метод обработчик кнопки mute
        отключает/выключает микрофон
        """
        # проверить на наличие разговора
        self.pushButton_CmdMute.statusLed = not self.pushButton_CmdMute.statusLed
        if self.pushButton_CmdMute.statusLed:
            print u"микрофон отключен"
        else: 
            print u"микрофон включен"


    def dnd(self):
        """
        метод обработчик кнопки не dnd
        выключает режим небеспокоить
        """
        self.pushButton_CmdDND.statusLed = not self.pushButton_CmdDND.statusLed
        if self.pushButton_CmdDND.statusLed:
            print u"включен режим не беспокоить"
        else: 
            print u"выключен режим не беспокоить"


    def conf(self):
        """
        метод обработчик кнопки conf
        организует конференцию 
        """
        print u"конференция"


    def hangup(self):
        """
        метод обработчик нажатия на кнопку hangup
        конец соединения
        """
        print u"конец разговора"


    def record(self):
        """
        метод обработчик кнопки запись разговора
        начинает запись разговора на диск
        """
        # проверить на наличие разговора
        self.pushButton_CmdRecord.statusLed = not self.pushButton_CmdRecord.statusLed
        if self.pushButton_CmdRecord.statusLed:
            print u"началась запись разговора"
        else: 
            print u"закончилась запись разговора"


    def backspace(self):
        """
        метод обработчик нажатия на кнопку backspace
        стирает последний набранный символ номера
        """
        self.number = self.number[:-1]
        self.plainTextEditDisplay.setPlainText(self.number)


    def register(self):
        """
        метод обработчик нажатия на кнопку register
        начинает процесс регистрации sip абонента
        """
        # проверить что еще не зарегистрирован
        # выплняем регистрацию, в случа успеха зажигаем led и меняем надпись на кнопке
        # изменение статуса пораждает событие которое изменит надпись на кнопке
        self.pushButton_CmdRegister.statusLed = not self.pushButton_CmdRegister.statusLed


    def registerStatusChanged(self, value):
        """
        метод обработчик события изменения решистрации
        уведомляет об успешной регистрации/разрегистрации        
        """
        if self.pushButton_CmdRegister.statusLed:
            self.pushButton_CmdRegister.setText("unregister")
        else:
            self.pushButton_CmdRegister.setText("register")

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SIPPhone()
    myapp.show()
    sys.exit(app.exec_())
