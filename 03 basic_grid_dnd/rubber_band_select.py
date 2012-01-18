#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 10:53:33 CET
# File:    rubber_band_select.py

import sys
from qt_import import *
from modules import *
#=======================================================================================================================
def map_to_grid(point, grid_size):
    x = int(point.x()/grid_size)*grid_size;
    y = int(point.y()/grid_size)*grid_size;
    return QPoint(x, y);
    
#=======================================================================================================================
class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__();
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        self.objects = [moveablePushButton('1', self)];
        self.objects.append(moveablePushButton('2', self));
        self.objects.append(moveablePushButton('3', self));
        self.objects[0].setGeometry(10,20,20,20);
        self.objects[1].setGeometry(100,20,60,60);
        self.objects[2].setGeometry(150,20,20,20);
        
        self.rubber = SRubberBand(self);
        self.selection = selection_manager();
        self.shiftPressed = False;
        
    def keyPressEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = True;
            self.setWindowTitle("shift pressed");
    def keyReleaseEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = False;
            self.setWindowTitle("shift not pressed");
    
    def move_selected_to(self, item, pos):
        self.selection.happend = True;
        for it in self.selection:
            it.move(map_to_grid(it.pos() + pos, 10));
            
    def mousePressEvent(self, e):
        self.rubber.start(e);
        
    def mouseMoveEvent(self, e):
        self.rubber.change(e);
        
    def mouseReleaseEvent(self, e):
        sel = self.rubber.get_selection(self.objects, e);
        if self.shiftPressed and not self.rubber.empty():
            self.selection.select_list_add(sel);
        if not self.shiftPressed:
            self.selection.select_list(sel);
        
        self.rubber.set_to_zero();

#=======================================================================================================================
def main():
    app = QApplication(sys.argv);
    #~ app.setStyle("macintosh")
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
