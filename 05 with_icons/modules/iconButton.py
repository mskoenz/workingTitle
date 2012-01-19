#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    18.01.2012 10:09:36 CET
# File:    iconButton.py

from os import path
from .qt_import import *
from .moveablePushButton import *
from .__style_options import *

class iconButton(moveablePushButton):
    def __init__(self, parent, img, width, height):
        super(iconButton, self).__init__(img, parent);
        self.img_path = path.join("", "icons", img+".png");

        self.parent = parent;
        self.setFixedSize(QSize(style_icon_scale_width*width, style_icon_scale_height*height));
        self.setToolTip(img);
        
    def paint(self):
        checked = self.isChecked();
        #choose colorset
        if checked:
            col_bg0 = QColor(style_icon_background_sel[0]);
            col_bg1 = QColor(style_icon_background_sel[1]);
            col_line0 = QColor(style_icon_line_sel[0]);
            col_line1 = QColor(style_icon_line_sel[1]);
        else:
            col_bg0 = QColor(style_icon_background_normal[0]);
            col_bg1 = QColor(style_icon_background_normal[1]);
            col_line0 = QColor(style_icon_line_normal[0]);
            col_line1 = QColor(style_icon_line_normal[1]);
        
        #init painter
        pos = QPoint(0,0);
        size = QPoint(self.size().width(), self.size().height()) - QPoint(2,2); #<- empiric, don't ask
        painter = QPainter();
        painter.begin(self);
        painter.setRenderHints(style_icon_background_render);
        
        #init pen for background
        pen_width = style_pen_width;
        offset = QPoint(int(pen_width/2), int(pen_width/2));
        pen = SPen("black", pen_width);
        pen.setBrush(SGradient(pos, col_line0, pos+size, col_line1))
        
        #paint background
        painter.setPen(pen);
        painter.setBrush(SGradient(pos, col_bg0, pos+size, col_bg1));
        painter.drawRoundedRect(QRect(pos+offset, pos+size-offset), style_rounded_radius, style_rounded_radius);
        
        #scale icon
        img = QPixmap(self.img_path);
        minimum = min(self.size().height(), self.size().width()) - 2*style_icon_pixmap_smaller;
        if style_icon_max_pixmap_size > minimum:
            img = img.scaled(minimum, minimum, transformMode = style_icon_pixmap_trafo);
        
        #paint icon
        img_pos = QPoint(img.size().width(), img.size().height());
        painter.drawPixmap((pos+size+QPoint(2,2)-img_pos)/2, img);
        
        #done :)
        painter.end();

    def paintEvent(self, e):
        self.paint();
