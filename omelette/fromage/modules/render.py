from PyQt4.QtGui import *

from omelette.fromage.modules.classdiagram import *
from omelette.parser.uml import UMLObject

import random

class DiagramScene(QGraphicsScene):
    def __init__(self, parent):        
        QGraphicsScene.__init__(self, parent)
        self.demoimage = None
                
    def demoStart(self):
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.drawTest)
        self.timer.start(1000)
        
        self.demoimage = QImage(self.sceneRect().width(), self.sceneRect().height(), QImage.Format_RGB32)
        demopainter = QPainter(self.demoimage)
        demopainter.fillRect(self.sceneRect(), QBrush(QColor(255,255,255), Qt.SolidPattern))        
        
    def drawTest(self):        
        demopainter = QPainter(self.demoimage)
        
        transform = QTransform()
        transform.translate(random.randint(0, self.sceneRect().width()), random.randint(0, self.sceneRect().height()))
        
        demopainter.setTransform(transform)
        
        uml = UMLObject()
        uml.__setitem__('name', 'barnex')
        uml.add_attribute("# attr1")
        uml.add_attribute("# dlugi attr2")
        uml.add_operation("- jakas_operacja():string")
        uml.add_operation("+ toString():int")
        dc = DrawableClass(uml)
        dc.updateSize()
        dc.paint(demopainter, None, None)
        
        demopainter.end()
        self.update()
    
    def drawForeground(self, painter, rect):
        if(self.demoimage != None):
            painter.drawImage(0, 0, self.demoimage)