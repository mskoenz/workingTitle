#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    16.01.2012 15:54:05 CET
# File:    main.py

import sys
from skeleton import *
from qt_import import *

class SWidget(QWidget):
    def __init__(self, reso, parent=None):
        QWidget.__init__(self, parent)
        self.setGeometry(300, 300, 300, 150);
        self.setFixedSize(300, 300);
        self.setMouseTracking(True);
        self.reso_list = reso;
        
    def paintEvent(self, event):
        painter = QPainter();
        painter.begin(self);
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing);
        pen = QPen(QColor("black"));
        pen.setWidth(2);
        painter.setPen(QPen(pen));
        painter.drawPolyline( QPolygon( self.reso_list.get_points( of_y = -150, sc_y = -1) ) );
        painter.end();
        
    def mouseMoveEvent(self, event):
        self.reso_list.move_item_to("a", event.pos().x());
        self.repaint();
        print("bla", event.pos().x());



app = QApplication(sys.argv);

l = resource_line(300);


l.add_item("a", 10, 10);
l.add_item("c", 120, 10);
l.add_item("d", 150, 80);
l.add_item("b", 20, 30);

#~ print(l.points)

mainw = SWidget(l);

print(l);
mainw.show();

sys.exit(app.exec_());
