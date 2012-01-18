#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    18.01.2012 10:04:28 CET
# File:    with_icons.py

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
        self.setGeometry(100, 100, 700, 500);
        self.setAcceptDrops(True);
        pal = QPalette();
        pal.setColor(QPalette.Background, QColor("black"));
        self.setPalette(pal);
        
        self.objects = [iconButton(self, "scv", 40, 50)];
        self.objects.append(iconButton(self, "scv", 40, 50));
        self.objects.append(iconButton(self, "scv", 40, 50));
        self.objects.append(iconButton(self, "mul", 40, 200));
        self.objects[0].move( 10,250);
        self.objects[1].move(110,250);
        self.objects[2].move(210,250);
        self.objects[3].move(310,250);
        
        
        self.reso_list = resource_line(self, -100, 2000);
        for item in self.objects:
            self.reso_list.add_item(item, item.pos().x()+item.size().width(), item.size().height());
        
        self.objects.append(iconButton(self, "spm", 80, 50));
        self.objects.append(iconButton(self, "tho", 150, 100));
        self.objects.append(iconButton(self, "cru", 200, 150));
        self.objects[4].move( 10,150);
        self.objects[5].move(110,150);
        self.objects[6].move(310,50);
        
        self.rubber = SRubberBand(self);
        self.selection = selection_manager();
        self.shiftPressed = False;
        
    def get_area(self):
        area = 0;
        for it in self.objects:
            size = it.size();
            area += size.height()*size.width();
        return area;
        
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
            loc = map_to_grid(it.pos()+pos, 10);
            loc2 = map_to_grid(it.pos()+pos+QPoint(it.size().width(), 0), 10);
            it.move(loc);
            if it in self.reso_list.items:
                self.reso_list.move_item_to(it, loc2.x());
        self.repaint();
            
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
        
    def paintEvent(self, event):
        self.reso_list.paint(self, self.get_area());
    
#=======================================================================================================================
def main():
    app = QApplication(sys.argv);
    #~ app.setStyle("plastique")
    ex = Example();
    ex.show();
    app.exec_();
    
if __name__ == '__main__':
    main();
