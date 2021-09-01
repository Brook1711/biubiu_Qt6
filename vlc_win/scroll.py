from PyQt5.QtWidgets import (QWidget, QSlider, QLineEdit, QLabel, QPushButton, QScrollArea,QApplication,
                             QHBoxLayout, QVBoxLayout, QMainWindow, QGroupBox)
from PyQt5.QtCore import Qt, QSize
from PyQt5 import QtWidgets, uic

import sys

class Comment(QGroupBox):
    def __init__(self, parent=None):
        super(Comment, self).__init__(parent)
        self.layout = QVBoxLayout()
        # self.setFixedWidth(380)
        # self.setFixedHeight(100)
        self.user_name = QLabel("用户名称")
        self.user_comment = QLabel("评论内容")
        self.layout.addWidget(self.user_name)
        self.layout.addWidget(self.user_comment)
        self.setLayout(self.layout)


class CommentArea(QWidget):
    def __init__(self, parent=None):
        super(CommentArea, self).__init__(parent)
        self.layout = QVBoxLayout()
        # self.layout = QVBoxLayout()
        # self.setFixedWidth(400)
        # self.setFixedHeight(600)
        # self.setMaximumHeight(600)
        self.comment_list = []
        for i in range(20):
            comment = Comment()
            self.layout.addWidget(QLabel('test'))
        self.setLayout(self.layout)
        self.scroll = QScrollArea() 
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self)

class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.scroll = QScrollArea()             # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()                 # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()               # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        for i in range(1,50):
            # object = Comment()
            object = QLabel('test')
            self.vbox.addWidget(object)

        self.widget.setLayout(self.vbox)

        #Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)

        self.setCentralWidget(self.widget)

        self.setGeometry(600, 100, 1000, 900)
        self.setWindowTitle('Scroll Area Demonstration')
        self.show()

        return

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = MainWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()