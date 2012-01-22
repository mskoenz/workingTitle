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

from os import path

#=======================================================================================================================
def map_to_grid(point, grid_size):
    x = int(point.x()/grid_size)*grid_size;
    y = int(point.y()/grid_size)*grid_size;
    return QPoint(x, y);

#=======================================================================================================================
class base_widget(QWidget):
    
    def __init__(self, parent):
        self.parent = parent;
        super(base_widget, self).__init__();
        self.setAcceptDrops(True);

        pal = QPalette();
        pal.setColor(QPalette.Background, QColor("black"));
        self.setPalette(pal);
        
        self.min_objects = [];
        self.gas_objects = [];
        
        self.master_arch = {};
        for it in import_list:
            self.master_arch[it] = 0;
        
        
        self.reso_line = resource_line(self, -100, 2000);
        self.reso_line.add_item("init", -3, 750)
        self.reso_line.add_item("init", -3, -750, 1)
        self.gas_line =  resource_line(self, -100, 2000);
        
        #neccessary stuff
        img_path = path.join("modules", "basics", "cursors", "empty.gif");
        
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
        
        if sc2[name]["gps"] != 0:
            self.gas_objects.append(iconButton(self, name, sc2[name], "gps"));
            item2 = self.gas_objects[-1]
            item2.move(dx, dy + style_icon_scale_height*6);
            item2.set_mirror(item);
            
        
        
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
    def move_selected_to(self, item, pos, rel):#nmm
        old_pos = item.pos();
        new_pos = map_to_grid(pos-rel, style_grid_size);
        
        #~ if 0:
        if new_pos.x() < round(self.reso_line.get_x_from_area(self.get_area_from_item(item, "min"))/style_grid_size)*style_grid_size:
            self.ok_pos = self.mapToGlobal(old_pos + rel);
            QCursor.setPos(self.ok_pos);
        else:
            if new_pos != old_pos:
                self.ok_pos = QCursor.pos();
        
            for it in self.selection:
                loc = new_pos - old_pos + it.pos();
                it.move(loc);
                if it in self.reso_line.items:
                    self.reso_line.move_item_to(it, loc.x());
                if it in self.gas_line.items:
                    self.gas_line.move_item_to(it, loc.x());
        #~ self.repaint();
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
        self.rubber.change(e);
        
    def mouseReleaseEvent(self, e):
        sel = self.rubber.get_selection(self.min_objects, e);
        if self.shiftPressed and not self.rubber.empty():
            self.selection.select_list_add(sel);
        if not self.shiftPressed:
            self.selection.select_list(sel);
        
        self.repaint();
        self.rubber.set_to_zero();
    
    #paint events
    def paintEvent(self, event):
        if self.selection:
            #~ self.gas_line.paint(self, self.get_area_from_item(self.selection[0], "gas"), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
            self.reso_line.paint(self, self.get_area_from_item(self.selection[0], "min"));
            print("painter: main if");
        else:
            #~ self.gas_line.paint(self, self.get_total_area("gas"), area_color = ["lime", "yellow"], trafo = [0,402,1,1]);
            self.reso_line.paint(self, self.get_total_area("min"));
            print("painter: main else");
