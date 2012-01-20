#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    20.01.2012 08:56:48 CET
# File:    with_gamedata.py


import sys
from modules.qt_import import *
from modules import *
#=======================================================================================================================

    
#=======================================================================================================================
class Example(base_widget):
    def __init__(self):
        super(Example, self).__init__(self);
        self.setWindowTitle("Click or Move");
        self.setGeometry(100, 100, 700, 500);
        
        self.add_item("scv", -17, 3);
        self.add_item("scv", -17, 6);
        self.add_item("scv", -17, 9);
        self.add_item("scv", -17, 12);
        self.add_item("scv", -17, 15);
        self.add_item("scv", -17, 18);
        self.add_item("cmd", -100, 21);
        self.add_item("spm", 90, 10);
        self.add_item("spm", 60, 10);
        self.add_item("mule", 30, 13);
        self.add_item("mule", 30, 12);
        self.add_item("stimP", 60, 9);
        self.add_item("rea", 160, 8);
        
        
#=======================================================================================================================
def main():
    app = QApplication(sys.argv);
    #~ app.setStyle("plastique")
    ex = Example();
    ex.show();
    app.exec_();
    
if __name__ == '__main__':
    main();
    
