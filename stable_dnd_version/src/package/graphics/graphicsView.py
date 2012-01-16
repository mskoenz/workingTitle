from ..qt_import import *

class CustomView(QGraphicsView): 
    def __init__(self):
        QGraphicsView.__init__(self, parent = None)
        self.setRenderHints(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
