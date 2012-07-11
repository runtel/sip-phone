#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
Создание отдельно запускаемого проекта через py2exe
"""


from distutils.core import setup
import glob
import py2exe


datafiles = [
    ("ico",glob.glob("ico/*")),
    (".", ["property.ui", "sipphone.ui"])
]

setup(
    windows=[{"script":"sipphone.py"}],
    url='https://github.com/umkasuper/sip-phone',
    data_files = datafiles,
#    options={"py2exe": {"includes":["sip", "PyQt4", "pjsua", "statusCmdButton", "programmButton"], "bundle_files": 1,"compressed": 1}}
    options={"py2exe": {"includes":["sip", "PyQt4", "pjsua", "statusCmdButton", "programmButton"]}}
)