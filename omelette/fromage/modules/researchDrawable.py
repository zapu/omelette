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
        
        self.edges = []
                
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
            self.updateEdges()
            #update arrows here etc

        return value
    
    def updateEdges(self):
        for edge in self.edges:
            edge.update()
            
    
    
class DrawableRelation(QGraphicsLineItem):
    def __init__(self, source, target):
        QGraphicsLineItem.__init__(self)
        
        self.source = source
        self.target = target
        
        self.source.edges.append(self)
        self.target.edges.append(self)
        
        if(self.target.name == "barnex"):
            self.setPen(QPen(QColor(255, 0, 0), 1, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            self.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            
        self.update()
        
    def update(self):
        self.setLine(QLineF(self.source.pos(), self.target.pos()))
        pass
        
    def paint(self, painter, style, widget):
        QGraphicsLineItem.paint(self, painter, style, widget)
        pass
    
    