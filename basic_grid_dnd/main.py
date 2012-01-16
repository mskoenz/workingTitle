import sys
from qt_import import *

class Button(QPushButton):
  
    def __init__(self, title, parent):
        super().__init__(title, parent)

    def mouseMoveEvent(self, e):

        if e.buttons() != Qt.LeftButton:
            return

        mimeData = QMimeData()
        
        data = QByteArray();
        text = QDataStream(data, QIODevice.WriteOnly);
        text << self.pos();
        mimeData.setData("pos",data);
        
        drag = QDrag(self)
        drag.setMimeData(mimeData)
        drag.setHotSpot(e.pos() - self.rect().topLeft())
        
        dropAction = drag.start(Qt.MoveAction)


    def mousePressEvent(self, e):
      
        QPushButton.mousePressEvent(self, e)
        if e.button() == Qt.LeftButton:
            print('press')


class Example(QWidget):
  
    def __init__(self):
        super(Example, self).__init__()
        self.setWindowTitle('Click or Move')
        self.setGeometry(300, 300, 300, 300)
        self.setAcceptDrops(True)

        self.button1 = Button('1', self);
        self.button2 = Button('2', self);
        self.button3 = Button('3', self);
        self.button1.setGeometry(10,20,20,20);
        self.button2.setGeometry(100,20,20,20);
        self.button3.setGeometry(150,20,20,20);

        self.belegung =  [];
        for i in range(30):
            self.belegung.append([]);
            for j in range(30):
                self.belegung[i].append(0);

    def dragEnterEvent(self, e):
        e.accept();

    def dropEvent(self, e):

        position = e.pos()
        nx = int(position.x()/10);
        ny = int(position.y()/10);
        
        b = self.belegung;
        
        if(b[nx][ny] == 0 and b[nx][ny] == 0 and b[nx+1][ny] == 0 and b[nx][ny-1] == 0 and b[nx+1][ny-1] == 0):
            
            data = e.mimeData().data("pos");
            data2 = QDataStream(data, QIODevice.ReadOnly)
            p = QPoint()
            data2 >> p;
            
            ox = int(p.x()/10);
            oy = int(p.y()/10);
            
            b[ox][oy] = 0;
            b[ox+1][oy] = 0;
            b[ox+1][oy-1] = 0;
            b[ox][oy-1] = 0;
            
            b[nx][ny] = 1;
            b[nx+1][ny] = 1;
            b[nx+1][ny-1] = 1;
            b[nx][ny-1] = 1;
            
            
            if p == self.button1.pos():
                self.button1.move(QPoint(int(position.x()/10)*10, int(position.y()/10)*10))
            if p == self.button2.pos():
                self.button2.move(QPoint(int(position.x()/10)*10, int(position.y()/10)*10))
            if p == self.button3.pos():
                self.button3.move(QPoint(int(position.x()/10)*10, int(position.y()/10)*10))
            
            e.setDropAction(Qt.MoveAction)
            e.accept()

def main():
  
    app = QApplication(sys.argv)
    ex = Example()
    ex.show()
    app.exec_()  

if __name__ == '__main__':
    main()
