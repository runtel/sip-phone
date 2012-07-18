#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import os, sys
import pickle
from PyQt4 import QtCore, QtGui, uic

from programmButton import QProgrammButton
from programmButtonLabel import QProgrammButtonLabel
from property import propertyWindow
from statusCmdEventFilter import installEventFilter
from sipcall import SIP
import pjsua as pj
#from sipphone_ui import  Ui_sipPhoneWindow

def module_path():
    if hasattr(sys, "frozen"):
        return os.path.dirname(
            unicode(sys.executable, sys.getfilesystemencoding( ))
        )
    return os.path.dirname(unicode(__file__, sys.getfilesystemencoding( )))

class SIPPhone(QtGui.QMainWindow):

    def __init__(self, parent = None):
        QtGui.QWidget.__init__(self, parent)

        uic.loadUi("sipphone.ui", self)
#	self.setupUi(self)
        self.number = ""
        # назначаем обработчики кнопок
        # цифровых
        QtCore.QObject.connect(self.pushButtonDigit1, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("1"))
        QtCore.QObject.connect(self.pushButtonDigit2, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("2"))
        QtCore.QObject.connect(self.pushButtonDigit3, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("3"))
        QtCore.QObject.connect(self.pushButtonDigit4, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("4"))
        QtCore.QObject.connect(self.pushButtonDigit5, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("5"))
        QtCore.QObject.connect(self.pushButtonDigit6, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("6"))
        QtCore.QObject.connect(self.pushButtonDigit7, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("7"))
        QtCore.QObject.connect(self.pushButtonDigit8, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("8"))
        QtCore.QObject.connect(self.pushButtonDigit9, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("9"))
        QtCore.QObject.connect(self.pushButtonDigit0, QtCore.SIGNAL("clicked()"), lambda:self.digit_key_pressed("0"))

        # кнопка #, позвонить
        QtCore.QObject.connect(self.pushButtonDigitGrid, QtCore.SIGNAL("clicked()"), lambda:self.dial())

        # командные кнопки
        QtCore.QObject.connect(self.pushButton_CmdClear, QtCore.SIGNAL("clicked()"), lambda:self.clear())
        QtCore.QObject.connect(self.pushButton_CmdRedial, QtCore.SIGNAL("clicked()"), lambda:self.redial())
        QtCore.QObject.connect(self.pushButton_CmdMute, QtCore.SIGNAL("clicked()"), lambda:self.mute())
        QtCore.QObject.connect(self.pushButton_CmdDND, QtCore.SIGNAL("clicked()"), lambda:self.dnd())
        QtCore.QObject.connect(self.pushButton_CmdConf, QtCore.SIGNAL("clicked()"), lambda:self.conf())
        QtCore.QObject.connect(self.pushButton_CmdHangUp, QtCore.SIGNAL("clicked()"), lambda:self.hangup())
        QtCore.QObject.connect(self.pushButton_CmdRecord, QtCore.SIGNAL("clicked()"), lambda:self.record())
        QtCore.QObject.connect(self.pushButton_CmdBackspace, QtCore.SIGNAL("clicked()"), lambda:self.backspace())
        QtCore.QObject.connect(self.pushButton_CmdDial, QtCore.SIGNAL("clicked()"), lambda:self.dial())
        QtCore.QObject.connect(self.pushButton_CmdRegister, QtCore.SIGNAL("clicked()"), lambda:self.register())
        QtCore.QObject.connect(self.pushButton_CmdAnswer, QtCore.SIGNAL("clicked()"), lambda:self.answer())

        # программируемые кнопки
        # создаем список наших кнопок
        self.programmButtons = self.groupBoxProgrammButton.findChildren(QProgrammButton)
        self.programmButtonsLabel = self.groupBoxProgrammButton.findChildren(QProgrammButtonLabel)

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


        for i in xrange(0, len(self.programmButtonsLabel)):
            if self.programmButtonsLabel[i].numberButton >= 0:
                # обработчик контекстного меню
                self.programmButtonsLabel[i].setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
                QtCore.QObject.connect(self.programmButtonsLabel[i], QtCore.SIGNAL("customContextMenuRequested(QPoint)"), self.programmButtonsLabelContextMenu )
                self.programmButtonsLabel[i].setText("")

        # обработчики событий
        # изменение состояния регистрации
