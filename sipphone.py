#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import os, sys
import time
import pickle
import re
from PyQt4 import QtCore, QtGui, uic

from programmButton import QProgrammButton
from programmButtonLabel import QProgrammButtonLabel
from property import propertyWindow
from recordbook import recordbookWindow
from infoDocWidget import infoDocWidgeta
from statusCmdEventFilter import installEventFilter
from sipcall import SIP
import pjsua as pj
from callList import callListModel, callDelegate

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
        QtCore.QObject.connect(self.pushButton_CmdTransfer, QtCore.SIGNAL("clicked()"), lambda:self.transfer())

        self.pushButtonTest.clicked.connect(self.clkTest)
        
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

        # запомнили картинку по умолчантю
        self.defPixmap = self.infoFoto.pixmap()

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
        QtCore.QObject.connect(self.sip, QtCore.SIGNAL("transfer_status"), self.onCallTransfer)
        
        # create objects
        self.list_data = [None, None, None, None, None]
        self.lm = callListModel(self.list_data, self)
        #lv = QtGui.QListView()
        de = callDelegate(self.listCall)

        self.listCall.setModel(self.lm)
        self.listCall.setItemDelegate(de)
        
        # обработчик сообщения о выборке объекта из списка
        self.listCall.clicked.connect(self.onListCallClicked)
        self.listCall.doubleClicked.connect(self.onListCallDblClicked)


        #self.setCentralWidget(self.pushButton_CmdTransfer)

        # сздаем doc window
        #dock = QtGui.QDockWidget("Customers", self)
        #uic.loadUi("infoshow.ui", dock)

        #self.addDockWidget(QtCore.Qt.RightDockWidgetArea, dock)
