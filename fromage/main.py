
import sys

from PyQt4.QtGui import *
from PyQt4.QtCore import QRectF, QPointF

from omelette.fromage.modules.drawable import *

import PyQt4

class DiagramScene(QGraphicsScene):
    def __init__(self, parent):
        QGraphicsScene.__init__(self, parent)


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
    
        
        self.setWindowTitle("trololo czemu mi podkresla tekst na pomaranczowo?")
        

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    mainWindow = MainWindow()
    
    mainWindow.diagram.addItem(DrawableClass("Test 1"))
    mainWindow.diagram.addItem(DrawableClass("Test 2"))
    
    mainWindow.show()

    app.exec_()