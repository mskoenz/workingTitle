#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 21:48:17 CET
# File:    condition_drag.py


import sys
from qt_import import *
import copy;

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        #~ self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum);
        self.last_click = QPoint(0,0);
        self.setMouseTracking(True);
    def mouseMoveEvent(self, e):
        self.parent.repaint();
        
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
            self.parent.restrict = QPolygon();
            for it in [x for x in [self.parent.button1, self.parent.button2, self.parent.button3] if x not in self.parent.selection]:
                size = QPoint(it.rect().width(), it.rect().height());
                rect = QRect(it.pos(), it.pos()+size - QPoint(2,2));
                self.parent.restrict = self.parent.restrict.united(rect);
    def paintEvent(self, e):
        QPushButton.paintEvent(self, e);
        paintCursor(self, self.mapFromGlobal(self.parent.ok_pos));
        
def map_to_grid(point, grid_size): #doesn't work in negatives!!
    x = int(point.x()/grid_size)*grid_size;
    y = int(point.y()/grid_size)*grid_size;
    return QPoint(x, y);

class Example(QWidget):
  
    def __init__(self):
        QWidget.__init__(self);
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        x = QCursor(QBitmap("empty.gif"), 0, 0);
        print(x.hotSpot());
        self.setCursor(x);
        
        
        self.button1 = Button('1', self);
        self.button2 = Button('2', self);
        self.button3 = Button('3', self);
        self.button1.setGeometry(10,20,20,20);
        self.button2.setGeometry(100,50,60,60);
        self.button3.setGeometry(160,150,20,20);
        
        
        
        self.r1 = QPolygon(QRect(20, 20, 240, 240));
        self.r2 = QPolygon(QRect(10, 10, 100, 100));
        self.restrict = self.r1.united(self.r2).subtracted(self.button1.rect());
        self.mark = QPolygon();
        self.setMouseTracking(True);
        
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
    
    #~ def outside(self, pos, size):
        #~ tl = pos;
        #~ bl = tl + QPoint(0, size.height());
        #~ tr = tl + QPoint(size.width(), 0);
        #~ br = tr + QPoint(0, size.height());
        #~ print(tl,bl,tr,br);
        #~ if not self.restrict.containsPoint(tl, Qt.OddEvenFill) or\
           #~ not self.restrict.containsPoint(bl, Qt.OddEvenFill) or\
           #~ not self.restrict.containsPoint(tr, Qt.OddEvenFill) or\
           #~ not self.restrict.containsPoint(br, Qt.OddEvenFill):
            #~ return True;
        #~ return False;
    
    def move_selected_to(self, item, pos, rel):
        
        p = item.pos();

        pos = pos-rel;
        self.mark = QPolygon();
        for it in self.selection:
            size = QPoint(it.rect().size().width(), it.rect().size().height());
            rect = QRect(pos-p+it.pos(), pos-p+it.pos()+size-QPoint(2,2));
            self.mark = self.mark.united(QPolygon(rect));
            print(len(self.restrict.intersected(self.mark)));
        if len(self.restrict.intersected(self.mark)) > 3:
            pos = p;
            self.ok_pos = self.mapToGlobal(pos + rel);
            QCursor.setPos(self.ok_pos);
        else:
            if pos != p:
                self.ok_pos = QCursor.pos();
        for it in self.selection:
            rel = p -it.pos();
            it.move(pos - rel);
        self.repaint();
            
    def mouseMoveEvent(self, e):
        self.ok_pos = QCursor.pos();
        self.repaint();
    
    def mousePressEvent(self, e):
        self.deselect_all();

    def paintEvent(self, e):
        painter = QPainter();
        painter.begin(self);
        painter.drawPolygon(self.restrict);
        #~ painter.drawPolygon(self.mark);
        painter.drawPolygon(self.restrict.intersected(self.mark));
        painter.end();
        paintCursor(self, self.mapFromGlobal(self.ok_pos));
        
    def leaveEvent(self, e):
        self.ok_pos = QPoint(10000, 10000); #surely not on the screen
        self.repaint();
        
def paintCursor(self, pos):
    painter = QPainter();
    painter.begin(self);
    painter.drawPixmap(pos, QPixmap("cursor_green.png"));
    painter.end();
    
def main():
    app = QApplication(sys.argv);
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
