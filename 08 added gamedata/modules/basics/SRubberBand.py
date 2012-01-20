#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:36:26 CET
# File:    SRubberBand.py

import sys
from ..qt_import import *

class SRubberBand(QRubberBand):
    def __init__(self, parent = None):
        super(SRubberBand, self).__init__(QRubberBand.Rectangle, parent);
        self.origin = QPoint(0, 0);
    
    def start(self, e):
        self.origin = e.pos();
        self.setGeometry(QRect(self.origin, QSize()));
        self.show();
    
    def change(self, e):
        self.setGeometry(QRect(self.origin, e.pos()).normalized());
    
    def get_selection(self, obj, e):
        self.hide();
        intersect_list = [];
        area = self.geometry();
        for it in obj:
            if area.intersects(it.geometry()):
                intersect_list.append(it);
        return intersect_list;
    
    def empty(self):
        if self.size() == QSize(0, 0):
            return True;
        return False;
    def set_to_zero(self):
        self.setGeometry(QRect(0, 0, 0, 0));
