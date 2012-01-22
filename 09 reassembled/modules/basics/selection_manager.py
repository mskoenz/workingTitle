#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    17.01.2012 15:36:33 CET
# File:    selection_manager.py

import sys
from ..qt_import import *

class selection_manager(list):
    def __init__(self):
        self = [];
    
    def is_on(self, item):
        if item in self:
            return True;
        return False;
    
    def select_item_add(self, item):
        if item not in self:
            item.setChecked(True);  #item specifics
            self.append(item);
    
    def select_item(self, item):
        self.deselect_all();
        self.select_item_add(item);
        
    def deselect_item_add(self, item):
        if item in self:
            item.setChecked(False);  #item specifics
            self.remove(item);
        
    def toggle_item_add(self, item):
        if item not in self:
            self.select_item_add(item);
        else:
            self.deselect_item_add(item);
            
    def toggle_item(self, item):
        if item in self:
            self.deselect_all();
        else:
            self.deselect_all();
            self.select_item_add(item);

    def select_list_add(self, items):
        for item in items:
            self.select_item_add(item);
    
    def deselect_all(self):
        while self:
            self.deselect_item_add(self[0]);
            
    def select_list(self, items):
        self.deselect_all();
        self.select_list_add(items);

        
