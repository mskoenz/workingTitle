#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 10:53:33 CET
# File:    rubber_band_select.py

import sys
from qt_import import *

#=======================================================================================================================
class Button(QPushButton):
  
    def __init__(self, title, parent):
        super().__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton or not self.isChecked():
            return None;
        
        self.parent.move_selected_to(self, e.pos() - QPoint(int(self.size().width()/2), int(self.size().height()/2)));
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            #~ print(">click start");
            if self.parent.shiftPressed == True:
                self.parent.selection.toggle_item_add(self);
            else:
                self.parent.selection.toggle_item(self);
            #~ print(">click end");
        if e.button() == Qt.RightButton:
            if not self.parent.selection.is_on(self):
                if self.parent.shiftPressed == True :
                    self.parent.selection.select_item_add(self);
                else:
                    self.parent.selection.select_item(self);
    def mouseReleaseEvent(self, e): #is neccessary bc otherwise Example.mouseReleaseButton is called
        pass;
#=======================================================================================================================
def map_to_grid(point, grid_size):
    x = int(point.x()/grid_size)*grid_size;
    y = int(point.y()/grid_size)*grid_size;
    return QPoint(x, y);
    
#=======================================================================================================================
class SRubberBand(QRubberBand):
    def __init__(self, parent = None):
        super().__init__(QRubberBand.Rectangle, parent);
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
#=======================================================================================================================
class selection_manager(list):
    def __init__(self):
        self = [];
    
    def is_on(self, item):
        if item in self:
            return True;
        return False;
    
    def select_item_add(self, item):
        if item not in self:
            item.setChecked(True);
            self.append(item);
    
    def select_item(self, item):
        self.deselect_all();
        self.select_item_add(item);
        
    def deselect_item_add(self, item):
        if item in self:
            item.setChecked(False);
            self.remove(item);
        
    def toggle_item_add(self, item):
        if item not in self:
            self.select_item_add(item);
        else:
            self.deselect_item_add(item);
            
    def toggle_item(self, item):
        if item in self:
            self.deselect_all();
        else:
            self.deselect_all();
            self.select_item_add(item);

    def select_list_add(self, items):
        for item in items:
            self.select_item_add(item);
    
    def deselect_all(self):
        while self:
            self.deselect_item_add(self[0]);
            
    def select_list(self, items):
        self.deselect_all();
        self.select_list_add(items);
        
            
#=======================================================================================================================
class Example(QWidget):
    def __init__(self):
        super(Example, self).__init__();
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        self.objects = [Button('1', self)];
        self.objects.append(Button('2', self));
        self.objects.append(Button('3', self));
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
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
