#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 10:10:31 CET
# File:    spm.py

from .default_data_container import *
import copy

spm_data = copy.deepcopy(data_cont);
spm_data.set_name("Spacemarine", "spm");
spm_data.set_eco(50, 0, 1, 25);
