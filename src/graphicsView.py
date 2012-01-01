try:
    #~ from PySide1.QtCore import *
    #~ from PySide1.QtGui import *
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
    except ImportError:
        print("Error: no PySide or PyQt4 Module")

class CustomView(QGraphicsView): 
    def __init__(self):
        QGraphicsView.__init__(self, parent = None)
        self.setRenderHints(QPainter.SmoothPixmapTransform)
        self.setDragMode(QGraphicsView.RubberBandDrag)
        
