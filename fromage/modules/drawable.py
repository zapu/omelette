from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF

from PyQt4.Qt import *
import math

class DrawableClass(QGraphicsItem):
    def __init__(self, name):
        QGraphicsItem.__init__(self)
        
        self.name = name
        
        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)
        
        self.relations = []
                
    def boundingRect(self):
        return QRectF(0, 0, 100, 100)
        
    def paint(self, painter, style, widget):
        pen = QPen()
        pen.setColor(QColor(255, 255, 255))
        painter.fillRect(0, 0, 100, 100, QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.name)
        
    def itemChange(self, change, value):
        if(change == QGraphicsItem.ItemPositionChange):
            newPos = value.toPointF()
            #update arrows here etc

        return value
    
    def updateEdges(self):
        for relation in self.relations:
            relation.update()
            
    
    
class DrawableRelation(QGraphicsItem):
    #broken, will rewrite :(
    
    def __init__(self, source, target):
        QGraphicsItem.__init__(self)
        
        self.source = source
        self.target = target
        
        for node in [self.source, self.target]:
            if(not self in node.relations):
                node.relations.append(self)
        
    def paint(self, painter, style, widget):
        pen = QPen()
        pen.setColor(QColor(255, 255, 255))
        painter.setPen(pen)
        painter.drawLine(self.source.pos(), self.target.pos())
    
    def remove(self): 
        for node in [self.source, self.target]:
            if(not self in node.relations):
                node.relations.remove(self)
                
    def update(self):
        pass
        
    def boundingRect(self):
        pass