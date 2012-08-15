#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Модель для отображения списка вызовов
"""

import sys
from PyQt4 import QtCore, QtGui, uic


class callDelegate(QtGui.QItemDelegate):
    def __init__(self, parent=None, *args):
        QtGui.QItemDelegate.__init__(self, parent, *args)

    def sizeHint(self, option, index):
        if option.state & QtGui.QStyle.State_Enabled:
#    	    editor = self.createEditor(None, option, index)
#	    self.editor.setGeometry(option.rect)
            return QtCore.QSize(10, 20)
        else:
            print index.data()
    	    return index.data().sizeHint()

    def paint(self, painter, option, index):
        painter.save()
        # set background color
        painter.setPen(QtGui.QPen(QtCore.Qt.NoPen))
        if option.state & QtGui.QStyle.State_Selected:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.red))
        else:
            painter.setBrush(QtGui.QBrush(QtCore.Qt.white))
#	     painter.setBrush(option.foreground())
        painter.drawRect(option.rect)

        # set text color
        painter.setPen(QtGui.QPen(QtCore.Qt.black))
        value = index.data(QtCore.Qt.DisplayRole)
        text = u" Линия №" + str(index.row() + 1) + "-"
        if value.isValid():
#            text += value.toString()
#        print "Call with", callBack.call.info().remote_uri,
#        print "is", callBack.call.info().state_text,
#        print "last code =", callBack.call.info().last_code,
#        print "(" + callBack.call.info().last_reason + ")"
            call = value.toPyObject()
            text += call.info().remote_uri
        else:
            text += "idle"
        painter.drawText(option.rect, QtCore.Qt.AlignLeft, text)
        painter.restore()
#	self.editor.setGeometry(option.rect)
#        print option.rect
#	self.editor.render(painter, QPoint(0, option.rect.y()))


class callListModel(QtCore.QAbstractListModel):
    def __init__(self, datain, parent=None, *args):
        """ datain: a list where each item is a row
        """
        QtCore.QAbstractListModel.__init__(self, parent, *args)
        self.listdata = datain

    def rowCount(self, parent = QtCore.QModelIndex()):
        return len(self.listdata)

    def data(self, index, role):
        if index.isValid() and role == QtCore.Qt.DisplayRole:
            return QtCore.QVariant(self.listdata[index.row()])
        else:
            return QtCore.QVariant()

    def setData(self, index, value, role = QtCore.Qt.EditRole):
        if role == QtCore.Qt.EditRole:
            row = index.row()
            self.listdata[row] = value
#            index = self.index(callid)
#            self.dataChanged.emit(index, index)
            self.dataChanged.emit(index, index)
            return True

class listWindow(QtGui.QWidget):
    def __init__(self, *args):
        QtGui.QWidget.__init__(self, *args)

        # create objects
        list_data = [1, 2, 3, 5, 7]
        lm = callListModel(list_data, self)        
        lv = QtGui.QListView()
        de = callDelegate(lv)

        lv.setModel(lm)
        lv.setItemDelegate(de)
        list_data[0] = 10

        # layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(lv)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    w = listWindow()
    w.show()
    sys.exit(app.exec_())


