import sys
import os.path, os
if sys.platform == "win32": 
    os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.16"
import time
import vlc
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Slot, Qt, QPoint, QEasingCurve, QPropertyAnimation
from PySide6.QtGui import QAction, QPainter, QPainterPath, QPixmap, QFont, QPalette, QColor
from PySide6.QtWidgets import QLayout, QMainWindow, QApplication, QScrollArea, QSplitter, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QGroupBox, QLabel, QScrollArea, QGridLayout
'''
class Danmu(QLabel):
    font = QFont('SimHei',20,100)
    pe = QPalette()  
    pe.setColor(QPalette.WindowText,Qt.white)
    pe.setColor(QPalette.Window,Qt.red)
    def __init__(self,parent,text="弹幕测试文字",y=200,color=QColor(255,255,255)):
        super().__init__(text,parent)
        
        self.text = text
        self.parent = parent
        self.setFont(self.font)

        self.posY = y
        self.color = color
        self.setPalette(self.pe)

        self.anim2 = QPropertyAnimation(self,b'pos')
        self.anim2.setDuration(10000)
        self.anim2.setStartValue(QPoint(2000,self.posY))
        self.anim2.setEndValue(QPoint(0,self.posY))
        self.anim2.setEasingCurve(QEasingCurve.Linear)
        # self.setStyleSheet("background:transparent")
        self.anim2.start()
'''
class Danmu(QLabel):

    def __init__(self, parent=None):
        
        super(Danmu, self).__init__(parent)

        self.text = "弹幕测试文字"
        self.setText(self.text)
        self.anim2 = QPropertyAnimation(self,b'pos')
        self.anim2.setDuration(10000)
        self.anim2.setStartValue(QPoint(2000,50))
        self.anim2.setEndValue(QPoint(-50,50))
        self.anim2.setEasingCurve(QEasingCurve.Linear)
        # self.setStyleSheet("background:transparent")
        self.anim2.finished.connect(self.anim_finished)
        self.anim2.start()
        
    def anim_finished(self):
        self.deleteLater()
    

class DanmuPool():
    def __init__(self, parent, server={}) -> None:
        danmu_test = Danmu(parent=parent)
        danmu_test.show()
        pass

class DanmuZone(QWidget):
    def __init__(self, parent=None) -> None:
        super(DanmuZone, self).__init__(parent)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)

        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)   # 设置页边距
        layout.setSpacing(0)