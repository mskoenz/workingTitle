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
class moveablePushButton(QPushButton):
    #needs parent to have:  -move_selected_to(item, pos)
    #                       -selection = selection_manager
    #                       -bool shiftPressed
    
    def __init__(self, title, parent):
        super(moveablePushButton, self).__init__(parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        #for nice mouse (nmm)
        self.last_click = QPoint(0,0);
        self.setMouseTracking(True);
        
    def mouseMoveEvent(self, e):
        self.parent.repaint();#nmm
        if e.buttons() != Qt.RightButton or not self.isChecked():
            self.parent.ok_pos = QCursor.pos();
            return None;
        
        self.parent.move_selected_to(self, self.mapToParent(e.pos()), self.last_click);#nmm
        
    def mousePressEvent(self, e):
        self.last_click = e.pos();#nmm
        
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
        self.parent.repaint();
    
    def paintEvent(self, e):#nmm
        paintCursor(self, self.mapFromGlobal(self.parent.ok_pos));
        
    def mouseReleaseEvent(self, e): #is neccessary bc otherwise Example.mouseReleaseButton is called
        pass;
        
def paintCursor(self, pos):#nmm must be a free function
    painter = QPainter();
    painter.begin(self);
    painter.drawPixmap(pos, QPixmap(path.join("modules", "basics", "cursors", style_paint_cursor_img)));
    painter.end();
