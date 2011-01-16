import sys
from PyQt4 import QtGui, QtCore
from omelette.parser.parser import Parser
from omelette.fromage.ui import Ui_MainWindow
from omelette.fromage.qscintilla import QSci
from omelette.fromage.factory import DrawableFactory

class FromageForm(QtGui.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self, parent)
        self.parser = Parser()
        self.setupUi(self)

        self.layout = QtGui.QHBoxLayout(self.centralwidget)
        self.splitter = QtGui.QSplitter(self.centralwidget)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)

        self.qsci = QSci(self.splitter)
        self.scene = QtGui.QGraphicsScene(self.splitter)
        self.view = QtGui.QGraphicsView(self.splitter)
        self.view.setScene(self.scene)
        self.scene.setSceneRect(QtCore.QRectF(0, 0, 500, 500))

        self.layout.addWidget(self.splitter)

        QtCore.QObject.connect(self.actionGenerate,
                QtCore.SIGNAL("triggered()"), self.generate)

    def generate(self):
        self.scene.clear()

        code = "prototype base class\n" + self.qsci.text()
        uml_objects = self.parser.parse(code)

        for name, uml_object in uml_objects.items():
            uml_object["name"] = name

        for uml_object in uml_objects.values():
            if uml_object.is_prototype: continue

            drawable = DrawableFactory.create("class", uml_object)
            drawable.updateSize()
            
            self.scene.addItem(drawable)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    form.show()
    sys.exit(app.exec_())
