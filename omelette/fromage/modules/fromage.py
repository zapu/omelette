import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import QRectF
from omelette.fromage.modules.qscintilla import QSci
from omelette.fromage.modules.fromage_ui import Ui_MainWindow
from omelette.fromage.modules.render import DiagramScene
from omelette.fromage.modules.classdiagram import *
from omelette.parser.uml import UMLObject

class FromageForm(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.setupUi(self)

        self.horizontal_layout = QtGui.QHBoxLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.qsci = QSci(self.splitter)
        self.diagram = DiagramScene(self)
        self.diagram.setSceneRect(QRectF(0, 0, 500, 500))
        self.diagram.demoStart()
        
        self.graphics_view = QtGui.QGraphicsView(self.splitter)
        self.graphics_view.setScene(self.diagram)

        self.horizontal_layout.addWidget(self.splitter)

    def setupDemo(self):
        uml = UMLObject()
        uml.__setitem__('name', 'barnex')
        uml.add_attribute("# attr1")
        uml.add_attribute("# dlugi attr2")
        uml.add_operation("- jakas_operacja():string")
        uml.add_operation("+ toString():int")
        dc = DrawableClass(uml)
        dc.updateSize()
        
        self.diagram.addItem(dc)
    
if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    #form.setupDemo()
    form.show()
    sys.exit(app.exec_())