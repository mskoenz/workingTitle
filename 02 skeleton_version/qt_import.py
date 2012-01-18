#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    16.01.2012 17:36:09 CET
# File:    qt_import.py

try:
    from PySide.QtCore import *
    from PySide.QtGui import *
    print("PySide loaded")
except ImportError:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        print("PyQt4 loaded")
    except ImportError:
        print("Error: no PySide or PyQt4 Module")

