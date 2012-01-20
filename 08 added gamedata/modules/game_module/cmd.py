#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 11:33:04 CET
# File:    cmd.py


from .default_data_container import *
import copy

cmd_data = copy.deepcopy(data_cont);
cmd_data.set_name("Command Center", "cmd");
cmd_data.set_eco(400, 0, -11, 100);
