#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 12:45:43 CET
# File:    mule.py


from .default_data_container import *
import copy

rea_data = copy.deepcopy(data_cont);
rea_data.set_name("Reaper", "rea");
rea_data.set_eco(50, 50, 1, 45);
