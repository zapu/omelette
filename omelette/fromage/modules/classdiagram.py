from omelette.fromage.common import DrawableNode

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF
from PyQt4.Qt import *
import math

class DrawableClass(DrawableNode, QGraphicsItem):
    def __init__(self, uml_object):
        super(DrawableClass, self).__init__(uml_object)
        QGraphicsItem.__init__(self)
        self.__boundingRect = QRectF(0, 0, 100, 100)
        self.__font = QFont('Comic Sans MS', 10)
        self.__sectionMargin = 5
        self.__textMargin = 3
        
        self.setFlag(QGraphicsItem.ItemIsMovable, 1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, 1)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, 1)

    def boundingRect(self):
        return self.__boundingRect
    
    def paint(self, painter, style, widget):
        metrics = QFontMetrics(self.__font)
        painter.setFont(self.__font)
        painter.setPen(QColor(0,0,0))

        currentHeight = self.__sectionMargin
        painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(self.__getitem__('name')), metrics.height()), 0, self.__getitem__('name'))
        currentHeight += self.__sectionMargin + metrics.height()
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        currentHeight += self.__sectionMargin
        for attribute in self.attributes():
            painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(attribute), metrics.height()), 0, attribute)
            currentHeight += self.__textMargin + metrics.height()
        
        currentHeight += self.__sectionMargin    
        painter.drawLine(0, currentHeight, self.__boundingRect.width(), currentHeight)
        currentHeight += self.__sectionMargin
        for operation in self.operations():
            painter.drawText(QRect(self.__textMargin, currentHeight, metrics.width(operation), metrics.height()), 0, operation)
            currentHeight += self.__textMargin + metrics.height()
            
        painter.drawRect(self.__boundingRect)
    
    def __sizeOfSection(self, metrics, list):
        count = 0
        maxWidth = 0
        for text in list:
            maxWidth = max(maxWidth, 2 * self.__textMargin + metrics.width(text))
            count += 1

        return (maxWidth, 2 * self.__sectionMargin + (count - 1) * self.__textMargin + count * metrics.height())
    
    def updateSize(self):
        metrics = QFontMetrics(self.__font)
        fontHeight = metrics.height()
        drawableHeight = 2 * self.__sectionMargin + metrics.height()
        drawableWidth = 2 * self.__textMargin + metrics.width(self.__getitem__('name'))
        
        for section in [self.operations(), self.attributes()]:
            size = self.__sizeOfSection(metrics, section)
            drawableWidth = max(drawableWidth, size[0])
            drawableHeight += size[1]
        
        self.__boundingRect = QRectF(0, 0, 2 * self.__textMargin +  drawableWidth, drawableHeight)
        
        pass
        