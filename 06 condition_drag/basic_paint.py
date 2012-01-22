from qt_import import *
import sys

p50 = QPoint(50, 50);
p10 = QPoint(10, 10)+p50;
p10b = QPoint(10, 30);
p11 = QPoint(11, 11)+p50;
p30 = QPoint(30, 30);
p90 = QPoint(90, 90);
px = QPoint(10, 30);

class test(QWidget):
    def __init__(self, parent = None):
        super(test, self).__init__(parent);
        self.rect = QRect(p11, p11);
        self.poly = QPolygon(QRect(p10, p10));
        #~ self.poly = self.poly.subtracted(QPolygon(self.rect));
        self.poly2 = QPolygon(QRect(p10, QPoint(10, 10)));
        self.setMouseTracking(True);
        
    def mouseMoveEvent(self, e):
        if e.buttons() != Qt.RightButton:
            return
        old_cursor = p10;
        new_cursor = e.pos();
        top_l_x = old_cursor.x();
        top_l_y = old_cursor.y();
        bottom_r_x = new_cursor.x();
        bottom_r_y = new_cursor.y();
        
        if old_cursor.y() >= new_cursor.y():
            top_l_y, bottom_r_y = bottom_r_y, top_l_y;
            
        if old_cursor.x() >= new_cursor.x():
            top_l_x, bottom_r_x = bottom_r_x, top_l_x;
            
        self.poly2 = QPolygon(QRect(QPoint(top_l_x, top_l_y), QPoint(bottom_r_x, bottom_r_y)));
        self.repaint();

    def paintEvent(self, e):
        p = QPainter();
        p.begin(self);
        
        ins = self.poly2.intersected(self.poly);
        for i in ins:
            print(i);
        print();
        
        p.drawPolygon(self.poly);
        p.drawPolygon(self.poly2);
        p.setPen(QPen("red"));
        p.drawPoint(px);
        p.end();





def main():
    app = QApplication(sys.argv);
    ex = test();
    ex.show();
    app.exec_();

if __name__ == '__main__':
    main();
