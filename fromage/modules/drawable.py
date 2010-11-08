from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF

from PyQt4.Qt import*

class DrawableClass(QGraphicsItem):
    def __init__(self, name):
        QGraphicsItem.__init__(self)
        self.name = name
        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
                
    def boundingRect(self):
        return QRectF(0, 0, 100, 100)
        
    def paint(self, painter, style, widget):
        pen = QPen()
        pen.setColor(QColor(255, 255, 255))
        painter.fillRect(0, 0, 100, 100, QColor(0, 0, 0))
        painter.setPen(pen)
        painter.drawText(self.boundingRect(), Qt.AlignCenter, self.name)