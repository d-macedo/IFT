
from PyQt4 import QtCore, QtGui
import numpy as np
import math
import heapq
from PIL import Image 
import pdb
import scipy
from scipy import ndimage
import Queue as Q
import sys
import ift
from skimage import io

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)





class ClickableLabel(QtGui.QLabel):

    coord_object = []
    coord_bg = []

    def __init__(self,test):
        super(ClickableLabel,self).__init__(test)
        self.isPressed = False
        self.pic = QtGui.QPixmap("circle.png")
        self.pic.fill(QtCore.Qt.transparent)
        self.setPixmap(self.pic)

    def mousePressEvent(self,event):
        self.isPressed = True

    def mouseMoveEvent(self,event):
        if (self.isPressed):
            if (event.buttons() == QtCore.Qt.LeftButton):
                pos = event.pos()
                self.pic = self.pixmap()
                self.img = self.pic.toImage()
                
                
                self.img.setPixel(pos.x(),pos.y(),QtGui.qRgb(255,0,0))

                self.pic2 = QtGui.QPixmap.fromImage(self.img)
                self.setPixmap(self.pic2)

                self.coord_object.append((pos.y(),pos.x()))

                
            if(event.buttons() == QtCore.Qt.RightButton):
                pos = event.pos()
                self.pic = self.pixmap()
                self.img = self.pic.toImage()
                self.img.setPixel(pos.x(),pos.y(),QtGui.qRgb(0,0,255))

                

                self.pic2 = QtGui.QPixmap.fromImage(self.img)
                self.setPixmap(self.pic2)

                self.coord_bg.append((pos.y(),pos.x()))

    def mouseReleaseEvent(self,event):
        self.isPressed = False
        
        
        

