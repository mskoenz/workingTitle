#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    16.01.2012 15:54:17 CET
# File:    skeleton_item.py

from os import path
import copy
import math
from qt_import import QPoint


def sign(arg):
    return int(math.copysign(1, arg));

def addX(point, dx):
    point.setX(point.x()+dx);

def addY(point, dy):
    point.setY(point.y()+dy);

class resource_line:
    def __init__(self, width):
        #invariant: always sorted in x-direction
        self.points = [QPoint(0,0), QPoint(0,0), QPoint(width, 0)];
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
    
    def get_points(self, of_x = 0, of_y = 0, sc_x = 1, sc_y = 1):
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
        
        if dx > 0:
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
                
        if dx < 0:
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
    
    def __str__(self):
        res = "";
        for i in range(1,len(self.items)):
            res += str(self.items[i]) + " (" + str(self.points[2*i].x()) + "/" + str(self.points[2*i].y()) + ")-(" \
                                           + str(self.points[2*i+1].x()) + "/" + str(self.points[2*i+1].y()) + ")\n" 
    
        return res;

class item:
    def __init__(self, name):
        self.img_path = path.join("..", "img", name+".png");
        self.marked_path = path.join("..", "img", name+"M.png");
    
    def __str__(self):
        res = "item-class" + "\n";
        res += self.img_path + "\n";
        res += (self.marked_path) + "\n";
        return res;
    
#~ it1 = item("gho");
#~ it2 = item("tho");
#~ it3 = item("scv");
#~ 
#~ l = resource_line(100);
#~ 
#~ l.add_item(it1, 5, 10);
#~ l.add_item(it2, 50, 10);
#~ l.add_item(it3, 80, 10);
#~ 
#~ l.move_item(it1, 0);
#~ 
#~ print(l);
