#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""
import sys
from PyQt4 import QtCore, QtGui, uic


class propertyWindow(QtGui.QDialog):

    def __init__(self, cfg, listSndDevices, parent = None):
        """
        на входе конфигурация в виде словаря со значениями
        """
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi("property.ui", self)
        self.connect(self.buttonBox, QtCore.SIGNAL("accepted()"), self.accept)
        self.connect(self.buttonBox, QtCore.SIGNAL("rejected()"), self.reject)
        # настраиваем validator для ввода ip адреса
        regExp = QtCore.QRegExp("((1{0,1}[0-9]{0,2}|2[0-4]{1,1}[0-9]{1,1}|25[0-5]{1,1})\\.){3,3}(1{0,1}[0-9]{0,2}|2[0-4]{1,1}[0-9]{1,1}|25[0-5]{1,1})")
        validator = QtGui.QRegExpValidator(regExp, self)
        self.lineEditRegistrator.setValidator(validator)

        if cfg.has_key("username"):
            self.lineEditUserName.setText(cfg["username"])
        if cfg.has_key("password"):
            self.lineEditPassword.setText(cfg["password"])
        if cfg.has_key("registrator"):
            self.lineEditRegistrator.setText(cfg["registrator"])

        for dev in listSndDevices:
            if dev.output_channels:
                self.comboRecordDevices.addItem(dev.name)
            if dev.input_channels:
                self.comboPlaybackDevices.addItem(dev.name)

#        if cfg.has_key("recording"):

#        if cfg.has_key("playback"):

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = propertyWindow({}) # пустой словарь в качестве конфиги
    ret = widget.exec_()
    print ret
    sys.exit(0)

