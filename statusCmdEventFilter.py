#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    EventFilter 

"""

import sys
from PyQt4 import QtCore, QtGui

def installEventFilter(widget):

    class statusCmdEventFilter(QtCore.QObject):

	rightclicked = QtCore.pyqtSignal(int)
	mouseleave = QtCore.pyqtSignal(int)
	clicked = QtCore.pyqtSignal(int)
	
	def eventFilter(self, obj, event):

	    if widget == obj:

    		# событие мыш покинула кнопку
    		if event.type() == QtCore.QEvent.Leave:
		    self.mouseleave.emit(widget.numberButton)
        	    return True

                # событие нажали кнопку мышки
		if event.type() == QtCore.QEvent.MouseButtonRelease:
                    # левая кнопка мышки нажата
		    if event.button() & QtCore.Qt.LeftButton:
        		self.clicked.emit(widget.numberButton)
		        return True

                    # правая кнопка мышки нажата
		    if event.button() & QtCore.Qt.RightButton:
        		self.rightclicked.emit(widget.numberButton)
  		        return True

  		    return False

	    return False
	    
    enentfilter = statusCmdEventFilter(widget)
    widget.installEventFilter(enentfilter)
    return enentfilter