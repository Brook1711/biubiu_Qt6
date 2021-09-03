import sys
import os.path, os
if sys.platform == "win32": 
    os.environ['PYTHON_VLC_MODULE_PATH'] = "./vlc-3.0.16"
import time
import vlc
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QPoint, Slot, Qt, QPropertyAnimation, QEasingCurve
from PySide6.QtGui import QAction, QPainter, QPainterPath, QPixmap,QFont

from PySide6.QtWidgets import QLayout, QMainWindow, QApplication, QScrollArea, QSplitter, QTextBrowser, QWidget, QFrame, QSlider, QHBoxLayout, QPushButton, QVBoxLayout, QFileDialog, QGroupBox, QLabel, QScrollArea, QGridLayout

from biubiuLib.SidebarLib import CommentArea, UserInfo, VideoInfo
from biubiuLib.DanmuLib import Danmu, DanmuPool, DanmuZone

class TextBrowser(QWidget):

    def __init__(self, parent):
        super(TextBrowser, self).__init__(parent)
        self.setWindowTitle('弹幕机')
        # self.setWindowFlags()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Tool)
        # self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        # self.setWindowOpacity(0.1)
        self.setFixedHeight(400)
        self.setFixedWidth(400)
        layout = QGridLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.textBrowser = QTextBrowser(        )
        self.textBrowser.setFont(QFont('Microsoft JhengHei', 14, QFont.Bold))
        
        # self.textBrowser.setStyleSheet("background:transparent")
        layout.addWidget(self.textBrowser, 1, 0, 1, 10)
        self.textBrowser.setText("<h1>hello</h1>\n<h1>hello</h1>\n<h1>hello</h1>")
        self.textBrowser.setStyleSheet("background:transparent;border-width:0;border-style:outset")
        self.textBrowser.setAutoFillBackground(False)
        self.textBrowser.setFixedHeight(200)




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
        self.video_zone = QFrame()
        self.videoframe = QFrame()
        self.danmu_zone = DanmuZone(self.video_zone)
        self.videoframe.setParent(self.video_zone)
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               Qt.transparent)
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)
        # self.video_zone.show()
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
        self.video_info = VideoInfo()
        self.right_layout.addWidget(self.video_info)
        self.comment_aera = CommentArea()
        self.right_layout.addWidget(self.comment_aera)
        # self.right_layout.addStretch(10)
        
        # self.right_layout.setSpacing(20)
        # self.right_layout.SetFixedSize()
        self.right_widget = QWidget()
        self.right_widget.setLayout(self.right_layout)
        self.right_widget.setFixedWidth(400)
        # ** end right sidebar

        # ** add left play zone (video box)
        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.video_zone)
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
        self.video_info.text1_widget.setText("视频标题为："+self.media.get_meta(0)) 
        self.video_info.text3_widget.setText(("视频时长为："+str(self.media.get_duration())+"s"))
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
        time.sleep(1)
        self.video_info.text2_widget.setText('视频音频情况：'+str([(i[0], i[1].decode()) for i in self.mediaplayer.audio_get_track_description()])+"\n可用字幕"+str([(i[0], i[1].decode()) for i in self.mediaplayer.video_get_spu_description()]))
        danmu_test = QLabel("<h1>danmu</h1>")
        danmu_test.setParent(self.danmu_zone)
        anim2 = QPropertyAnimation(danmu_test,b'pos', self.danmu_zone)
        anim2.setDuration(20000)
        anim2.setStartValue(QPoint(1000,50))
        anim2.setEndValue(QPoint(-50,50))
        anim2.setEasingCurve(QEasingCurve.Linear)
        self.danmu_zone.show()
        anim2.start()
        self.danmu_zone.setStyleSheet("background:transparent;border-width:0;border-style:outset")


        
        

        
        
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
    def moveEvent(self, event: QtGui.QMoveEvent) -> None:
        ## target danmu_zone position
        videoPos = self.mapToGlobal(self.videoframe.pos())
        self.danmu_zone.move(videoPos)
        # print(videoPos)
        return super().moveEvent(event)

    def resizeEvent(self, event: QtGui.QResizeEvent) -> None:
        
        ## target danmu_zone size
        # print(self.video_zone.width(), self.video_zone.height())
        self.videoframe.resize(self.video_zone.width(),self.video_zone.height())
        self.danmu_zone.resize(self.video_zone.width(),self.video_zone.height())
        return super().resizeEvent(event)