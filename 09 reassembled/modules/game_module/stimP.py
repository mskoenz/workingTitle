#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 13:05:25 CET
# File:    stimP.py


from .default_data_container import *
import copy

stimP_data = copy.deepcopy(data_cont);
stimP_data.set_name("Stim Pack", "stimP");
stimP_data.set_eco(100, 100, 0, 170);
