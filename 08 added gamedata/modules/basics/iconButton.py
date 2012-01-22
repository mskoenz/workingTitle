#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    18.01.2012 10:09:36 CET
# File:    iconButton.py

from os import path
from ..qt_import import *
from .moveablePushButton import *
from .__style_options import *

class iconButton(moveablePushButton):
    def __init__(self, parent, img, data, mode = "mps"):
        super(iconButton, self).__init__(img, parent);
        self.img_path = path.join("modules", "game_module", "icons", img+".png");
        
        self.data = data;
        self.parent = parent;
        self.setFixedSize(QSize(style_icon_scale_width*self.data["time"], style_icon_scale_height*self.data[mode]));
        self.setToolTip(data["name"]);
        self.mirror = None;
        
    def set_mirror(self, mir):
        self.mirror = mir;
        mir.mirror = self;
    
    def paint(self):
        checked = self.isChecked();
        #choose colorset
        if checked:
            col_bg0 = QColor(style_icon_background_sel[0]);
            col_bg1 = QColor(style_icon_background_sel[1]);
            col_line0 = QColor(style_icon_line_sel[0]);
            col_line1 = QColor(style_icon_line_sel[1]);
        else:
            col_bg0 = QColor(style_icon_background_normal[0]);
            col_bg1 = QColor(style_icon_background_normal[1]);
            col_line0 = QColor(style_icon_line_normal[0]);
            col_line1 = QColor(style_icon_line_normal[1]);
        
        #init painter
        pos = QPoint(0,0);
        size = QPoint(self.size().width(), self.size().height()) - QPoint(2,2); #<- empiric, don't ask
        painter = QPainter();
        painter.begin(self);
        painter.setRenderHints(style_icon_background_render);
        
        #init pen for background
        pen_width = style_pen_width;
        offset = QPoint(int(pen_width/2), int(pen_width/2));
        pen = SPen("black", pen_width);
        pen.setBrush(SGradient(pos, col_line0, pos+size, col_line1))
        
        #paint background
        painter.setPen(pen);
        painter.setBrush(SGradient(pos, col_bg0, pos+size, col_bg1));
        painter.drawRoundedRect(QRect(pos+offset, pos+size-offset), style_rounded_radius, style_rounded_radius);
        
        #scale icon
        img = QPixmap(self.img_path);
        minimum = min(self.size().height(), self.size().width()) - 2*style_icon_pixmap_smaller;
        if style_icon_max_pixmap_size > minimum:
            img = img.scaled(minimum, minimum, transformMode = style_icon_pixmap_trafo);
        
        #paint icon
        img_pos = QPoint(img.size().width(), img.size().height());
        painter.drawPixmap((pos+size+QPoint(2,2)-img_pos)/2, img);
        
        #done :)
        painter.end();

    def paintEvent(self, e):
        self.paint();
        print("painted:",self.data["name"]);
        
        
        
        
        
        
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
            self.objects[-1].setGeometry((i%15)*19, int(i/15)*19, 20, 20);
        
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
            self.printout = copy.deepcopy(self.poly);
            self.poly = self.poly.intersected(self.multi_mark);
            
            correct = []; # store possible target points
            
            for i in self.poly:
                correct.append(i);
            correct.pop(); #bc first = last
            
            #bc of rect properties (see QRect doc) right and bottom line need decrementation
            for i in range(len(correct)):
                if self.poly[i-1].x() <= self.poly[i].x() and self.poly[i+1].y() > self.poly[i].y(): #point ---+
                    correct[i].setX(correct[i].x()-1)                                                #         |
                                                                                                     
                if self.poly[i-1].y() <= self.poly[i].y() and self.poly[i+1].x() < self.poly[i].x(): #         |
                    correct[i].setX(correct[i].x()-1)                                                #point ---+
                    correct[i].setY(correct[i].y()-1)
                                                                                                     #         |
                if self.poly[i-1].x() >= self.poly[i].x() and self.poly[i+1].y() < self.poly[i].y(): #point is +---
                    correct[i].setY(correct[i].y()-1)
                    
            #make unique
            unique = {i:1 for i in correct}.keys();
            
            #find closest target to new_cursor
            target = QPoint(-1000, -1000); #shouldn't be near! #convention
            for p in unique:
                print(p);
                if dist(new_cursor - target) > dist(new_cursor - p):
                    target = p;

            new_cursor = target;
            goto = new_cursor - rel;
            
        if new_cursor != old_cursor:
            self.ok_pos = self.mapToGlobal(new_cursor);
            
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
