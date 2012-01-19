#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    18.01.2012 13:57:12 CET
# File:    painter_helper.py

from .qt_import import *

class SPen(QPen):
    def __init__(self, color = "Black", width = 2):
        super(SPen, self).__init__(QColor(color));
        self.setJoinStyle(Qt.RoundJoin);
        self.setCapStyle(Qt.RoundCap);
        self.setWidth(width);

class SGradient(QLinearGradient):
    def __init__(self, p1, col1, p2, col2):
        super(SGradient, self).__init__(p1.x(), p1.y(), p2.x(), p2.y()); #so complicated bc of PyQt4
        self.setSpread(QGradient.PadSpread);
        self.setColorAt(0, QColor(col1));
        self.setColorAt(1, QColor(col2));

class SBrush(QBrush):
    def __init__(self, color):
        super(SBrush, self).__init__(QColor(color));
        grad = SGradient(QPoint(0,0), "red", QPoint(0,0), "orange");
