try:
    #~ from PySide1.QtCore import *
    #~ from PySide1.QtGui import *
    from PySide.QtCore import *
    from PySide.QtGui import *
    print("PySide loaded")
except ImportError:
    try:
        from PyQt4.QtCore import *
        from PyQt4.QtGui import *
        print("PyQt4 loaded")
    except ImportError:
        print("Error: no PySide or PyQt4 Module")

