#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 09:10:49 CET
# File:    move.py

import sys
from qt_import import *

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super().__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);

    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton or not self.isChecked():
            return None;
        self.parent.move_selected_to(self, e.pos()+self.pos()-QPoint(int(self.size().width()/2), int(self.size().height()/2)));
        
    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.parent.select_item(self);
            print("click");
        if e.buttons() == Qt.RightButton and not self.isChecked():
            self.parent.deselect_all();


class Example(QWidget):
  
    def __init__(self):
        super(Example, self).__init__();
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        self.button1 = Button('1', self);
        self.button2 = Button('2', self);
        self.button3 = Button('3', self);
        self.button1.setGeometry(10,20,20,20);
        self.button2.setGeometry(100,20,20,20);
        self.button3.setGeometry(150,20,20,20);
        
        self.selection = [];
                
        self.keydown = False;

    def keyPressEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.keydown = True;
            self.setWindowTitle("Click");
            print("OK");
    def keyReleaseEvent(self, e):
        if  e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.keydown = False;
            self.setWindowTitle("Click or Move");
            print("NOK");
    
    def select_item(self, item):
        if self.keydown == True:
            if item.isChecked == True:
                self.selection.remove(item);
                item.setChecked(False);
            else:
                self.selection.append(item);
                item.setChecked(True);
        else:
            self.deselect_all();
            self.selection.append(item);
            item.setChecked(True);
    def deselect_all(self):
        for it in self.selection:
            it.setChecked(False);
            self.selection = [];
    def move_selected_to(self, item, pos):
        dif = item.pos() - pos;
        print(dif);
        for it in self.selection:
            it.move(it.pos()-dif);
            
    def mousePressEvent(self, e):
        self.deselect_all();
        
def main():
    app = QApplication(sys.argv);
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
