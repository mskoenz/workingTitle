#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 12:45:43 CET
# File:    mule.py


from .default_data_container import *
import copy

mule_data = copy.deepcopy(data_cont);
mule_data.set_name("M.U.L.E", "mule");
mule_data.set_eco(0, 0, 0, 90, height = 1);
