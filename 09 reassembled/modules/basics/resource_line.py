#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:47:16 CET
# File:    resource_line.py
#
import copy
import math
from ..qt_import import *
from .__style_options import *
from .utilities import *

class resource_line:
    def __init__(self, parent, start, end):
        #invariant: always sorted in x-direction
        self.points = [QPoint(start,0), QPoint(start,0), QPoint(end, 0)];
        self.items = ["start"];
        self.x_offset = [0];
        self.pos = [];
        self.pos.append([0]);
        self.parent = parent;
    
    #add item
    def add_item(self, item, x_pos, heigth, offset = 0):
        i = 0;
        offset *= style_icon_scale_width;
        while(self.points[i].x() < x_pos+offset):
            i+=1;
        
        ground = self.points[i-1].y();
        self.points.insert(i, QPoint(x_pos + offset, ground));
        self.points.insert(i, QPoint(x_pos + offset, ground));
        
        if item in self.items:
            k = self.items.index(item); #every item holds all index of its identities
            self.pos[k].append(int(i/2)); #insert new index
            self.pos.insert(int(i/2), self.pos[k]); #give the new one the list
        else:
            self.pos.insert(int(i/2), [int(i/2)]);
        
        if len(self.items) > int(i/2): #if insert != append all following index must be incremented
            for j in range(int(i/2)+1, len(self.pos)):
                posi = self.pos[j];
                k = posi.index(j-1);
                posi[k] = j;
        
        self.items.insert(int(i/2), item);
        self.x_offset.insert(int(i/2), offset);
        
        
        for p in self.points[i+1:]:
            addY(p, style_icon_scale_height*heigth);
    
    def move_item_to(self, item, x):
        k = self.items.index(item);
        self.move_item_by(item, x-self.points[2*k].x()+self.x_offset[k]);
    
    def move_item_by(self, item, dx):
        i = self.items.index(item);
        
        p = self.points;
        it = self.items;
        pos = self.pos;
        off = self.x_offset;
        
        for k in pos[i]:
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
                    jk = pos[k].index(k);
                    ji = pos[i].index(i);
                    pos[k][jk] = i;
                    pos[i][ji] = k;
                    pos[k], pos[i] = pos[i], pos[k];
                    off[k], off[i] = off[i], off[k];
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
                    
                    jk = pos[k].index(k);
                    ji = pos[i].index(i);
                    pos[k][jk] = i;
                    pos[i][ji] = k;
                    pos[k], pos[i] = pos[i], pos[k];
                    off[k], off[i] = off[i], off[k];
                    it[k], it[i] = it[i], it[k];
                    
                    i-=1;
                    k-=1;
    
    #trafo functions
    def offset(self, vec, trafo):
        for p in vec:
            p += QPoint(trafo[0], trafo[1]);
    
    def scale(self, vec, trafo):
        for p in vec:
            p.setX(p.x()*trafo[2]);
            p.setY(p.y()*trafo[3]);
    
    #transformation only occurs if the points need to be known
    def get_points(self, trafo): #Todo: optimize
        p = self.points;
        res = copy.deepcopy(p);
        for i in range(len(p)-1, 1, -1):    #to remove zero-edges (see get_plygon) except start
            if p[i] == p[i-1]:
                res.remove(res[i]);
                res.remove(res[i-1]);
        self.offset(res, trafo);
        self.scale(res, trafo);
        return res;
        
    def get_polygon(self, area, trafo):
        #list for polygon
        p = self.points;
        poly = [];
        end_x = self.get_x_from_area(area);
        
        for i in range(1,len(self.items)+1):
            if self.get_area_to(p[2*i].x()) < area and 2*i != len(p)-1:
                if poly and poly[-1] == p[2*i]: #to prevent zero-edges      # moves here =>         | zero-edge     
                    poly.remove(poly[-1]);                                  #    |   v   =>         v               
                else:                                                       #    | +-+   =>         +               
                    poly.append(p[2*i]);                                    #    v | |   =>         |               
                poly.append(p[2*i+1]);                                      #      | |   =>       +-+    or +-+     
            else:                                                           #    +-+ +-- =>       | +---    | +---  
                poly.append(QPoint(end_x, p[2*i].y()));                     #    |       =>       |         | |     
                poly.append(QPoint(end_x, 0));                              #----+       => ------+       --+ +     
                break;
        
        poly2 = copy.deepcopy(poly);
        
        self.offset(poly2, trafo);
        self.scale(poly2, trafo);
        return poly2;
    
    def paint(self, parent, area, line_color = style_line_color, area_color = style_area_color, \
              trafo = [style_x_offset, style_y_offset, style_x_scale, style_y_scale]):
        painter = QPainter();
        painter.begin(parent);
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing);
        
        #determin, where the gradient should start
        start = 0;
        if len(self.items) > 8:
            start = self.points[16].x();
        #pos where the gradient should end
        end = self.get_x_from_area(area);
        
        #init for polygon
        a_brush = QBrush(SGradient(QPoint(start,0), QColor(area_color[0]), QPoint(end, 0), QColor(area_color[1])));
        painter.setBrush(a_brush);
        a_pen = SPen();
        a_pen.setBrush(a_brush);
        painter.setPen(a_pen);
        
        #draw polygon
        painter.drawPolygon( QPolygon( self.get_polygon(area, trafo) ));
        
        #draw marker line
        painter.drawLine(QPoint(end, 0), QPoint(end, 600));
        painter.drawText(QPoint(end+10, 20), time_from_sec(end/style_icon_scale_width));
        #init for line
        l_brush = QBrush(SGradient(QPoint(0,0), QColor(line_color[0]), QPoint(self.parent.size().width(), 0), QColor(line_color[1])));
        l_pen = SPen();
        l_pen.setBrush(l_brush);
        painter.setPen(l_pen);
        #draw reso line
        painter.drawPolyline( QPolygon( self.get_points(trafo) ) );
        
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
        if area == 0:
            return 0;
        
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
