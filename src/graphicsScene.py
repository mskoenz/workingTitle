from PyQt4.QtCore import *
from PyQt4.QtGui import *
from graphicsPixmapItem import *

import math

class CustomScene(QGraphicsScene):
    def __init__(self, parent = None):
        QGraphicsScene.__init__(self)
        self.setBackgroundBrush(QColor("black"))
        self.setSceneRect(0, 0, 300, 300)
        self.itemlist = []
        self.ctrl = PositionControl()
        
    def addPixmap(self, name, cx, cy):
        self.itemlist.append(CustomItem(name, self))
        self.itemlist[-1].moveBy(cx, cy)
        self.addItem(self.itemlist[-1])
        
    def mouseMoveEvent(self, event):
        a = self.selectedItems()
        #~ QGraphicsScene.mouseMoveEvent(self, event)
        d = self.ctrl.accept()
        
        for z in a:
            z.moveBy(d[0], d[1])
        #~ Qt.IntersectsItemBoundingRect
        for z in a:
            if(len(z.collidingItems()) != 0):
                self.ctrl.revertCursor()
                for z in a:
                    z.moveBy(-d[0], -d[1])

        self.ctrl.moveCursor()

    def mousePressEvent(self, event):
        QGraphicsScene.mousePressEvent(self, event)
        self.ctrl.update()
        
