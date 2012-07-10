
#!/usr/bin/python
#coding=utf8

"""
Создание отдельно запускаемого проекта через py2exe
"""


from distutils.core import setup
import py2exe

setup(
    windows=[{"script":"sipphone.py"}],
    options={"py2exe": {"includes":["sip", "PyQt4", "pjsua"]}}
)