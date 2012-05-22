#!/bin/sh
# для наших Custom Widget назначаем путь
export PYQTDESIGNERPATH=$(pwd):${PYQTDESIGNERPATH}
# запускаем Qt-Designer
./designer sip-phone.ui