#        self.viewMenu.addAction(self.dockWidget_2.toggleViewAction())
#        self.dockWidget_2.setLayout(self.verticalLayout)

    
    def clkTest(self):
        """
        тестирование по дписки
        """
        if self.sip.account:
            self.sip.add_buddy()

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
            self.cfg["buttons"] = {}      # номера на кнопках
            self.cfg["name"] = {}         # имена на кнопках
            self.cfg["username"] = ""     # имя пользователя
            self.cfg["registrator"] = ""  # где регистрируемся


    def init(self):

        self.setWindowTitle("uri: sip:" + self.getCfgPropertyStr("username") + "@" + self.getCfgPropertyStr("registrator"))
        self.register(False)

        self.setCurrentCall(None)
        self.statusBar.showMessage("Disconnected")

    def setCurrentCall(self, call):
        self.currentCall = call
        number = None
        try:
            if not call is None:
                number = re.findall(':(.*?)@', call.info().remote_uri)[0]
                self.getNumberInfo(number)
        except LookupError:
            pass
        self.getNumberInfo(number)


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


    def getCfgPropertyStr(self, propertyName):
        """
        метод возвращает значение св-ва из конфигурации
        пустую строку если на кнопке ни чего не прописано
        """
        if self.cfg.has_key(propertyName):
            return self.cfg[propertyName];
        return ""


    def getCallNameProgrammButton(self, numberButton):
        """
        метод возвращает имя связаное с кнопкой
        None если на кнопке ни чего не прописано
        """
        return self.getProgrammButtonValue(numberButton, "name")


    def getCallNumberProgrammButton(self, numberButton):
        """
        метод возвращает значение кнопки
        None если на кнопке ни чего не прописано
        """
        return self.getProgrammButtonValue(numberButton, "buttons")


    def getProgrammButtonValue(self, numberButton, keyName):
        """
        метод возвращает значение связаное с ключем keyName
        None если на кнопке ни чего не прописано
        """

        # в словаре есть ключ "name"
        if self.cfg.has_key(keyName):
            # есть ключ по номеру кнопки
            if self.cfg[keyName].has_key(numberButton):
                return self.cfg[keyName][numberButton]
        return None


    def event(self, e):
        """
        обработчик сообщений от клавиатуры
        """
        if e.type() == QtCore.QEvent.KeyPress:
            # проверяем на нажатие 0-9, добавляем к нашей строке
            if e.key() in xrange(QtCore.Qt.Key_0, QtCore.Qt.Key_9):
                self.number = self.number + '%c' % e.key()
                self.lineEditDisplay.setText(self.number)
            elif e.key() == QtCore.Qt.Key_Backspace:    # забой
                self.backspace()
            elif e.key() == QtCore.Qt.Key_Return:   # собственно позвонить
                self.dial()

        return QtGui.QMainWindow.event(self,e)


    def on_actionProperts_triggered(self, checked = None):
        """
        обработчик сообщения от меню "menuProperts"
        """
        if checked is None: return

        # тут создадим окошко с настройками
        widget = propertyWindow(self.cfg, self.sip.lib.enum_snd_dev())
        if widget.exec_():
            self.cfg["username"] = widget.lineEditUserName.text().__str__()
            self.cfg["password"] = widget.lineEditPassword.text().__str__()
            self.cfg["registrator"] = widget.lineEditRegistrator.text().__str__()
            self.cfg["record"] = widget.comboRecordDevices.currentText().__str__()
            self.cfg["playback"] = widget.comboPlaybackDevices.currentText().__str__()
            self.saveCfg()
            self.init()

    def on_actionRecordBook_triggered(self, checked = None):
        """
        обработчик сообщения от меню "menuRecordBook"
        """
        # тут создадим окошко для работы с записнухой        
        if checked is None: return

        widget = recordbookWindow(None)
        widget.exec_()


    def on_actionShow_Info_triggered(self, checked = None):
        """
        обработчик сообщения от меню "showInfo"
        """
        if checked is None: return
        self.groupInfo.setVisible(checked)


    def digit_key_pressed(self, par1):
        """
        обработчик сообщений от цифровых кнопок
        """
        self.number = self.number + par1
        self.lineEditDisplay.setText(self.number)


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


    def onListCallClicked(self, index):
        """
        обработчик сообщения о выборке из списка вызов
        """
        #for i in self.listCall.selectedIndexes():
        #    print i.row()
        pass

    def onListCallDblClicked(self, index):
        """
        обработчик сообщения о двойном нажатии клавиши
        """        
        for i in self.listCall.selectedIndexes():
            call = self.lm.data(i,  QtCore.Qt.DisplayRole).toPyObject()
            if call is None:
                continue
                
            if call == self.currentCall:
                continue

            if self.pushButton_CmdTransfer.isChecked():
                self.currentCall.transfer_to_call(call)
                return


            # текущий вызов должен быть в разговорном
            if not self.currentCall is None:
                if self.currentCall.info().state == pj.CallState.CONFIRMED:
                    self.currentCall.hold()

            if call.info().state == pj.CallState.CONFIRMED:
                call.unhold()

            self.setCurrentCall(call)
            return


    def getFreeCallID(self):
        """
        выдает свободный call индекс
        """
        for i, item in enumerate(self.list_data):
            if item is None:
                return i
        return None

    def connectCall(self, callid, call):
        """
        добавляет вызов call в список под индексом callid
        """
       
        index = self.lm.index(callid)
        self.lm.setData(index, call, QtCore.Qt.EditRole)

        
    def freeCall(self, call):
        """
        удаляет вызов call из списка зызовов
        """
        for i, item in enumerate(self.list_data):
            if call == item:
                index = self.lm.index(i)
                self.lm.setData(index, None, QtCore.Qt.EditRole)
    

    def dial(self):
        """
        метод инициализируем вызов по SIP
        """
        # тут вписываемся для звонка

        if len(self.number):
            self.lineEditDisplay.setText("Dial to :" + self.number)
            if self.sip.account is None:
                self.lineEditDisplay.setText("Registration")
            else:
                if len(self.cfg["registrator"]):
                    callid = self.getFreeCallID()
                    if not callid is None:
                        # если есть текущий вызов ставим его на удержание
                        if not self.currentCall is None:
                            # если он не в разговорном то на hold ставить его нельзя
                            if self.currentCall.info().state == pj.CallState.CONFIRMED:
                                self.currentCall.hold()
                                # включен режим перевода вызова
                                if self.pushButton_CmdTransfer.isChecked():
                                    self.currentCall.transfer(str("sip:" + self.number + "@" + self.cfg["registrator"]))
                                    self.setCurrentCall(None)
                                    return
                            else: # поставим когда ответит
                                pass

                        call = self.sip.make_new_call("sip:" + self.number + "@" + self.cfg["registrator"])
