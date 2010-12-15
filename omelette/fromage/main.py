import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QPointF

from omelette.fromage.modules.classdiagram import *
from omelette.parser.uml import *
from omelette.fromage.modules.render import *

import PyQt4

class MainWindow(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.resize(500, 500)
        
        self.diagram = DiagramScene(self)
        self.diagram.setSceneRect(QRectF(0, 0, 500, 500))
        self.view = QGraphicsView(self.diagram)
        
        layout = QHBoxLayout()
        layout.addWidget(self.view)
        
        widget = QWidget()
        widget.setLayout(layout)
        
        self.setCentralWidget(widget)
    
        self.setWindowTitle("FROMAGE")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()
    
    uml = UMLObject()
    uml.__setitem__('name', 'barnex')
    uml.add_attribute("# attr1")
    uml.add_attribute("# dlugi attr2")
    uml.add_operation("- jakas_operacja():string")
    uml.add_operation("+ toString():int")
    dc = DrawableClass(uml)
    dc.updateSize()
    
    mainWindow.diagram.addItem(dc)
    
    #mainWindow.diagram.addItem(DrawableRelation(classes[0], classes[1]))
    #mainWindow.diagram.addItem(DrawableRelation(classes[0], classes[2]))
    
    mainWindow.show()

    app.exec_()