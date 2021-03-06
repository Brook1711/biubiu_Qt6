#! /usr/bin/python

#
# Qt example for VLC Python bindings
# Copyright (C) 2009-2010 the VideoLAN team
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston MA 02110-1301, USA.
#
import sys
import os.path, os
if sys.platform == "win32": 
    os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.16"

import vlc
from PySide6 import QtGui, QtCore
from PySide6.QtCore import Slot, Qt
from PySide6.QtGui import QAction, QPainter, QPainterPath, QPixmap

from PySide6.QtWidgets import QLayout, QMainWindow, QApplication, QSplitter, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QGroupBox, QLabel 

try:
    unicode        # Python 2
except NameError:
    unicode = str  # Python 3

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
        
class Player(QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QMainWindow.__init__(self, master)
        self.setWindowTitle("biubiu Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()
        self.isPaused = False

    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QSplitter(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            # self.videoframe = QtGui.QMacCocoaViewContainer(0)
            self.videoframe = QFrame()
        else:
            self.videoframe = QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        self.positionslider = QSlider(QtCore.Qt.Horizontal, self)
        self.positionslider.setToolTip("Position")
        self.positionslider.setMaximum(1000)
        self.positionslider.sliderMoved.connect(self.setPosition)
        # self.connect(self.positionslider,
                    #  QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        self.hbuttonbox = QHBoxLayout()
        self.playbutton = QPushButton("Play")
        self.hbuttonbox.addWidget(self.playbutton)
        self.playbutton.clicked.connect(self.PlayPause)
        # self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
                    #  self.PlayPause)

        self.stopbutton = QPushButton("Stop")
        self.hbuttonbox.addWidget(self.stopbutton)
        self.stopbutton.clicked.connect(self.Stop)
        # self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
                    #  self.Stop)

        self.hbuttonbox.addStretch(1)
        self.volumeslider = QSlider(QtCore.Qt.Horizontal, self)
        self.volumeslider.setMaximum(100)
        self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        self.volumeslider.setToolTip("Volume")
        self.hbuttonbox.addWidget(self.volumeslider)
        self.volumeslider.valueChanged.connect(self.setVolume)
        # self.connect(self.volumeslider,
                    #  QtCore.SIGNAL("valueChanged(int)"),
                    #  self.setVolume)
        # ** add right sidebar
        self.right_layout = QVBoxLayout()
        # edit the content in right sidebar

        self.test_btn = QPushButton()
        ## currently empty
        self.user_info = UserInfo()
        self.right_layout.addWidget(self.user_info)
        self.right_layout.addStretch(10)
        
        # self.right_layout.setSpacing(20)
        # self.right_layout.SetFixedSize()
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setFixedWidth(400)
        # ** end right sidebar

        # ** add left play zone (video box)
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.vboxlayout.addWidget(self.positionslider)
        self.vboxlayout.addLayout(self.hbuttonbox)
        self.left_widget = QWidget()
        self.left_widget.setLayout(self.vboxlayout)
        # ** end left play zone

        # ** add left and right widget
        
        # self.main_layout = QHBoxLayout()
        # self.main_layout.addWidget(self.left_widget)
        # self.main_layout.addWidget(self.right_widget)
        self.widget.addWidget(self.left_widget)
        self.widget.addWidget(self.right_widget)
        self.widget.setStretchFactor(3, 4)
        # self.widget.setSizes([500, 250])
        open = QAction("&Open", self)
        open.triggered.connect(self.OpenFile)
        # self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        exit = QAction("&Exit", self)
        exit.triggered.connect(sys.exit)
        # self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        menubar = self.menuBar()
        filemenu = menubar.addMenu("&File")
        filemenu.addAction(open)
        filemenu.addSeparator()
        filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.updateUI)
        # self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                    #  self.updateUI)
    @Slot()
    def PlayPause(self):
        """Toggle play/pause status
        """
        if self.mediaplayer.is_playing():
            self.mediaplayer.pause()
            self.playbutton.setText("Play")
            self.isPaused = True
        else:
            if self.mediaplayer.play() == -1:
                self.OpenFile()
                return
            self.mediaplayer.play()
            self.playbutton.setText("Pause")
            self.timer.start()
            self.isPaused = False
    @Slot()
    def Stop(self):
        """Stop player
        """
        self.mediaplayer.stop()
        self.playbutton.setText("Play")
    @Slot()
    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename[0])
        # put the media in the media player
        self.mediaplayer.set_media(self.media)

        # parse the metadata of the file
        self.media.parse()
        # set the title of the track as window title
        self.setWindowTitle(self.media.get_meta(0))

        # the media player has to be 'connected' to the QFrame
        # (otherwise a video would be displayed in it's own window)
        # this is platform specific!
        # you have to give the id of the QFrame (or similar object) to
        # vlc, different platforms have different functions for this
        if sys.platform.startswith('linux'): # for Linux using the X Server
            self.mediaplayer.set_xwindow(self.videoframe.winId())
        elif sys.platform == "win32": # for Windows
            self.mediaplayer.set_hwnd(self.videoframe.winId())
        elif sys.platform == "darwin": # for MacOS
            self.mediaplayer.set_nsobject(self.videoframe.winId())
        self.PlayPause()
    @Slot()
    def setVolume(self, Volume):
        """Set the volume
        """
        self.mediaplayer.audio_set_volume(Volume)
    
    @Slot()
    def setPosition(self, position):
        """Set the position
        """
        # setting the position to where the slider was dragged
        self.mediaplayer.set_position(position / 1000.0)
        # the vlc MediaPlayer needs a float value between 0 and 1, Qt
        # uses integer variables, so you need a factor; the higher the
        # factor, the more precise are the results
        # (1000 should be enough)
    @Slot()
    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            self.timer.stop()
            if not self.isPaused:
                # after the video finished, the play button stills shows
                # "Pause", not the desired behavior of a media player
                # this will fix it
                self.Stop()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = Player()
    player.show()
    player.resize(640, 480)
    if sys.argv[1:]:
        player.OpenFile(sys.argv[1])
    sys.exit(app.exec_())