#!/usr/bin/python
# -*- coding: utf-8 -*-

"""

"""

import sys
from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin
from programmButtonLabel import QProgrammButtonLabel

class programmButtonPluginLabel(QPyDesignerCustomWidgetPlugin):
    """
    programmButtonPlugin(QPyDesignerCustomWidgetPlugin)

    Provides a Python custom plugin for Qt Designer by implementing the
    QDesignerCustomWidgetPlugin via a PyQt-specific custom plugin class.
    """

    def __init__(self, parent=None):
#        QPyDesignerCustomWidgetPlugin.__init__(self, parent)
        super(programmButtonPluginLabel, self).__init__(parent)
        self.initialized = False


    def initialize(self, formEditor):
      if self.initialized:
          return
      self.initialized = True

    def isInitialized(self):
        return self.initialized

    def createWidget(self, parent):
        # метод должен вернуть экземпляр класса нашего виджета
        # вот тут и пригодилось согласование с принятым в Qt4 API
        return QProgrammButtonLabel(parent)

    def name(self):
        # этод метод должен вернуть имя класса виджета
        return "QProgrammButtonLabel"

    def group(self):
        # имя группы виджета
        return "PyQt MTA SIP-Phone"

    def icon(self):
        return QtGui.QIcon(_logo_pixmap)

    def toolTip(self):
        # всплывающая подсказка
        return u"QButtonLabel с цветовым состоянием"

    def whatsThis(self):
        # краткое описание
        return u"Кнопка с цветовым состоянием"

    def isContainer(self):
        # True, если виджет может служить контейнером других виджетов,
        # при этом требуется реализация QDesignerContainerExtension
        # False в противном случае
        return False

    def domXml(self):
        # должен вернуть XML-описание виджета и параметры его свойств.
        # минимально -- класс и имя экземпляра класса
        # вставляется в .ui
        return "<widget class=\"QProgrammButtonLabel\" name=\"programmButtonLabel\">\n"\
               "</widget>\n" \
#               "    <property name=\"green\">\n"\
#               "        <bool>false</bool>\n"\
#               "    </property>\n"\

    def includeFile(self):
        # возвращает имя модуля, в котором хранится наш виджет
        # вставляется как `import <includeFile>` в генеренном из .ui Python-коде
        return "programmButtonLabel"