class Window(QtGui.QMainWindow):

    def __init__(self):
        QtGui.QMainWindow.__init__(self)

        self.main_img = None
        self.main_img_ift = None

        self.centralwidget = QtGui.QWidget(self)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))

        self.clearButton = QtGui.QPushButton(self.centralwidget)
        self.clearButton.setGeometry(QtCore.QRect(80, 450, 94, 30))
        self.clearButton.setObjectName(_fromUtf8("clearButton"))
        self.clearButton.setText("Clear")
        self.clearButton.clicked.connect(self.clearGlass)

        self.x_mouse_position = QtGui.QLabel(self.centralwidget)
        self.x_mouse_position.setGeometry(QtCore.QRect(350, 500, 65, 20))
        self.x_mouse_position.setText(_fromUtf8(""))
        self.x_mouse_position.setObjectName(_fromUtf8("x_mouse_position"))

        self.y_mouse_position = QtGui.QLabel(self.centralwidget)
        self.y_mouse_position.setGeometry(QtCore.QRect(430, 500, 65, 20))
        self.y_mouse_position.setText(_fromUtf8(""))
        self.y_mouse_position.setObjectName(_fromUtf8("y_mouse_position"))

        # self.x_position_label = QtGui.QLabel(self.centralwidget)
        # self.x_position_label.setGeometry(QtCore.QRect(80, 210, 65, 20))
        # self.x_position_label.setText(_fromUtf8(""))
        # self.x_position_label.setObjectName(_fromUtf8("x_position_label"))

        # self.y_position_label = QtGui.QLabel(self.centralwidget)
        # self.y_position_label.setGeometry(QtCore.QRect(80, 280, 65, 20))
        # self.y_position_label.setText(_fromUtf8(""))
        # self.y_position_label.setObjectName(_fromUtf8("y_position_label"))

        self.image_content = QtGui.QGraphicsView(self.centralwidget)
        self.image_content.setGeometry(QtCore.QRect(340, 0, 441, 501))
        self.image_content.setObjectName(_fromUtf8("image_content"))
        
        self.label2 = QtGui.QLabel(self.centralwidget)
        self.label2.setGeometry(QtCore.QRect(340,0,441,501))
        self.label2.setMouseTracking(True)

        self.glass = ClickableLabel(self.centralwidget)
        self.glass.setGeometry(QtCore.QRect(340,0,441,501))
        self.glass.setMouseTracking(True)
        self.glass.installEventFilter(self)

        self.runButton = QtGui.QPushButton(self.centralwidget)
        self.runButton.setGeometry(QtCore.QRect(80, 490, 94, 30))
        self.runButton.setObjectName(_fromUtf8("runButton"))
        self.runButton.clicked.connect(self.segmentIFT)

        self.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(self)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName(_fromUtf8("menubar"))

        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        self.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(self)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        self.setStatusBar(self.statusbar)

        self.actionOPen = QtGui.QAction(self)
        self.actionOPen.setObjectName(_fromUtf8("actionOPen"))
        self.actionOPen.setShortcut("Ctrl+O")
        self.actionOPen.triggered.connect(self.open_file)

        self.menuFile.addAction(self.actionOPen)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)
        
    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.runButton.setText(_translate("MainWindow", "Run", None))
        self.menuFile.setTitle(_translate("MainWindow", "FIle", None))
        self.actionOPen.setText(_translate("MainWindow", "Open", None))

    def open_file(self):
        name = QtGui.QFileDialog.getOpenFileName(self.centralwidget,"Open File", ".", "Image Files (*.bmp *.jpg *.png *.xpm *.jpeg *.pgm)")
        self.main_img = Image.open(str(name), "r")


        self.main_img_ift = io.imread(str(name))

    
        if self.main_img.mode == "L":
            self.main_img = self.main_img.convert("RGBA")
        elif self.main_img.mode == "LA":
            self.main_img = self.main_img.convert("RGBA")
        else:
            b , g, r = self.main_img.split()
            self.main_img = Image.merge("RGB", (r,g,b))

        data = self.main_img.convert("RGBA").tobytes("raw", "RGBA")
        qim = QtGui.QImage(data, self.main_img.size[0], self.main_img.size[1], QtGui.QImage.Format_ARGB32)
        pic = QtGui.QPixmap.fromImage(qim)
        self.label2.setPixmap(pic)
        
        
        
    
    def eventFilter(self, source, event):
        if(event.type() == QtCore.QEvent.MouseMove and source is self.glass):
            pos = event.pos()
            self.x_mouse_position.setText("X : %d" % pos.x())
            self.y_mouse_position.setText("Y : %d" % pos.y())
            # self.x_position_label.setText(str(self.glass.coord_object))
            # self.y_position_label.setText(str(self.glass.coord_bg))

        return QtGui.QMainWindow.eventFilter(self,source,event)

    def clearGlass(self):
        self.glass.clear()
        self.pic = QtGui.QPixmap("circle.png")
        self.pic.fill(QtCore.Qt.transparent)
        self.glass.setPixmap(self.pic)
        self.glass.coord_bg = []    
        self.glass.coord_object = []

    def segmentIFT(self):
        adj8 = [(0, 0), (-1,-1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1),
            (0, 1), (1, 1)]


        if not self.glass.coord_bg and not self.glass.coord_object:
            print "insira as coordenadas corretamente"
            sys.exit()
        else:

            obj_coord = []
            bg_coord = []

            # for i in range(249, 282):
            # #     for j in range(342, 372):
            # obj_coord.append((358,390))

            # # for i in range(297,377):
            # #     for j in range(139,248):
            # bg_coord.append((353,174))

            # print obj_coord

            # print "-----------------------"

            # print bg_coord

            for x, y in self.glass.coord_bg:
                print str(x) + " " + str(y) + " " + str(self.main_img_ift[x,y])


            print "----------------"

            for x, y in self.glass.coord_object:
                print str(x) + " " + str(y) + " " + str(self.main_img_ift[x,y])

            seg = ift.watershed(self.main_img_ift,self.glass.coord_object,self.glass.coord_bg)

            print "sucesso"

            io.imsave("seg.png", seg)
            pic = QtGui.QImage()
            load_pic = pic.load("seg", ".png")
            assert load_pic == True

            image_width = pic.width()
            image_height = pic.height()

            borders = []

            for y in range(0, image_height):
                for x in range(0, image_width):
                    for dx, dy in adj8:
                        ref = (x,y)

                        coord_x = x + dx
                        coord_y = y + dy

                        if coord_x < 0 or coord_x >= image_width:
                            continue

                        if coord_y < 0 or coord_y >= image_height:
                            continue



                        valueAdj = QtGui.qGray(pic.pixel(coord_x, coord_y))

                        valueRef = QtGui.qGray(pic.pixel(x,y))

                        if valueAdj != valueRef:
                            borders.append(ref)
            
            

            result_pic = QtGui.QImage()
            load_result_pic = result_pic.load("square2",".pgm")
            assert load_result_pic == True

            image_result_height = result_pic.height()
            image_result_width = result_pic.width()



            pix = self.glass.pixmap()
            imagem = pix.toImage()

            for x, y in borders:
                imagem.setPixel(x,y, QtGui.qRgb(255,0,0))

            for x,y in bg_coord:
                imagem.setPixel(x,y, QtGui.qRgb(0,0,255))

            for x,y in obj_coord:
                imagem.setPixel(x,y, QtGui.qRgb(0,0,255))

            image = QtGui.QPixmap.fromImage(imagem)
            self.glass.setPixmap(image)

    

        

if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    main = QtGui.QMainWindow()
    window = Window()
    window.show()
    window.resize(800,600)
    sys.exit(app.exec_())

