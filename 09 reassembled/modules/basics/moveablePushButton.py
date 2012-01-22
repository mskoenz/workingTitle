#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:51:06 CET
# File:    moveablePushButton.py

import sys
from os import path

from ..qt_import import *
from .__style_options import *
from .utilities import *

class moveablePushButton(QPushButton):
    #needs parent to have:  -move_selected_to(item, pos)
    #                       -selection = selection_manager
    #                       -bool shiftPressed
    
    def __init__(self, title, parent):
        super(moveablePushButton, self).__init__(parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        self.last_click = QPoint(0,0);
        
    def mouseMoveEvent(self, e):
        if e.buttons() != style_icon_drag_button or not self.isChecked():
            self.parent.ok_pos = QCursor.pos();
            return None;
            
        self.parent.move_selected_to(self, self.mapToParent(e.pos()), self.last_click);
        
    def mousePressEvent(self, e):
        self.last_click = e.pos();#nmm
        
        if e.button() == style_icon_toggle_button:
            if self.parent.shiftPressed == True:
                self.parent.selection.toggle_item_add(self);
            else:
                self.parent.selection.toggle_item(self);
                
        if e.button() == style_icon_drag_button:
            if not self.parent.selection.is_on(self):
                if self.parent.shiftPressed == True :
                    self.parent.selection.select_item_add(self);
                else:
                    self.parent.selection.select_item(self);
        
        if e.buttons() == style_icon_drag_button and self.isChecked():
            
            self.parent.multi_mark = QPolygon(self.parent.rect());
            for mark in self.parent.selection:
                for re in [x for x in self.parent.min_objects if x not in self.parent.selection]:
                    rel_p = re.pos() + e.pos() + self.pos() - mark.pos();
                    tar = QRect(rel_p - QPointS(mark.size())+QPoint(1,1), rel_p + QPointS(re.size())-QPoint(1,1));
                    self.parent.multi_mark = self.parent.multi_mark.subtracted(QPolygon(tar));
    
    def mouseReleaseEvent(self, e): #is neccessary bc otherwise some_parent.mouseReleaseEvent is called
        self.parent.repaint();
        pass;
        
