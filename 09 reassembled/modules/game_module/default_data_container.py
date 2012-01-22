#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 09:55:36 CET
# File:    default_data_container.py

import math

class SDict(dict):
    def __init__(self):
        super(SDict, self).__init__();
        
    def set_eco(self, reso, gas, sup, time, height = None):
        self["min"] = reso;
        self["gas"] = gas;
        self["sup"] = sup;
        self["time"] = time;
        if height == None:
            self["mps"] = round(reso*1.0/time);
        else:
            self["mps"] = height;
        self["gps"] = round(gas*1.0/time);

    def set_name(self, name, short):
        self["name"] = name;
        self["short"] = short;

data_cont = SDict();
data_cont["name"] = "not set";
data_cont["short"] = "not_set";
data_cont["min"] = 0;
data_cont["gas"] = 0;
data_cont["sup"] = 0;
data_cont["time"] = 0;
data_cont["mps"] = 0;
data_cont["gps"] = 0;

#~ data_cont["type"] = 0;
#~ data_cont["HP"] = 0;
#~ data_cont["energy"] = 0;
#~ data_cont["speed"] = 0;
#~ data_cont["armor"] = 0;
#~ data_cont["sight"] = 0;
#~ 
#~ data_cont["grd_weapon"] = 0;
#~ data_cont["air_weapon"] = 0;
#~ 
#~ data_cont["limited"] = 32;
#~ data_cont["limits"] = [];
#~ data_cont["options"] = [];
#~ data_cont["unlocks"] = [];
#~ data_cont["techReq"] = [];
#~ data_cont["alpha"] = [];
