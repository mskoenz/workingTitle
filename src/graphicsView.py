from PyQt4.QtCore import *
from PyQt4.QtGui import *

class CustomView(QGraphicsView): 
    def __init__(self):
        QGraphicsView.__init__(self, parent = None)
        self.setRenderHints(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
