#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:47:16 CET
# File:    resource_line.py
#
#class resource_line:
#   __init__(start, end);
#   offset(vec, offset_x, offset_y);
#   scale(vec, scale_x, scale_y);
#   add_item(item, x_pos, heigth);
#   get_points(of_x = 0, of_y = 0, sc_x = 1, sc_y = 1);
#   move_item_to(item, x);
#   move_item_by(item, dx);
#   __str__();
#   paint(parent, color, area);
#   get_area_to(x);
#   fet_x_from_area(area);
import copy
import math
from qt_import import *

def sign(arg):
    return int(math.copysign(1, arg));

def addX(point, dx):
    point.setX(point.x()+dx);

def addY(point, dy):
    point.setY(point.y()+dy);

class resource_line:
    def __init__(self, start, end):
        #invariant: always sorted in x-direction
        self.points = [QPoint(start,0), QPoint(start,0), QPoint(end, 0)];
        self.items = ["start"];
    
    def offset(self, vec, x_offset, y_offset):
        for p in vec:
            p += QPoint(x_offset, y_offset);
    
    def scale(self, vec, x_scale, y_scale):
        for p in vec:
            p.setX(p.x()*x_scale);
            p.setY(p.y()*y_scale);
    
    def add_item(self, item, x_pos, heigth):
        i = 0;
        while(self.points[i].x() < x_pos):
            i+=1;
            
        ground = self.points[i-1].y();
        self.points.insert(i, QPoint(x_pos, ground));
        self.points.insert(i, QPoint(x_pos, ground));
        self.items.insert(int(i/2), item);
        
        for p in self.points[i+1:]:
            p.setY(p.y()+heigth);
    
    #transformation only occurs if the points need to be known
    def get_points(self, of_x = 0, of_y = 0, sc_x = 1, sc_y = 1): #Todo: optimize
        res = copy.deepcopy(self.points);
        self.offset(res, of_x, of_y);
        self.scale(res, sc_x, sc_y);
        return res;
    
    def move_item_to(self, item, x):
        k = self.items.index(item);
        self.move_item_by(item, x-self.points[2*k].x());
    
    def move_item_by(self, item, dx):
        k = self.items.index(item);
        
        p = self.points;
        it = self.items;

        addX(p[2*k], dx);
        addX(p[2*k+1], dx);
        
        if dx > 0:  #two ifs bc more efficient than generic version
            i = k + 1;
            while p[2*k].x() > p[2*i].x():
                tmp1 = p[2*k].x();  #cretate temporaries (deep!)
                tmp2 = p[2*k+1].x();
                
                dif_k = p[2*k+1].y()-p[2*k].y();    #compute difference in heigth
                dif_i = p[2*i+1].y()-p[2*i].y();
                
                t_dif = dif_i -dif_k;   #difference between the heights
                                                                    #     start-configuration     => end-conf
                p[2*k].setX(p[2*i].x());                            #            pos xi |       pos xi |      | new k
                p[2*k+1].setX(p[2*i+1].x());                        #                   v              v      v
                                                                    #          p(2*i+1) +-------  =>          +----
                p[2*i].setX(tmp1);                                  #           dif_i-> |         =>          |
                p[2*i+1].setX(tmp2);                                #   p(2*k+1) +------+ p(2*i)  =>          |
                                                                    #        /-> | <--+ t_dif     =>          |
                addY(p[2*i], t_dif);                                # dif_k +--> | <-/            =>   +------+
                addY(p[2*k+1], t_dif);                              #        \-> |                =>   |
                                                                    #------------+ p(2*k)         =>---+
                it[k], it[i] = it[i], it[k];
                i+=1;
                k+=1;
                
        if dx < 0:  #second if
            i = k - 1;
            while p[2*k].x() < p[2*i].x():
                tmp1 = p[2*k].x();
                tmp2 = p[2*k+1].x();
                
                dif_k = p[2*k+1].y()-p[2*k].y();
                dif_i = p[2*i+1].y()-p[2*i].y();
                
                t_dif = dif_k - dif_i;
                
                p[2*k].setX(p[2*i].x());
                p[2*k+1].setX(p[2*i+1].x());
                
                p[2*i].setX(tmp1);
                p[2*i+1].setX(tmp2);
                
                addY(p[2*k], t_dif);
                addY(p[2*i+1], t_dif);
                
                it[k], it[i] = it[i], it[k];
                i-=1;
                k-=1;
    
    def paint(self, parent, color, area):
        painter = QPainter();
        painter.begin(parent);
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing);
        pen = QPen(QColor(color)); #color doesn't matter
        pen.setJoinStyle(Qt.RoundJoin);
        pen.setCapStyle(Qt.RoundCap);
        pen.setWidth(2);
        painter.setBrush(QBrush(QColor("red")));
        painter.setPen(pen);

        #list for polygon
        p = self.points;
        poly = [];
        end_x = self.get_x_from_area(area);
        #~ print(end_x);
        
        for i in range(1,len(self.items)+1):
            if self.get_area_to(p[2*i].x()) < area and 2*i != len(p)-1:
                poly.append(p[2*i]);
                poly.append(p[2*i+1]);
            else:
                poly.append(QPoint(end_x, p[2*i].y()));
                poly.append(QPoint(end_x, 0));
                break;
        poly2 = copy.deepcopy(poly);
        self.offset(poly2, 0, -150);
        self.scale(poly2, 1, -1);
        
        pen.setColor("red");
        painter.setPen(pen);
        painter.drawPolygon( QPolygon( poly2 ));
        
        pen.setColor(color);
        painter.setPen(pen);
        painter.drawPolyline( QPolygon( self.get_points(of_y = -150, sc_y = -1) ) );
        
        
        #end poly
        painter.end();
    
    def get_area_to(self, x_in):
        area = 0;
        old_x = 0;
        p = self.points;
        for i in range(len(self.items)):
            if p[2*i+2].x() < x_in:
                area += (p[2*i+2].x() - old_x)*p[2*i+1].y();
            else:
                area += (x_in - old_x)*(p[2*i+1].y());
                break;
            old_x = p[2*i+2].x();
        return area;
    
    def get_x_from_area(self, area):
        p = self.points;
        old_x = 0;
        for i in range(len(self.items)):
            next_area = (p[2*i+2].x()-old_x)*p[2*i+1].y();
            #~ print(i," next_area: ",next_area, "old_x: ", old_x, "y: ", p[2*i+1].y(),"x_new: ", p[2*i+2].x());
            if next_area < area:
                area -= next_area;
            else:
                return old_x + area/p[2*i+1].y();
            old_x = p[2*i+2].x();
        return 0;
    
    def __str__(self):
        res = "";
        for i in range(1,len(self.items)):
            res += str(self.items[i]) + " (" + str(self.points[2*i].x()) + "/" + str(self.points[2*i].y()) + ")-(" \
                                           + str(self.points[2*i+1].x()) + "/" + str(self.points[2*i+1].y()) + ")\n" 
    
        return res;
