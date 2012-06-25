#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
    EventFilter 

"""

import sys
from PyQt4 import QtCore, QtGui

def installEventFilter(widget):

    class statusCmdEventFilter(QtCore.QObject):

	mouseleave = QtCore.pyqtSignal(int)
	mouseenter = QtCore.pyqtSignal(int)
	
	def eventFilter(self, obj, event):

	    if widget == obj:
    		# событие мышь покинула кнопку
    		if event.type() == QtCore.QEvent.Leave:
		    self.mouseleave.emit(widget.numberButton)
        	    return True
        	    
        	# событие мышь навелась на кнопку
        	if event.type() == QtCore.QEvent.Enter:
		    self.mouseenter.emit(widget.numberButton)
        	    return True

	    return False
	    
    enentfilter = statusCmdEventFilter(widget)
    widget.installEventFilter(enentfilter)
    return enentfilter
