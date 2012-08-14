#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""
import sys
from PyQt4 import QtCore, QtGui, uic
import sqlite3
import pickle

class recordbookWindow(QtGui.QDialog):

    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        uic.loadUi("recordbook.ui", self)

        # вешаем обработчики
        self.pushOpenFile.clicked.connect(self.openFile)
        self.pushNew.clicked.connect(self.new)
        self.pushUpdate.clicked.connect(self.update)
        self.pushDelete.clicked.connect(self.delete)
        self.listRecordBook.itemActivated.connect(self.listItemActivated)
        self.listRecordBook.currentItemChanged.connect(self.listItemChanged)


        connection = sqlite3.connect('recordbook.db')
        connection.row_factory = sqlite3.Row
        current = connection.cursor()

        # проверяем наличие уже созданой таблицы, если ее не нашли то создаем
        current.execute("select * from sqlite_master where name='records'")
        accounttable = False
        for i in current:
            accounttable = True
        if not accounttable:
            # создаем таблицу с одним рутовым accountом root, root, все может
            current.execute("create table records(id integer primary key autoincrement, name text, family text, surname text, homephone text, workphone text, mobilephone text, Data BLOB)")
            connection.commit()


        self.fileName = None

        # заполним список записнушки
        current.execute("select * from records")
        records = current.fetchall()

        for record in records:
            listItem = QtGui.QListWidgetItem(self.getNameStr(record))
            listItem.setData(QtCore.Qt.UserRole, long(record["id"]))
            self.listRecordBook.addItem(listItem)

        if connection:
    	    connection.close()

    def getNameStr(self, record):
        return u"{0:} {1:} {2:}".format(record["family"], record["name"], record["surname"])

    def listItemActivated(self, item):
        print "Activated"

    def listItemChanged(self, itemTo, itemFrom):
        #print "Changed", item.data(QtCore.Qt.UserRole).toInt()[0]
        # проверим From что он хороший
        if not itemFrom is None:
            var = itemFrom.data(QtCore.Qt.UserRole).toInt();
            needDelete = True
            if var[1]:
                if var[0] >= 0:
                    needDelete = False
            if needDelete:
                self.listRecordBook.takeItem(self.listRecordBook.row(itemFrom))
            del var

        var = itemTo.data(QtCore.Qt.UserRole).toInt();
        if not var[1]: # хрень с данными
            return

        if var[0] < 0: # это только что созданый элемент
            self.lineName.setText("")
            self.lineFamily.setText("")
            self.lineSurname.setText("")
            self.linePhone.setText("")
            pixmap = QtGui.QPixmap()
            self.labelIMG.setPixmap(pixmap)
            return;

        connection = sqlite3.connect('recordbook.db')
        connection.row_factory = sqlite3.Row
        current = connection.cursor()

        # получаем данные
        current.execute("select * from records where id=:id", {"id": var[0]})
        record = current.fetchone()

        self.lineName.setText(record["name"])
        self.lineFamily.setText(record["family"])
        self.lineSurname.setText(record["surname"])
        self.linePhone.setText(record["homephone"])

        bytearr = QtCore.QByteArray.fromRawData(record["Data"])
        
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(bytearr)
        if not pixmap.isNull():
            pixmap = pixmap.scaled(self.labelIMG.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.labelIMG.setPixmap(pixmap)

        if connection:
    	    connection.close()

        # забываем открытый файл
        self.fileName = None
        
    def openFile(self):
        options = QtGui.QFileDialog.Options()
        fileName = QtGui.QFileDialog.getOpenFileName(self,
                "open photo file",
                "",
                "Image Files (*.png);;All Files (*)", None, options)
        if fileName:
            pixmap = QtGui.QPixmap(fileName)
            if pixmap.isNull():
                QtGui.QMessageBox.information(self, "Recordbook", "Cannot load %s." % fileName)
                return

            pixmap = pixmap.scaled(self.labelIMG.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
            self.labelIMG.setPixmap(pixmap)
            self.fileName = fileName.__str__()

    
    def new(self):
        # как new
        listItem = QtGui.QListWidgetItem("")
        listItem.setData(QtCore.Qt.UserRole, -1)
        self.listRecordBook.addItem(listItem)
        self.listRecordBook.setCurrentItem(listItem)


    def update(self):
        connection = sqlite3.connect('recordbook.db')
        current = connection.cursor()

        item = self.listRecordBook.currentItem()
        var = item.data(QtCore.Qt.UserRole).toInt();
        if not var[1]:
            return;

#        # проверяем созданой записи
#        current.execute("select * from records where homephone=:homephone", {"homephone": self.linePhone.text().__str__()})
#        records = current.fetchall()
#
#        if len(records) != 0:
#            QtGui.QMessageBox.information(self, "Recordbook", "Record exist")
#            return

        binary = None
        if not self.fileName is None:
            try:
                fin = open(self.fileName, "rb")
                binary = sqlite3.Binary(fin.read())
            except IOError, e:
                print "Error %d: %s" % (e.args[0],e.args[1])
            finally:
                if fin:
                    fin.close()

        if var[0] < 0:
            # добавляем запись
            current.execute("insert into records values(NULL, ?, ?, ?, ?, ?, ?, ?)",
                (self.lineName.text().__str__(),
                 self.lineFamily.text().__str__(),
                self.lineSurname.text().__str__(),
                self.linePhone.text().__str__(),
                str("None"),
                str("None"), binary))

            item.setData(QtCore.Qt.UserRole, current.lastrowid)

        else:
            if binary is None:
                current.execute("update records set name=:name, "
                    "family=:family, "
                    "surname=:surname, "
                    "homephone=:homephone, "
                    "workphone=:workphone, "
                    "mobilephone=:mobilephone "
                    "where id=:id",
                    {"name":self.lineName.text().__str__(),
                    "family": self.lineFamily.text().__str__(),
                    "surname": self.lineSurname.text().__str__(),
                    "homephone": self.linePhone.text().__str__(),
                    "workphone": str("None"),
                    "mobilephone": str("None"),
                    "id": var[0]})
            else:
                current.execute("update records set name=:name, "
                    "family=:family, "
                    "surname=:surname, "
                    "homephone=:homephone, "
                    "workphone=:workphone, "
                    "mobilephone=:mobilephone, "
                    "Data=:Data "
                    "where id=:id",
                    {"name":self.lineName.text().__str__(),
                    "family": self.lineFamily.text().__str__(),
                    "surname": self.lineSurname.text().__str__(),
                    "homephone": self.linePhone.text().__str__(),
                    "workphone": str("None"),
                    "mobilephone": str("None"),
                    "Data": binary,
                    "id": var[0]})

        record = {"name": self.lineName.text().__str__(),
                  "family": self.lineFamily.text().__str__(),
                  "surname": self.lineSurname.text().__str__()}
        item.setText(self.getNameStr(record))

        connection.commit()

        if connection:
            connection.close()


    def delete(self):
        item = self.listRecordBook.currentItem()
        var = item.data(QtCore.Qt.UserRole).toInt();
        if not var[1]:
            return;
        if var[0] < 0:
            return;
        connection = sqlite3.connect('recordbook.db')
        connection.row_factory = sqlite3.Row
        current = connection.cursor()

        # получаем данные
        current.execute("delete from records where id=:id", {"id": var[0]})
        connection.commit()

        if connection:
            connection.close()
        self.listRecordBook.takeItem(self.listRecordBook.row(item))

    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    widget = recordbookWindow(None)
    ret = widget.exec_()
    sys.exit(0)


