#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 13:34:10 CET
# File:    utilities.py

from ..qt_import import QPoint
import math

def time_from_sec(sec):
    s = int(sec)%60;
    m = int(sec/60);
    return str(m)+":"+("0" if s < 10 else "")+str(s);

def sign(arg):
    return int(math.copysign(1, arg));

def QPointS(size):
    return QPoint(size.width(), size.height());

def dist(point):
    return math.sqrt(pow(point.x(), 2)+pow(point.y(), 2));

def map_to_grid(point, grid_size):
    x = int(point.x()/grid_size)*grid_size;
    y = int(point.y()/grid_size)*grid_size;
    return QPoint(x, y);

def addX(point, dx):
    point.setX(point.x()+dx);

def addY(point, dy):
    point.setY(point.y()+dy);

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
