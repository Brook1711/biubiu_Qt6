from PyQt5 import QtCore, QtGui, QtWidgets

class ControlBar(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        self.slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
        layout.addWidget(self.slider)
        buttons = QtWidgets.QHBoxLayout()
        layout.addLayout(buttons)
        buttons.addWidget(QtWidgets.QToolButton(text='play'))
        buttons.addWidget(QtWidgets.QToolButton(text='stop'))
        buttons.addStretch()


class VolumeWidget(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 0)
        layout.setSpacing(1)
        handle = QtWidgets.QFrame()
        handle.setFixedHeight(12)
        handle.setStyleSheet('''
            QFrame {
                border: 1px solid darkGray;
                border-radius: 2px;
                background: #aa646464;
            }
        ''')
        layout.addWidget(handle)
        volumeLayout = QtWidgets.QHBoxLayout()
        layout.addLayout(volumeLayout)
        for i in range(4):
            volumeLayout.addWidget(QtWidgets.QSlider(QtCore.Qt.Vertical))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.startPos = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            delta = event.pos() - self.startPos
            self.move(self.pos() + delta)


class Notification(QtWidgets.QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        self.label = QtWidgets.QLabel('Notification', alignment=QtCore.Qt.AlignCenter)
        layout.addWidget(self.label)


class PlayerWidget(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.video = QtWidgets.QLabel(self)
        self.video.setPixmap(QtGui.QPixmap('movie.png'))
        self.video.setScaledContents(True)
        self.controlBar = ControlBar(self)
        self.notification = Notification(self)
        self.volumeWidget = VolumeWidget(self)
        self.volumeWidget.move(30, 30)

        self.setStyleSheet('''
            VolumeWidget, ControlBar {
                border: 1px outset darkGray;
                border-radius: 4px;
                background: #aad3d3d3;
            }
            VolumeWidget:hover, ControlBar:hover {
                background: #d3d3d3;
            }
            Notification {
                border: 1px outset darkGray;
                border-radius: 4px;
                background: #aa242424;
            }
            Notification QLabel {
                color: white;
            }
        ''')

    def sizeHint(self):
        if self.video.pixmap() and not self.video.pixmap().isNull():
            return self.video.pixmap().size()
        return QtCore.QSize(640, 480)

    def resizeEvent(self, event):
        # set the geometry of the "video"
        videoRect = QtCore.QRect(
            QtCore.QPoint(), 
            self.video.sizeHint().scaled(self.size(), QtCore.Qt.KeepAspectRatio))
        videoRect.moveCenter(self.rect().center())
        self.video.setGeometry(videoRect)

        # control panel
        controlHeight = self.controlBar.sizeHint().height()
        controlRect = QtCore.QRect(0, self.height() - controlHeight, 
            self.width(), controlHeight)
        self.controlBar.setGeometry(controlRect)

        # notification
        notificationWidth = max(self.notification.sizeHint().width(), self.width() * .6)
        notificationRect = QtCore.QRect(
            (self.width() - notificationWidth) * .5, 20, 
            notificationWidth, self.notification.sizeHint().height()
        )
        self.notification.setGeometry(notificationRect)

    def paintEvent(self, event):
        qp = QtGui.QPainter(self)
        qp.fillRect(self.rect(), QtCore.Qt.black)