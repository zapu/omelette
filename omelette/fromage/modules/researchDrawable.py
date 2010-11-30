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
        
        self.__relationText = self.source.name + "-" + self.target.name
        
        self.source.edges.append(self)
        self.target.edges.append(self)
        
        self.__textExtra = 0
        
        if(self.target.name == "barnex"):
            self.setPen(QPen(QColor(255, 0, 0), 1, Qt.DotLine, Qt.RoundCap, Qt.RoundJoin))
        else:
            self.setPen(QPen(QColor(255, 0, 0), 2, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            
        self.update()
        
    def update(self):
        self.setLine(QLineF(self.source.pos(), self.target.pos()))
        
    def paint(self, painter, style, widget):
        #matrix = QMatrix()
        
        srodekX = self.line().p1().x() + self.line().dx() / 2
        srodekY = self.line().p1().y() + self.line().dy() / 2
        
        fontMetrics = painter.fontMetrics()
        self.__textExtra = fontMetrics.width(self.__relationText)
        
        #matrix.translate(srodekX, srodekY)
        #matrix.rotate(45)
        #painter.setMatrix(matrix)
        
        #painter.drawText(QPointF(srodekX, srodekY), self.source.name + "-" + self.target.name)
        painter.drawText(QPointF(srodekX - fontMetrics.width(self.__relationText) / 2, srodekY - 10), self.__relationText)
        
        #painter.setMatrix(QMatrix())
        
        QGraphicsLineItem.paint(self, painter, style, widget)
        
    def boundingRect(self):
        #extra = (self.pen().width() + 20) / 2.0;
        extra = self.__textExtra
        
        return QRectF(self.line().p1(), 
                      QSizeF(self.line().p2().x() - self.line().p1().x(),
                      self.line().p2().y() - self.line().p1().y())).normalized().adjusted(-extra, -extra, extra, extra);

    
    