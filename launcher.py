from PyQt5 import QtCore, QtGui, QtWidgets
import time

from threading import Thread
from PyQt5.QtWidgets import QMainWindow, QLabel
from PyQt5.QtWidgets import QGridLayout, QWidget, QDesktopWidget
from pathlib import Path
import os
from subprocess import *
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from util import get_port
from port_manip import throw_port_json
import eel

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640,478)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(57, 80, 590, 301))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy)
        self.frame.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frame.setStyleSheet("background-color: rgb(None);\n"
"selection-color: rgb(0, 0, 0);\n"
"border-color: rgb(None);\n"
f"background-image: url('{Path.cwd()}/splash5.png');\n"
"background-repeat: no-repeat;\n" 
"background-position: center;\n")
        self.frame.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setLineWidth(0)
        self.frame.setObjectName("frame")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(60, 371, 700, 10))
        self.progressBar.setStyleSheet("background-color: rgb(None);\n"
"color: rgb(None);")
        self.progressBar.setProperty("value", 24)
        self.progressBar.setTextVisible(False)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())
        qtRectangle = MainWindow.frameGeometry()
        centerPoint = QDesktopWidget().availableGeometry().center()
        qtRectangle.moveCenter(centerPoint)
        MainWindow.move(qtRectangle.topLeft())
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        
        MainWindow.setWindowFlags(MainWindow.windowFlags() | QtCore.Qt.FramelessWindowHint)
        MainWindow.setAttribute(QtCore.Qt.WA_TranslucentBackground)

    def execute_function_threaded(self, func):
        """Run given function in thread"""
        self.t = Thread(target=func)
        self.t.start()
        print('thread started')

    def auto_close(self, n,MainWindow):
        """Close self in n seconds"""
        print('going to sleep')
        a=0
        for i in range(n):
            self.progressBar.setProperty("value", a)
            time.sleep(0.15)
            a+=1
        print('done sleeping!')
        MainWindow.close()
        call(["python3", f"{Path.cwd()}/main.py"])
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    # port = get_port()
    # throw_port_json(port)    
    ui.execute_function_threaded(func=lambda: ui.auto_close(100,MainWindow))
    # eel.start('web/mainpage.html', mode='custom', cmdline_args=['node_modules/electron/dist/electron', '.'], port=port)
    sys.exit(app.exec_())
