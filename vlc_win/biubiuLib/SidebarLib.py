import sys
import os.path, os
if sys.platform == "win32": 
    os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.16"
import time
import vlc
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QPainter, QPainterPath, QPixmap

from PySide6.QtWidgets import QLayout, QMainWindow, QApplication, QScrollArea, QSplitter, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QGroupBox, QLabel, QScrollArea

class Comment(QGroupBox):
    def __init__(self, parent=None):
        super(Comment, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setFixedWidth(380)
        self.setFixedHeight(100)
        self.user_name = QLabel("用户名称")
        self.user_comment = QLabel("评论内容")
        self.layout.addWidget(self.user_name)
        self.layout.addWidget(self.user_comment)
        self.setLayout(self.layout)


class CommentArea(QScrollArea):
    def __init__(self, parent=None):
        super(CommentArea, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.widget = QWidget()
        # self.layout = QVBoxLayout()
        self.widget.setFixedWidth(400)
        # self.widget.setFixedHeight(600)
        for i in range(20):
            comment = Comment()
            self.layout.addWidget(comment)
        self.widget.setLayout(self.layout)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setWidgetResizable(True)
        self.setWidget(self.widget)

class VideoInfo(QGroupBox):
    def __init__(self, parent=None):
        super(VideoInfo, self).__init__(parent)
        self.layout = QVBoxLayout()
        self.setFixedWidth(400)
        # self.setFixedHeight(200)
        self.text1_widget=QLabel("视频标题")
        self.text2_widget=QLabel("视频格式")
        self.text3_widget=QLabel("视频时长")
        self.text1_widget.setWordWrap(True)
        self.text2_widget.setWordWrap(True)
        self.text3_widget.setWordWrap(True)
        self.layout.addWidget(self.text1_widget)
        self.layout.addWidget(self.text2_widget)
        self.layout.addWidget(self.text3_widget)
        self.setLayout(self.layout)

class UserInfo(QGroupBox):

    def __init__(self, parent=None):
        super(UserInfo, self).__init__(parent)
        self.col = QHBoxLayout()
        # Create widgets
        self.setFixedWidth(400)
        self.setFixedHeight(200)
        self.radius = 50
        self.Antialiasing=True

        #####################核心实现#########################
        
        self.ico = QLabel()
        self.ico.setMaximumSize(2*self.radius, 2*self.radius)
        self.ico.setMinimumSize(2*self.radius, 2*self.radius)
        self.target = QPixmap(self.ico.size())  # 大小和控件一样
        self.target.fill(Qt.transparent)  # 填充背景为透明

        p = QPixmap("1.ico").scaled(  # 加载图片并缩放和控件一样大
            2*self.radius, 2*self.radius, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation)

        painter = QPainter(self.target)
        if self.Antialiasing:
            # 抗锯齿
            painter.setRenderHint(QPainter.Antialiasing, True)
            # painter.setRenderHint(QPainter.HighQualityAntialiasing, True) # can not execute under Qt6
            painter.setRenderHint(QPainter.SmoothPixmapTransform, True)

        #         painter.setPen(# 测试圆圈
        #             QPen(Qt.red, 5, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
        path = QPainterPath()
        path.addRoundedRect(
            0, 0, self.ico.width(), self.ico.height(), self.radius, self.radius)
        # **** 切割为圆形 ****#
        painter.setClipPath(path)
        #         painter.drawPath(path)  # 测试圆圈

        painter.drawPixmap(0, 0, p)
        self.ico.setPixmap(self.target)
        #####################核心实现#########################
        #####################头像右边文字#####################
        self.user_text_layout = QVBoxLayout()
        self.text1_widget = QLabel("用户名称")
        self.text2_widget = QLabel("用户状态")
        self.user_text_layout.addWidget(self.text1_widget)
        self.user_text_layout.addWidget(self.text2_widget)
        #####################头像右边文字#####################
        self.col.addWidget(self.ico)
        self.col.addLayout(self.user_text_layout)
        self.setLayout(self.col)
        