import sys
from os import path

from package import *
from package.qt_import import QApplication

app = QApplication(sys.argv)

mainw = CustomView()
scene = CustomScene(mainw)

img_prefix = path.join(path.curdir, 'img', 'gho')

scene.addPixmap(img_prefix, 9.5, 9.5)
scene.addPixmap(img_prefix, 109.5, 109.5)
scene.addPixmap(img_prefix, 9.5, 109.5)
scene.addPixmap(img_prefix, 199.5, 109.5)
scene.addPixmap(img_prefix, 199.5, 199.5)
scene.addPixmap(img_prefix, 9.5, 199.5)


mainw.setScene(scene)

mainw.show()

sys.exit(app.exec_())