# Картинка для отображение я Qt-Designer
_logo_32x32_xpm = [
"32 32 122 2",
"  	c None",
". 	c #FFFFFF",
"+ 	c #F83B56",
"@ 	c #F83C56",
"# 	c #F83E59",
"$ 	c #F9465F",
"% 	c #F94E66",
"& 	c #F9566D",
"* 	c #F95E74",
"= 	c #FA667B",
"- 	c #FA6E81",
"; 	c #FA7688",
"> 	c #FA7E8F",
", 	c #FA8596",
"' 	c #FB8D9D",
") 	c #FB96A4",
"! 	c #FB9EAB",
"~ 	c #FCA6B2",
"{ 	c #FCAEB9",
"] 	c #FCB5BF",
"^ 	c #FCBEC6",
"/ 	c #FDC5CE",
"( 	c #FECED4",
"_ 	c #FDD6DB",
": 	c #FEDEE2",
"< 	c #FEE5E9",
"[ 	c #FFEEF0",
"} 	c #FEF6F7",
"| 	c #FFFEFD",
"1 	c #F83E58",
"2 	c #F8465F",
"3 	c #F9667A",
"4 	c #FA6D82",
"5 	c #FA8696",
"6 	c #FB8E9D",
"7 	c #FC9DAB",
"8 	c #FCA5B2",
"9 	c #FCB6C0",
"0 	c #FCBDC6",
"a 	c #FDC6CE",
"b 	c #FDCED5",
"c 	c #FED6DB",
"d 	c #FEEDF0",
"e 	c #FEF5F7",
"f 	c #FFFDFD",
"g 	c #F95D74",
"h 	c #FA6E82",
"i 	c #FA7689",
"j 	c #FA7E90",
"k 	c #FB8696",
"l 	c #FB95A4",
"m 	c #FC9EAB",
"n 	c #FDB6BF",
"o 	c #FDBEC7",
"p 	c #FDCED4",
"q 	c #FEDDE2",
"r 	c #FEEEF0",
"s 	c #FFF5F7",
"t 	c #FFFDFE",
"u 	c #F93D58",
"v 	c #F8455F",
"w 	c #F96E81",
"x 	c #FA7D8F",
"y 	c #FCA5B1",
"z 	c #FCAEB8",
"A 	c #FDB6C0",
"B 	c #FDC6CD",
"C 	c #FDCDD4",
"D 	c #FED5DB",
"E 	c #FFEDF0",
"F 	c #F83B55",
"G 	c #3BF844",
"H 	c #41F345",
"I 	c #EE5F6B",
"J 	c #F9667B",
"K 	c #FA6D81",
"L 	c #F90B2C",
"M 	c #FDBDC7",
"N 	c #FDC5CD",
"O 	c #FECDD4",
"P 	c #FED6DC",
"Q 	c #FDDDE2",
"R 	c #FEE6E9",
"S 	c #FEF6F6",
"T 	c #FEFEFE",
"U 	c #3CF744",
"V 	c #FA5E73",
"W 	c #FA657B",
"X 	c #FCADB8",
"Y 	c #FDBEC6",
"Z 	c #FFFEFE",
"` 	c #FA667A",
" .	c #FDAEB9",
"..	c #FCB5C0",
"+.	c #FCBDC7",
"@.	c #FEF5F6",
"#.	c #FDADB9",
"$.	c #FCBEC7",
"%.	c #FDD5DB",
"&.	c #FFF6F7",
"*.	c #FEEEEF",
"=.	c #41F245",
"-.	c #FFEDEF",
";.	c #FA657A",
">.	c #FDB5BF",
",.	c #FDBDC6",
"'.	c #FDD6DC",
").	c #F95D73",
"!.	c #FB7D90",
"~.	c #FA8597",
"{.	c #FC96A4",
"].	c #F84D66",
"^.	c #F9566C",
"/.	c #FA7588",
"(.	c #FB8697",
"_.	c #FB9DAB",
":.	c #F84E66",
"<.	c #F9657B",
"[.	c #FB7588",
"}.	c #FB8596",
"|.	c #FCADB9",
"1.	c #FEDDE3",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
"+ + + @ # $ % & * = - ; > , ' ) ! ~ { ] ^ / ( _ : < [ } | . . . ",
"+ + @ + 1 2 % & * 3 4 ; > 5 6 ) 7 8 { 9 0 a b c : < d e f . . . ",
"@ + + + 1 $ % & g = h i j k ' l m ~ { n o a p c q < r s t . . . ",
"@ + + + u v % & * = w ; x 5 6 l m y z A ^ B C D q < E } f . . . ",
"@ + F G G G H I * J K ; L L L L m y { A M N O P Q R d S T . . . ",
"+ + G G G G G U V W h L L L L L L ~ X n Y B p _ Q R [ e Z . . . ",
"+ G G G G G G G G ` L L L L L L L L  ...+.a p _ : R r @.f . . . ",
"+ G G G G G G G G = L L L L L L L L #...$.N C %.q R d &.t . . . ",
"+ G G G G G G G G = L L L L L L L L X A o B p D q R *.&.f . . . ",
"+ =.G G G G G G G ` L L L L L L L L X 9 Y a p _ : < -.} t . . . ",
"+ + G G G G G G g ;.K L L L L L L ~ z >.Y N ( c : < r &.| . . . ",
"+ + @ =.G G H & * W h ; L L L L ! ~ z 9 ,.N O '.: R -.&.t . . . ",
"@ @ @ + 1 2 % & ).;.4 ; !.~.' {.! ~ { >.Y a p P : R d s t . . . ",
"@ + @ + 1 2 ].^.g 3 w /.j (.6 l _.~ { n $.B C P : R d s t . . . ",
"@ + + + 1 2 :.^.* <.w [.> }.6 ) m y |...M B p c 1.< d e | . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . ",
". . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . . "]

_logo_pixmap = QtGui.QPixmap(_logo_32x32_xpm)
