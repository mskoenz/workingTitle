import sys

try:
    #~ from PySide1.QtCore import *
    #~ from PySide1.QtGui import *
    from PySide.QtCore import *
    from PySide.QtGui import *
except ImportError:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        print()
    except ImportError:
        print("Error: no PySide or PyQt4 Module")

from graphicsView import CustomView
from graphicsScene import CustomScene
from graphicsPixmapItem import CustomItem

app = QApplication(sys.argv)

mainw = CustomView()
scene = CustomScene(mainw)

scene.addPixmap("gho", 9.5, 9.5)
scene.addPixmap("gho", 109.5, 109.5)
scene.addPixmap("gho", 9.5, 109.5)
scene.addPixmap("gho", 199.5, 109.5)
scene.addPixmap("gho", 199.5, 199.5)
scene.addPixmap("gho", 9.5, 199.5)


mainw.setScene(scene)

mainw.show()

sys.exit(app.exec_())