#                        if self.pushButton_CmdTransfer.isChecked():
#                            self.currentCall.transfer_to_call(call)
#                            self.currentCall = None
#                            return

                        self.connectCall(callid, call)
                        # нужно выделить currenCall в списке
                        index = self.lm.index(callid)
                        self.listCall.setCurrentIndex(index)

                        self.setCurrentCall(call)
#                        self.getNumberInfo(self.number)

                    else:
                        self.lineEditDisplay.setText("Free line is absent")
                else:
                    self.lineEditDisplay.setText("Need registrator")
        else:
            self.lineEditDisplay.setText("Need number")


    def clear(self):
        """
        метод обработчик кнопки clear
        очищает набранный номер
        """
        self.number = ""
        self.lineEditDisplay.setText(self.number)


    def redial(self):
        """
        метод обработчик кнопки redial
        перезванивает по последнему номеру
        """
        # тут вписываемся для перезвона
        self.lineEditDisplay.setText("Redial to :" + self.number)


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
        # снимаем всех с holdа
        for i in self.listCall.selectedIndexes():
            callOne = self.lm.data(i,  QtCore.Qt.DisplayRole).toPyObject()
            if callOne != self.currentCall:
                if callOne.info().state == pj.CallState.CONFIRMED:
                    callOne.unhold()

        # нужно для выпонения unhildа для всех callов на удержании
        time.sleep(1)

        # коммутируем всех друг на друга
        # только тех кто уже в разговоре
        for i in self.listCall.selectedIndexes():
            callOne = self.lm.data(i,  QtCore.Qt.DisplayRole).toPyObject()

            if callOne.info().state != pj.CallState.CONFIRMED:
                continue

            call_slot = callOne.info().conf_slot

            for j in self.listCall.selectedIndexes():
                callTwo = self.lm.data(j,  QtCore.Qt.DisplayRole).toPyObject()

                # самого на себя не коммутиуем
                if callTwo == callOne:
                    continue

                if callTwo.info().state != pj.CallState.CONFIRMED:
                    continue

                # проключаем каналы
                pj.Lib.instance().conf_connect(callTwo.info().conf_slot, call_slot)
                
                #pj.Lib.instance().conf_connect(call_slot, callTwo.info().conf_slot)


        #self.listCall.setCurrentIndex(None)


    def hangup(self):
        """
        метод обработчик нажатия на кнопку hangup
        конец соединения
        """
        #отбиваем выделеные вызовы

        for i in self.listCall.selectedIndexes():
            call = self.lm.data(i,  QtCore.Qt.DisplayRole).toPyObject()
            if call == self.currentCall:
                self.lineEditDisplay.setText("Hangup")
                self.number = ""

            if not call is None:
                call.hangup()


#        if not self.currentCall is None:
#            # отбиваем текущий вызов
#            
#
#            self.currentCall.hangup()
#            self.lineEditDisplay.setText("Hangup")
#            self.number = ""
#            #self.currentCall = None


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
        self.lineEditDisplay.setText(self.number)


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
            if len(self.cfg["registrator"]):
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
        # выделен только одна линий
        sel_len =  len(self.listCall.selectedIndexes())
        if sel_len != 1:
            return

        # по выбраному индексу получаем вызов
        indexes = self.listCall.selectedIndexes()
        call = self.lm.data(indexes[0],  QtCore.Qt.DisplayRole).toPyObject()

        # среди выделеного нет вызова
        if call is None:
            return

        # есть ли текущий активный вызов, ставим его на удержание
        if not self.currentCall is None:
            # повторый ансвер на текущем вызове
            #print self.currentCall, call
            if self.currentCall == call:
                if (self.currentCall.info().role == pj.CallRole.CALLEE) & (self.currentCall.info().state == pj.CallState.EARLY):
                    self.currentCall.answer()
                return
            # выбран другой вызов ставим на холд текущий
            self.currentCall.hold()

        # переключаемся на текущий вызов
        self.setCurrentCall(call)
        # проверяем нахождение в предответном
        if (self.currentCall.info().role == pj.CallRole.CALLEE) & (self.currentCall.info().state == pj.CallState.EARLY):
            self.currentCall.answer()
        else:
            self.currentCall.unhold()

    def transfer(self):
        """
        обработчик кнопки перевод абонета
        переводит текущий вызов на выбраный
        """
        # выделен должен быть только один вызов
