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
        
        self.objects = [iconButton(self, "scv", 17, 50/17)];
        self.objects.append(iconButton(self, "scv", 17, 50/17));
        self.objects.append(iconButton(self, "scv", 17, 50/17));
        self.objects[0].move( 10,250);
        self.objects[1].move(110,250);
        self.objects[2].move(210,250);
        
        
        self.reso_list = resource_line(self, -100, 2000);
        for item in self.objects:
            self.reso_list.add_item(item, item.pos().x(), 2/3, item.size().width());
            
        self.objects.append(iconButton(self, "mul", 5, 4));
        self.objects[3].move(310,250);
        self.reso_list.add_item(self.objects[3], self.objects[3].pos().x(), 3);
        self.reso_list.add_item(self.objects[3], self.objects[3].pos().x(), -3, 180);
        
        self.objects.append(iconButton(self, "spm", 25, 50/25));
        self.objects.append(iconButton(self, "stimP", 170, 200/170));
        self.objects.append(iconButton(self, "spm", 25, 50/25));
        self.objects[4].move( 10,150);
        self.objects[5].move(110,150);
        self.objects[6].move(310,50);
        
        self.rubber = SRubberBand(self);
        self.selection = selection_manager();
        self.shiftPressed = False;
        
    def get_total_area(self):
        return self.get_area_from_list(self.objects);
    
    def get_area_from_list(self, lis):
        area = 0;
        for it in lis:
            size = it.size();
            area += size.height()*size.width();
        return area;
    
    def get_list_from_x(self, x):
        return [it for it in self.objects if it.pos().x() <= x];
    
    def move_selected_to(self, item, pos):
        for it in self.selection:
            loc = map_to_grid(it.pos()+pos, 1);
            it.move(loc);
            if it in self.reso_list.items:
                self.reso_list.move_item_to(it, loc.x());
        self.repaint();
    
    def keyPressEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = True;
            self.setWindowTitle("shift pressed");
    def keyReleaseEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = False;
            self.setWindowTitle("shift not pressed");
            
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
        self.repaint();
        
    def paintEvent(self, event):
        if self.selection:
            self.reso_list.paint(self, self.get_area_from_list(self.get_list_from_x(self.selection[0].pos().x())));
        else:
            self.reso_list.paint(self, self.get_total_area());
#=======================================================================================================================
def main():
    app = QApplication(sys.argv);
    #~ app.setStyle("plastique")
    ex = Example();
    ex.show();
    app.exec_();
    
if __name__ == '__main__':
    main();
    