#        QtCore.QObject.connect(self.pushButton_CmdRegister, QtCore.SIGNAL("statusChanged(bool)"), self.registerStatusChanged)

        # инициализаируем конфигурацию
        self.cfgInit()
        self.sip = SIP(self)
        self.init()

        for i in xrange(0, len(self.programmButtonsLabel)):
            if self.programmButtonsLabel[i].numberButton >= 0:
                callName = self.getCallNameProgrammButton(self.programmButtonsLabel[i].numberButton);
                if callName:
                   self.programmButtonsLabel[i].setText(callName)

        QtCore.QObject.connect(self.sip, QtCore.SIGNAL("callout"), self.onCallOutChanged)
        QtCore.QObject.connect(self.sip, QtCore.SIGNAL("callin"), self.onCallInChanged)


    def cfgInit(self):
        """
        метод инициализирует и
        читает конфигурацию из файла
        """
        self.cfg = {}

        # потом загружаем из файла
        try:
            with open('cfg.pick', 'rb') as f:
                self.cfg = pickle.load(f)
        except:
            self.cfg["buttons"] = {}
            self.cfg["name"] = {}
            self.cfg["username"] = ""
            self.cfg["registrator"] = ""


    def init(self):

        self.setWindowTitle("uri: sip:" + self.cfg["username"] + "@" + self.cfg["registrator"])
        self.register(False)

        self.currentCall = None
        self.statusBar.showMessage("Disconnected")

    def saveCfg(self):
        """
        метод записывает всю конфигурацию в файл
        """

        with open('cfg.pick', 'wb') as f:
            pickle.dump(self.cfg, f)

    def programmButtonsLabelContextMenu(self, position):
        """
        метод обработчик сообщения контекстного меню от меток программных кнопок
        """

        # получили отправителя сообщения
        programmButtonLabel = self.sender()

        # создаем QLineEdit для ввода инфы
        editWidget = QtGui.QLineEdit()
        callName = self.getCallNameProgrammButton(programmButtonLabel.numberButton)
        if callName:
            editWidget.setText(callName)

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
            if not self.cfg.has_key("name"):
                self.cfg["name"] = {}
            self.cfg["name"][numberButton] = edit.text().__str__()
            menu.close()
            self.saveCfg()

        # связываем обработчик и сигнал
        QtCore.QObject.connect(editWidget, QtCore.SIGNAL("returnPressed()"), lambda:editOk(menu, editWidget, programmButtonLabel.numberButton))

        # открываем меню
        menu.exec_(programmButtonLabel.mapToGlobal(position))
        programmButtonLabel.setText(editWidget.text().__str__())


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


    def getCallNameProgrammButton(self, numberButton):
        """
        метод возвращает имя связаное с кнопкой
        None если на кнопке ни чего не прописано
        """
        # в словаре есть ключ "buttons"
        if self.cfg.has_key("name"):
            # есть ключ по номеру кнопки
            if self.cfg["name"].has_key(numberButton):
                return self.cfg["name"][numberButton]
        return None
    
    def getCallNumberProgrammButton(self, numberButton):
        """
        метод возвращает значение кнопки
        None если на кнопке ни чего не прописано
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
            elif e.key() == QtCore.Qt.Key_Backspace:    # забой
                self.backspace()
            elif e.key() == QtCore.Qt.Key_Return:   # собственно позвонить
                self.dial()

        return QtGui.QMainWindow.event(self,e)


    def on_menuProperts_triggered(self, checked = None):
        """
        обработчик сообщения от меню "menuProperts"
        """
        # тут создадим окошко с настройками
        widget = propertyWindow(self.cfg)
        if widget.exec_():
            self.cfg["username"] = widget.lineEditUserName.text().__str__()
            self.cfg["password"] = widget.lineEditPassword.text().__str__()
            self.cfg["registrator"] = widget.lineEditRegistrator.text().__str__()
            self.saveCfg()
            self.init()


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

        if self.currentCall is None:
            self.statusBar.showMessage("Disconnected")
        else:
            self.statusBar.showMessage(self.currentCall.info().state_text)


    def dial(self):
        """
        метод инициализируем вызов по SIP
        """
        # тут вписываемся для звонка

        if len(self.number):
            self.plainTextEditDisplay.setPlainText("Dial to :" + self.number)
            if self.sip.account is None:
                self.plainTextEditDisplay.setPlainText("Registartion")
            else:
                self.currentCall = self.sip.make_new_call("sip:" + self.number + "@" + self.cfg["registrator"])
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
        if not (self.currentCall is None):
            self.sip.hangup_calls()
            self.plainTextEditDisplay.setPlainText("Hangup")
            self.number = ""
        self.currentCall = None


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


    def register(self, value = None):
        """
        метод обработчик нажатия на кнопку register
        начинает процесс регистрации sip абонента
        через value передается состояние регистрации необъодимое для установления
        возвращает успешнсть регистрации
        """

        if value is None :
            value = self.pushButton_CmdRegister.statusLed;
        else: value = not value

        if value:
            self.sip.delete_account()
            self.pushButton_CmdRegister.statusLed = False
        else:
            if self.sip.create_account(self.cfg):
                self.pushButton_CmdRegister.statusLed = True
            else:
                self.pushButton_CmdRegister.statusLed = False

        if self.pushButton_CmdRegister.statusLed:
            self.pushButton_CmdRegister.setText("unregister")
        else:
            self.pushButton_CmdRegister.setText("register")


    def answer(self):
        """
        обработчик кнопки ответ абонета
        """
        # проверяем на активность вызова
        if not (self.currentCall is None):
            # проверяем нахождение в предответном
            if (self.currentCall.info().role == pj.CallRole.CALLEE) & (self.currentCall.info().state == pj.CallState.EARLY):
                self.currentCall.answer()

    def onCallInChanged(self, callBack, state):
        """
        обработчик сообщения о поступлении входящего вызова
        """
        self.statusBar.clearMessage()

        if state == pj.CallState.DISCONNECTED:
            # конец соединения
            callBack.sipaccount.calls.remove(callBack.incall)
            callBack.incall = None
            self.statusBar.showMessage("Disconnected")
            self.currentCall = None
            return


        print "Call with", callBack.call.info().remote_uri,
        print "is", callBack.call.info().state_text,
        print "last code =", callBack.call.info().last_code,
        print "(" + callBack.call.info().last_reason + ")"

        # в пре
        if state == pj.CallState.EARLY:
            if callBack.call.info().last_code == 183:
                call_slot = callBack.call.info().conf_slot
                callBack.start_play_file('/ATS/SOUND/music0.wav', call_slot)

        # перешли в разговорное состояние
        if state == pj.CallState.CONFIRMED:
            # завершаем играть то что играли
            call_slot = callBack.call.info().conf_slot
            callBack.stop_play_file(call_slot)

            # проключаем каналы
            pj.Lib.instance().conf_connect(0, call_slot)
            pj.Lib.instance().conf_connect(call_slot, 0)

        if state == pj.CallState.INCOMING:
            self.currentCall = callBack.call
            # отвечаем ringing
            self.currentCall.answer(180)
            # отвечаем call progressом
#            self.currentCall.answer(183)

        self.statusBar.showMessage(callBack.call.info().state_text)

    def onCallOutChanged(self, callBack, state):
        """
        обработчик событий исходящего вызова
        """
        self.statusBar.clearMessage()
        if state == pj.CallState.DISCONNECTED:
            callBack.stop_play_file(0)
            callBack.sipaccount.calls.remove(callBack.outcall)
            callBack.outcall = None
            self.statusBar.showMessage("Disconnected")
            self.currentCall = None
            return

#        print "Call with", callBack.call.info().remote_uri,
#        print "is", callBack.call.info().state_text,
#        print "last code =", callBack.call.info().last_code,
#        print "(" + callBack.call.info().last_reason + ")"

        self.statusBar.showMessage(callBack.call.info().state_text)

        # перешли в разговорное
        if state == pj.CallState.CONFIRMED:
            callBack.stop_play_file(0)

            # проключаем каналы
            call_slot = callBack.call.info().conf_slot
            pj.Lib.instance().conf_connect(0, call_slot)
            pj.Lib.instance().conf_connect(call_slot, 0)

        # проключаем мызыку
        if state == pj.CallState.EARLY:
            callBack.start_play_file('sounds/dialtone.wav', 0)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    myapp = SIPPhone()
    myapp.show()
    return_code = app.exec_()
    myapp.sip.clean()
    sys.exit(return_code)
