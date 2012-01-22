#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 08:58:18 CET
# File:    base_widget.py

from .qt_import import *

from .basics import *
from .game_module import *
from .basics.__style_options import *
from .basics.utilities import *

from os import path

#=======================================================================================================================
class base_widget(QWidget):
    
    def __init__(self, parent):
        self.parent = parent;
        super(base_widget, self).__init__();
        self.setAcceptDrops(True);

        #game logic stuff
        
        self.min_objects = [];
        self.gas_objects = [];
        
        self.master_arch = {};
        for it in import_list:
            self.master_arch[it] = 0;
        
        self.reso_line = resource_line(self, -100, 2000);
        self.reso_line.add_item("init", -3, 750)
        self.reso_line.add_item("init", -3, -750, 1)
        self.gas_line =  resource_line(self, -100, 2000);
        
        
        #style stuff
        pal = QPalette();
        pal.setColor(QPalette.Background, QColor("black"));
        self.setPalette(pal);
        
        self.setMouseTracking(True);
        cur = QCursor(path.join("modules","basics","cursors",style_paint_cursor_img), 0, 0);
        self.setCursor(cur);
        
        #neccessary stuff
        self.multi_mark = QPolygon();
        self.printout = QPolygon();
        self.ok_pos = QPoint(0,0);
        
        self.rubber = SRubberBand(self);
        self.selection = selection_manager();
        self.shiftPressed = False;

    #insert functions
    def add_item(self, name, dx, dy): #normal build min_objects
        self.master_arch[name] += 1;
        dx *= style_icon_scale_width;
        dy *= style_icon_scale_height;
        
        self.min_objects.append(iconButton(self, name, sc2[name]));
        item = self.min_objects[-1]
        item.move(dx, dy);
        
        #~ if sc2[name]["gps"] != 0:
            #~ self.gas_objects.append(iconButton(self, name, sc2[name], "gps"));
            #~ item2 = self.gas_objects[-1]
            #~ item2.move(dx, dy + style_icon_scale_height*6);
            
        
        
        if name == "scv":
            self.reso_line.add_item(item, dx, 2/3.0, item.data["time"]);
        if name == "mule":
            self.gas_line.add_item(item, dx, 2/3.0);
            #~ self.gas_line.add_item(item, dx, -2/3.0, item.data["time"]);
        
    #~ def add_item(self, name, pos):#for convenience
        #~ self.add_item(name, pos.x(), pos.y());
    
    #area functions
    def get_total_area(self, mode):
        return eval("self.get_area_from_list(self."+mode+"_objects, '"+mode+"')");
        #~ return self.get_area_from_list(self.min_objects2, "gas");
    
    def get_area_from_list(self, lis, mode):
        area = 0;
        for it in lis:
            area += it.data[mode]*style_icon_scale_height*style_icon_scale_width;
        return area;
    
    def get_list_from_item(self, item, mode):
        return [it for it in eval("self."+mode+"_objects") if it.pos().x() < item.pos().x() or it == item];
    
    def get_area_from_item(self, item, mode):
        return self.get_area_from_list(self.get_list_from_item(item, mode), mode);
    
    #move selected
    def move_selected_to(self, item, new_cursor, rel):
        
        old = item.pos();
        goto = new_cursor - rel;
        old_cursor = old + rel;
        
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
            #~ self.printout = copy.deepcopy(self.poly); #perhaps for later
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
                
                if it in self.reso_line.items:
                    self.reso_line.move_item_to(it, (goto-rel).x());
                if it in self.gas_line.items:
                    self.gas_line.move_item_to(it, (goto-rel).x());
                    
        #~ self.repaint(); #only for style
        
    #key events
    def keyPressEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = True;
    def keyReleaseEvent(self, e):
        if e.isAutoRepeat() == False and e.key() == Qt.Key_Shift:
            self.shiftPressed = False;
    
    #mouse events
    def mousePressEvent(self, e):
        self.rubber.start(e);
        
    def mouseMoveEvent(self, e):
        self.ok_pos = QCursor.pos();
        self.rubber.change(e);
        
    def mouseReleaseEvent(self, e):
        self.repaint();
        sel = self.rubber.get_selection(self.min_objects, e);
        if self.shiftPressed and not self.rubber.empty():
            self.selection.select_list_add(sel);
        if not self.shiftPressed:
            self.selection.select_list(sel);
        
        self.rubber.set_to_zero();
    
    #paint events
    def paintEvent(self, event):
        #~ if self.selection:
            #~ self.gas_line.paint(self, self.get_area_from_item(self.selection[0], "gas"), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
            #~ self.reso_line.paint(self, self.get_area_from_item(self.selection[0], "min"));
            #~ print("painter: main if");
        #~ else:
        self.gas_line.paint(self, self.get_total_area("gas"), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
        self.reso_line.paint(self, self.get_total_area("min"));
            #~ print("painter: main else");
