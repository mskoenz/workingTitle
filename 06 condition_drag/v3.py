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

def dist(point):
    return math.sqrt(pow(point.x(), 2)+pow(point.y(), 2));

def split_polygon(poly):
    split = [];
    temp = [];
    start = [];
    i = 0;
    
    while i < len(poly):
        if poly[i] in start:
            i+=1;
            continue;
        temp = [poly[i]];
        start.append(poly[i]);
        i += 1;
        while poly[i] not in start:
            temp.append(poly[i]);
            i += 1;
        temp.append(poly[i]);
        split.append(temp);
    
    return split;
    
    

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super(Button, self).__init__(title, parent);
        self.parent = parent;
        self.setCheckable(True);
        self.setFocusPolicy(Qt.NoFocus);
        self.last_click = QPoint(0,0);
        self.setMouseTracking(True);
        
    def mouseMoveEvent(self, e):
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
            
            self.parent.multi_mark = QPolygon(self.parent.rect());
            for mark in self.parent.selection:
                for re in [x for x in self.parent.objects if x not in self.parent.selection]:
                    rel_p = re.pos() + e.pos() + self.pos() - mark.pos();
                    tar = QRect(rel_p - QPointS(mark.size())+QPoint(2,2), rel_p + QPointS(re.size())-QPoint(2,2));
                    self.parent.multi_mark = self.parent.multi_mark.subtracted(QPolygon(tar));
                    
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
            self.objects[-1].setGeometry((i%10)*25, int(i/10)*25, 20, 20);
        
        self.multi_mark = QPolygon();
        self.printout = QPolygon();
        
        #~ self.setMouseTracking(True);
        #~ cur = QCursor("cursor_green.png", 0, 0);
        #~ self.setCursor(cur);
        
        self.count = 0;
        self.selection = [];
        self.ok_pos = QPoint(0,0);
        self.keydown = False;
        self.poly = QPolygon();
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
    
        
    
    def move_selected_to(self, item, new_cursor, rel):
        
        old = item.pos();
        goto = new_cursor - rel;
        old_cursor = old + rel;
        self.count += 1;
        
        if not self.multi_mark.containsPoint(new_cursor, Qt.OddEvenFill):
            #get the direction for right ordering
            top_l_x = old_cursor.x();
            top_l_y = old_cursor.y();
            bottom_r_x = new_cursor.x();
            bottom_r_y = new_cursor.y();
            
            if old_cursor.y() >= new_cursor.y():
                top_l_y, bottom_r_y = bottom_r_y, top_l_y;
                
            if old_cursor.x() >= new_cursor.x():
                top_l_x, bottom_r_x = bottom_r_x, top_l_x;
            
            #create selection polygon
            self.poly = QPolygon(QRect(QPoint(top_l_x, top_l_y), QPoint(bottom_r_x, bottom_r_y)));
            #intersect with the outside
            self.printout = copy.deepcopy(self.poly); #perhaps for later
            self.poly = self.poly.intersected(self.multi_mark);
            
            #the intersection can have mutliple isolated areas, witch are split here (returns list of closed point-list)
            split = split_polygon(self.poly); 
            
            
            correct = []
            
            # read all possible point in correct (s[:-1] bc start = endpoint)
            for s in split:
                for i in s[:-1]:
                    correct.append(i);
            
            #bc of rect properties (see QRect doc) right and bottom line need decrementation
            # the = in <=, >= are neccesary bc start = enp-point
            k = 0;
            for sp in split:
                for i in range(len(sp)-1):
                    if sp[i-1].x() <= sp[i].x() and sp[i+1].y() > sp[i].y():  #point is ---+
                        correct[k+i].setX(correct[k+i].x()-1)                 #            |
                        
                    if sp[i-1].y() <= sp[i].y() and sp[i+1].x() < sp[i].x():  #point is    | 
                        correct[k+i].setX(correct[k+i].x()-1)                 #         ---+
                        correct[k+i].setY(correct[k+i].y()-1)
                                                                              #            |
                    if sp[i-1].x() >= sp[i].x() and sp[i+1].y() < sp[i].y():  #point is    +---
                        correct[k+i].setY(correct[k+i].y()-1)
                k += (len(sp)-1);

            #make unique
            unique = [];
            for it in correct:
                if it not in unique:
                    unique.append(it);
            
            #find closest point to new_cursor
            target = QPoint(-1000, -1000); #shouldn't be near #convention
            for p in unique:
                if dist(new_cursor - target) > dist(new_cursor - p):
                    target = p;

            new_cursor = target;
            goto = new_cursor - rel; #correct destination

        if new_cursor != old_cursor: 
            self.ok_pos = self.mapToGlobal(new_cursor);

            #move everything
            for it in self.selection:
                rel = old -it.pos();
                it.move(goto - rel);

        self.repaint(); #only for style
    
    def mouseMoveEvent(self, e):
        self.ok_pos = QCursor.pos();

    def mousePressEvent(self, e):
        self.deselect_all();

    def paintEvent(self, e):
        
        pass;
        painter = QPainter();
        painter.begin(self);
        
        painter.drawPolygon(self.multi_mark);
        painter.drawPolygon(self.printout);
        
        painter.end();
        
def main():
    app = QApplication(sys.argv);
    ex = Example();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
