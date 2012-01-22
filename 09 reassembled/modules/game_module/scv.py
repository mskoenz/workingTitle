#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 09:55:00 CET
# File:    scv.py

from .default_data_container import *
import copy

scv_data = copy.deepcopy(data_cont);
scv_data.set_name("SCV", "scv");
scv_data.set_eco(50, 0, 1, 17);
