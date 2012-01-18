#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:51:06 CET
# File:    moveablePushButton.py

import sys
from qt_import import *

class moveablePushButton(QPushButton):
    #needs parent to have:  -move_selected_to(item, pos)
    #                       -selection = selection_manager
    #                       -bool shiftPressed
    
    def __init__(self, title, parent):
        super(moveablePushButton, self).__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton or not self.isChecked():
            return None;
        
        self.parent.move_selected_to(self, e.pos() - QPoint(int(self.size().width()/2), int(self.size().height()/2)));
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            if self.parent.shiftPressed == True:
                self.parent.selection.toggle_item_add(self);
            else:
                self.parent.selection.toggle_item(self);
        if e.button() == Qt.RightButton:
            if not self.parent.selection.is_on(self):
                if self.parent.shiftPressed == True :
                    self.parent.selection.select_item_add(self);
                else:
                    self.parent.selection.select_item(self);
    def mouseReleaseEvent(self, e): #is neccessary bc otherwise Example.mouseReleaseButton is called
        pass;
