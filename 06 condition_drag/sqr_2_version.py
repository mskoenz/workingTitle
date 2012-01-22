#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 21:58:54 CET
# File:    sqr_2_version.py


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
        #~ self.setMouseTracking(True);
        
    def mouseMoveEvent(self, e):
        #~ self.parent.repaint();
        
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
            self.parent.restrict = [];
            for it in [x for x in self.parent.objects if x not in self.parent.selection]:
                size = QPoint(it.rect().width(), it.rect().height());
                rect = QRect(it.pos(), it.pos()+size - QPoint(2,2));
                self.parent.restrict.append(rect);
    def paintEvent(self, e):
        QPushButton.paintEvent(self, e);
        print("repaint", self.text());
        paintCursor(self, self.mapFromGlobal(self.parent.ok_pos));
        
#~ def map_to_grid(point, grid_size): #doesn't work in negatives!!
    #~ x = int(point.x()/grid_size)*grid_size;
    #~ y = int(point.y()/grid_size)*grid_size;
    #~ return QPoint(x, y);

class Example(QWidget):
  
    def __init__(self):
        QWidget.__init__(self);
        self.setWindowTitle("Click or Move");
        self.setGeometry(300, 300, 300, 300);
        self.setAcceptDrops(True);
        
        #~ x = QCursor(QBitmap("empty.gif"), 0, 0);
        #~ print(x.hotSpot());
        #~ self.setCursor(x);
        
        
        self.objects = [];
        
        for i in range(70):
            self.objects.append(Button(str(i), self));
            self.objects[-1].setGeometry((i%20)*20, i*10 - int(i/20)*100, 20, 20);
        
        
        self.restrict = []
        self.mark = [];
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
        
        p = item.pos();

        pos = pos-rel;
        self.mark = [];
        for it in self.selection:
            size = QPoint(it.rect().size().width(), it.rect().size().height());
            rect = QRect(pos-p+it.pos(), pos-p+it.pos()+size-QPoint(2,2));
            self.mark.append(rect);
            #check n**m
            check = True;
            for move in self.mark:
                for block in self.restrict:
                    if block.intersects(move):
                        check = False;
                #for spec in spezliste[move]: <-- dict
                    #if spez.intersects(move):
                        #check = False;

                        print(block.size() == move.size())
                        break;
        if not check:
        #~ if False:
            pos = p;
            self.ok_pos = self.mapToGlobal(pos + rel);
            QCursor.setPos(self.ok_pos);
        else:
            if pos != p:
                self.ok_pos = QCursor.pos();
        for it in self.selection:
            rel = p -it.pos();
            it.move(pos - rel);
        #~ self.repaint();
            
    def mouseMoveEvent(self, e):
        self.ok_pos = QCursor.pos();
        #~ self.repaint();
    
    def mousePressEvent(self, e):
        self.deselect_all();

    def paintEvent(self, e):
        painter = QPainter();
        painter.begin(self);
        print("repainted main");
        #~ for rec in self.restrict:
            #~ painter.drawRect(rec);
        #~ painter.drawPolygon(self.mark);
        #~ painter.drawPolygon(self.restrict.intersected(self.mark));
        painter.end();
        paintCursor(self, self.mapFromGlobal(self.ok_pos));
        
    def leaveEvent(self, e):
        self.ok_pos = QPoint(10000, 10000); #surely not on the screen
        #~ self.repaint();
        
def paintCursor(self, pos):
    pass;
    #~ painter = QPainter();
    #~ painter.begin(self);
    #~ painter.drawPixmap(pos, QPixmap("cursor_green.png"));
    #~ painter.end();
    
def main():
    app = QApplication(sys.argv);
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
