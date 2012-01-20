#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    19.01.2012 13:34:10 CET
# File:    utilities.py

def time_from_sec(sec):
    s = int(sec)%60;
    m = int(sec/60);
    return str(m)+":"+("0" if s < 10 else "")+str(s);

def sign(arg):
    return int(math.copysign(1, arg));
