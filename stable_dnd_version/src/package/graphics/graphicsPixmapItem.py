from ..qt_import import *
import math

class CustomItem(QGraphicsPixmapItem):
    def __init__(self, name, parent = None):
        QGraphicsPixmapItem.__init__(self)
        self.setPixmap(QPixmap(name+".png").scaled(68,68, Qt.IgnoreAspectRatio, Qt.SmoothTransformation))
        self.name = name
        self.setFlags(QGraphicsItem.ItemIsSelectable | QGraphicsItem.ItemIsMovable)
        self.setTransformationMode(Qt.SmoothTransformation)        
    
    def paint(self, painter, option, widget):
        if(self.isSelected() == True):
            self.setPixmap(QPixmap(self.name+"M.png"))
        else:
            self.setPixmap(QPixmap(self.name+".png"))
            
        option.state &= ~QStyle.State_Selected
        QGraphicsPixmapItem.paint(self, painter, option, widget)
        
    def top(self):
        return self.mapRectToScene(self.boundingRect()).y()
    def bottom(self):
        rect = self.mapRectToScene(self.boundingRect())
        return rect.y()+self.boundingRect().height()
    def left(self):
        return self.mapRectToScene(self.boundingRect()).x()
    def right(self):
        rect = self.mapRectToScene(self.boundingRect())
        return rect.x()+self.boundingRect().width()
    def checkStatus(self, otherItem):
        res = 0

        if(otherItem.bottom() > self.top()):
            if(otherItem.top() < self.bottom()):
                res += 3
            else:
                res += 0
        else:
            res += 6
            
        if(otherItem.left() < self.right()):
            if(otherItem.right() < self.left()):
                res += 2
            else:
                res += 1
        else:
            res += 0
        
        return res;
        

class PositionControl:
    def __init__(self):
        self.lastPos = QCursor.pos()
        self.lastPos2 = QCursor.pos()
        self.maxSpeed = 1000
    def accept(self):
        #~ self.lastPos.setX(self.lastPos2.x())
        #~ self.lastPos.setY(self.lastPos2.y())
        
        dx = QCursor.pos().x()-self.lastPos2.x()
        dy = QCursor.pos().y()-self.lastPos2.y()
        
        if math.fabs(dx) > self.maxSpeed:
            dx = math.copysign(self.maxSpeed, dx)
            
        if math.fabs(dy) > self.maxSpeed:
            dy = math.copysign(self.maxSpeed, dy) 
        
        self.lastPos2.setX(self.lastPos2.x()+dx)
        self.lastPos2.setY(self.lastPos2.y()+dy)
        
        #~ QCursor.setPos(self.lastPos2)
        return [dx, dy]
        
    def update(self):
        self.lastPos2 = QCursor.pos()
        self.lastPos = QCursor.pos()
    def moveCursor(self):
        QCursor.setPos(self.lastPos2)
        self.lastPos.setX(self.lastPos2.x())
        self.lastPos.setY(self.lastPos2.y())
    def revertCursor(self):
        #~ QCursor.setPos(self.lastPos)
        self.lastPos2.setX(self.lastPos.x())
        self.lastPos2.setY(self.lastPos.y())

    
