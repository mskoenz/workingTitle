#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 09:46:03 CET
# File:    game_data.py

import_list = ["scv", "spm", "cmd", "mule", "stimP", "rea"];

for i in import_list:
    exec("from ." + i + " import *");

sc2 = {}
for i in import_list:
    exec("sc2['" + i + "'] = " + i + "_data");