#        sel_len =  len(self.listCall.selectedIndexes())
#        if sel_len != 1:
#            return
        
        if self.currentCall is None:
            self.sender().setChecked(False)
            return

        # текущий вызов не в разговоре
        if self.currentCall.info().state != pj.CallState.CONFIRMED:
            self.sender().setChecked(False)
            return

#        indexes = self.listCall.selectedIndexes()
#        call = self.lm.data(indexes[0],  QtCore.Qt.DisplayRole).toPyObject()

#        self.currentCall.transfer_to_call(call)

        self.sender().setChecked(self.sender().isChecked())        
        #self.currentCall.hangup()


    def onCallInChanged(self, callBack, state):
        """
        обработчик сообщения о поступлении входящего вызова
        """
        self.statusBar.clearMessage()

        if state == pj.CallState.DISCONNECTED:
            # конец соединения
            self.freeCall(callBack.call)
            if self.currentCall == callBack.call:
                self.setCurrentCall(None)
                self.pushButton_CmdTransfer.setChecked(False)
            callBack.sipaccount.calls.remove(callBack.incall)
            callBack.incall = None
            self.statusBar.showMessage("Disconnected")
            return


#        print "Call with", callBack.call.info().remote_uri,
#        print "is", callBack.call.info().state_text,
#        print "last code =", callBack.call.info().last_code,
#        print "(" + callBack.call.info().last_reason + ")"

        # в предответном играем музыку
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
            # отображаем окно со звонком
            self.show()
            self.activateWindow()

            callid = self.getFreeCallID()
            if not callid is None:
                self.connectCall(callid, callBack.call)
            else:
                callBack.call.answer(486)
                return

#            self.currentCall = callBack.call
            if self.pushButton_CmdDND.statusLed:
                callBack.call.answer(486)
                return
            # отвечаем ringing
            callBack.call.answer(180)
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
            self.freeCall(callBack.outcall)
            if self.currentCall == callBack.outcall:
                self.setCurrentCall(None)
                self.pushButton_CmdTransfer.setChecked(False)
            callBack.outcall = None
            self.statusBar.showMessage("Disconnected")
            
            return

        print "Call with", callBack.call.info().remote_uri,
        print "is", callBack.call.info().state_text,
        print "last code =", callBack.call.info().last_code,
        print "(" + callBack.call.info().last_reason + ")"

        self.statusBar.showMessage(callBack.call.info().state_text)

        # перешли в разговорное
        if state == pj.CallState.CONFIRMED:
            callBack.stop_play_file(0)

            # проключаем каналы
            call_slot = callBack.call.info().conf_slot
            pj.Lib.instance().conf_connect(0, call_slot)
            pj.Lib.instance().conf_connect(call_slot, 0)

            # это вызов уже не активный сразу ставим его на удержание
            if self.currentCall != callBack.outcall:
                callBack.outcall.hold()

        # проключаем мызыку
        if state == pj.CallState.EARLY:
            callBack.start_play_file('sounds/dialtone.wav', 0)


    def onCallTransfer(self, callBack, code, reason):
        print "CallTransfer message", code, reason
        # все хорошо перевелось вызов освобождаю
        if (reason == "OK") & (code == 200):
            self.pushButton_CmdTransfer.setChecked(False)
            callBack.call.hangup()
            return 

        if code == 486:
            self.pushButton_CmdTransfer.setChecked(False)
            self.lineEditDisplay.setText("Transfer user busy")
            #callBack.call.hangup()
            callBack.call.unhold()
            return 
            # для возможности возврата назад с удержания


    def getNumberInfo(self, number):
        """
        отображает информацию о звонящем абоненте
        """       
        info = recordbookWindow.getInfoByNumber(number)
        if info is None:
            self.infoFoto.setPixmap(QtGui.QPixmap("ico/1345104250_metacontact_offline.png"))
            return

        if not info["img"].isNull():
            pixmap = info["img"].scaled(self.infoFoto.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.infoFoto.setPixmap(pixmap)

if __name__ == "__main__":
    # в среде win стандартные кнопки настолько плохо смотряться что будем использовать другую тему
    if sys.platform == "win32":
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create("Plastique"))
    app = QtGui.QApplication(sys.argv)
    myapp = SIPPhone()
    myapp.show()
    return_code = app.exec_()
    myapp.sip.clean()
    sys.exit(return_code)
