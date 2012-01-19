#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 21:14:39 CET
# File:    combined.py


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
        
        #init data
        
        self.objects = [iconButton(self, "scv", 17, 50/17.0)];
        self.objects.append(iconButton(self, "scv", 17, 50/17.0));
        self.objects.append(iconButton(self, "scv", 17, 50/17.0));
        self.objects[0].move( 50,150);
        self.objects[1].move(100, 200);
        self.objects[2].move(150,250);
        
        
        self.reso_list = resource_line(self, -100, 2000);
        self.reso_list2 = resource_line(self, -100, 2000);
        
        for item in self.objects:
            self.reso_list.add_item(item, item.pos().x(), 2/3.0, item.size().width());
            self.reso_list2.add_item(item, item.pos().x(), 2/3.0, item.size().width());
            
        self.objects.append(iconButton(self, "mul", 5, 4));
        self.objects[3].move(5,200);
        self.reso_list.add_item(self.objects[3], self.objects[3].pos().x(), 3);
        self.reso_list.add_item(self.objects[3], self.objects[3].pos().x(), -3, 180);
        
        self.objects.append(iconButton(self, "spm", 25, 50/25.0));
        self.objects.append(iconButton(self, "stimP", 170, 200/170.0));
        self.objects.append(iconButton(self, "spm", 25, 50/25.0));
        self.objects[4].move( 310,250);
        self.objects[5].move(315,150);
        self.objects[6].move(320,50);
        
        #neccessary stuff
        
        x = QCursor(QBitmap("empty.gif"), QBitmap("empty.gif"),0, 0);#nmm
        self.setCursor(x);#nmm
        self.ok_pos = QPoint(0,0);#nmm
        self.setMouseTracking(True);#nmm
        
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
    
    def get_list_from_item(self, item):
        return [it for it in self.objects if it.pos().x() < item.pos().x() or it == item];
        
    def move_selected_to(self, item, pos, rel):#nmm
        old_pos = item.pos();
        new_pos = map_to_grid(pos-rel, 5);
        
        if new_pos.x() <= int(self.reso_list.get_x_from_area(self.get_area_from_list(self.get_list_from_item(item)))/5)*5:
            self.ok_pos = self.mapToGlobal(old_pos + rel);
            QCursor.setPos(self.ok_pos);
        else:
            if new_pos != old_pos:
                self.ok_pos = QCursor.pos();
        
            for it in self.selection:
                loc = new_pos - old_pos + it.pos();
                it.move(loc);
                if it in self.reso_list.items:
                    self.reso_list.move_item_to(it, loc.x());
                if it in self.reso_list2.items:
                    self.reso_list2.move_item_to(it, loc.x());
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
        self.ok_pos = QCursor.pos();#nmm
        self.rubber.change(e);
        self.repaint();#nmm
        
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
            self.reso_list2.paint(self, self.get_area_from_list(self.get_list_from_item(self.selection[0])), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
            self.reso_list.paint(self, self.get_area_from_list(self.get_list_from_item(self.selection[0])));
        else:
            self.reso_list2.paint(self, self.get_total_area(), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
            self.reso_list.paint(self, self.get_total_area());
            
        paintCursor(self, self.mapFromGlobal(self.ok_pos));#nmm
    
    def leaveEvent(self, e):#nmm
        self.ok_pos = QPoint(10000, 10000); #surely not on the screen
        self.repaint();
#=======================================================================================================================
def main():
    app = QApplication(sys.argv);
    #~ app.setStyle("plastique")
    ex = Example();
    ex.show();
    app.exec_();
    
if __name__ == '__main__':
    main();
    
