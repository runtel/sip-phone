#!/bin/sh
# для наших Custom Widget назначаем путь
export PYQTDESIGNERPATH=$(pwd):${PYQTDESIGNERPATH}
./designer ./sipphone.ui 
