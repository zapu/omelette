import sys
sys.path.append('../') 
from PyQt4 import QtGui
from omelette.fromage.fromage import FromageForm

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = FromageForm()
    form.show()
    sys.exit(app.exec_())
