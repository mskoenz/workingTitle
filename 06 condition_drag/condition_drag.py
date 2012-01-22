#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 21:48:17 CET
# File:    condition_drag.py


import sys
from qt_import import *
import copy;
import math;

def QPointS(size):
    return QPoint(size.width(), size.height());

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        self.last_click = QPoint(0,0);
        self.setMouseTracking(True);
        
        self.lock = False;
        
    def mouseMoveEvent(self, e):
        if self.lock:
            return None;
        if e.buttons() != Qt.RightButton or not self.isChecked():
            self.parent.ok_pos = QCursor.pos();
            return None;
            
        self.parent.move_selected_to(self, self.mapToParent(e.pos()), self.last_click);
        
    def mousePressEvent(self, e):
        self.last_click = e.pos();
        
        if e.button() == Qt.LeftButton:
            self.parent.select_item(self);
            print("click");
        if e.buttons() == Qt.RightButton and not self.isChecked():
            self.parent.deselect_all();
            self.parent.select_item(self);
        if e.buttons() == Qt.RightButton and self.isChecked():
            
            self.parent.multi_mark = [];
            for mark in self.parent.selection:
                for re in [x for x in self.parent.objects if x not in self.parent.selection]:
                    rel_p = re.pos() + e.pos() + self.pos() - mark.pos();
                    tar = QRect(rel_p - QPointS(mark.size())+QPoint(1,1), rel_p + QPointS(re.size())-QPoint(2,2));
                    self.parent.multi_mark.append(tar);
                    
    def paintEvent(self, e):
        QPushButton.paintEvent(self, e);
        
class Example(QWidget):

    def __init__(self):
        QWidget.__init__(self);
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        self.objects = [];
        
        for i in range(70):
            self.objects.append(Button(str(i), self));
            self.objects[-1].setGeometry((i%15)*19, int(i/15)*19, 20, 20);
        
        self.multi_mark = [];
        
        #~ self.setMouseTracking(True);
        
        self.selection = [];
        self.ok_pos = QPoint(0,0);
        self.keydown = False;

    def keyPressEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.keydown = True;
            self.setWindowTitle("shift pressed");
    
    def keyReleaseEvent(self, e):
        if  e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.keydown = False;
            self.setWindowTitle("shift not pressed");
    
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
        
    def move_selected_to(self, item, pos, rel):
        old = item.pos();
        goto = pos - rel;
        
        dif = QPoint(0, 0);
        
        fixed_cursor = pos;
        
        for re in self.multi_mark:
            if re.contains(fixed_cursor):
                p1 = re.topLeft()-fixed_cursor;
                p2 = re.bottomRight()-fixed_cursor + QPoint(1,1);
                dx = p1.x() if -p1.x() < p2.x() else p2.x();
                dy = p1.y() if -p1.y() < p2.y() else p2.y();
                if abs(dx) < abs(dy):
                    if abs(dx) > abs(dif.x()):
                        dif.setX(dx);
                elif abs(dx) > abs(dy):
                    if abs(dy) > abs(dif.y()):
                        dif.setY(dy);
                #~ else:
                    #~ if abs(dx) > abs(dif.x()):
                        #~ dif.setX(dx);
                    #~ if abs(dy) > abs(dif.y()):
                        #~ dif.setY(dy);

        if dif != QPoint(0,0):
            goto += dif;
            self.ok_pos = self.mapToGlobal(goto + rel);
            
            item.lock = True;
            QCursor.setPos(self.ok_pos);
            item.lock = False;
            for it in self.selection:
                rel = old -it.pos();
                it.move(goto - rel);
        else:
            self.ok_pos = QCursor.pos();
            for it in self.selection:
                rel = old -it.pos();
                it.move(goto - rel);
        self.repaint();
    
    def mouseMoveEvent(self, e):
        self.ok_pos = QCursor.pos();

    def mousePressEvent(self, e):
        self.deselect_all();

    def paintEvent(self, e):
        
        pass;
        painter = QPainter();
        painter.begin(self);
        
        for rec in self.multi_mark:
            painter.drawRect(rec);
        
        painter.end();
        
def main():
    app = QApplication(sys.argv);
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
