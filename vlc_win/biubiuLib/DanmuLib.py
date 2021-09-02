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