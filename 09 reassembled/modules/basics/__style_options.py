#!/usr/bin/python3.2
# -*- coding: cp1252 -*-
#
# Author:  Mario S. Könz <mskoenz@gmx.net>
# Date:    18.01.2012 11:01:51 CET
# File:    __style_options.py


from .painter_helper import *

#=======================================================================================================================
#for the base_widget class==============================================================================================

style_paint_cursor_img = "cursor_red.png";
style_grid_size = 5;
#=======================================================================================================================
#for the iconButton class===============================================================================================

#renderoptions (QPainter.[Antialiasing, TextAntialiasing, SmoothPixmapTransform, HighQualityAntialiasing, NonCosmeticDefaultPen])
style_icon_background_render = QPainter.TextAntialiasing;
#trafo options (Qt.[FastTransformation, SmoothTransformation]
style_icon_pixmap_trafo = Qt.FastTransformation;

#fineline around background
style_pen_width = 1; 

#radius of background edges
style_rounded_radius = 5;

#info for colors [start_gradient (top left), end_gradient (bottom right)]
style_icon_background_normal =  ["green", "black"];
style_icon_line_normal =        ["black", "green"];
style_icon_background_sel =     ["lightgreen", "lime"];
style_icon_line_sel =           ["green", "lightgreen"];

#maximal pixmap size
style_icon_max_pixmap_size = 68;

#margins between background and pixmap 
style_icon_pixmap_smaller = 1;

#scale factors of incoming height, width
style_icon_scale_height = 20;
style_icon_scale_width = 2;

#toggle button
style_icon_toggle_button = Qt.RightButton;
style_icon_drag_button = Qt.LeftButton;

#=======================================================================================================================
#for the resource_line class============================================================================================
style_line_color = ["blue", "black"];
style_area_color = ["lightblue", "blue"];

style_x_offset = 0;
style_y_offset = -400;
style_x_scale = 1;
style_y_scale = -1;
