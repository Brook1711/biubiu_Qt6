# biubiu_Qt6
biubiu project by Qt6

终于，向浏览器恶势力低头了

QT官网教程解读 [官网链接](https://doc.qt.io/qtforpython-6/tutorials/index.html#before-you-start)

tk+vlc代码参考：[git.videolan.org Git - vlc/bindings/python.git/blob - examples/tkvlc.py](https://git.videolan.org/?p=vlc/bindings/python.git;a=blob;f=examples/tkvlc.py;h=9984138afa37132ad1279e55d66eb7b705e21b98;hb=HEAD)

vlc dll参考：[Python 流媒体播放器（基于VLC）_血色@残阳的专栏-CSDN博客_python vlc](https://blog.csdn.net/yingshukun/article/details/89527561)

vlc 源码：[Index of /pub/videolan/vlc/last/win64/](http://download.videolan.org/pub/videolan/vlc/last/win64/)

exe打包二进制：pyinstaller

Pyinstaller -F -i 1.ico tkvlc.py
Pyinstaller -F -i 1.ico qt_vlc.py


Mac:py2app

py2applet --make-setup main.py

python3 setup.py py2app -A


pyinstaller --windowed --onefile --clean --noconfirm main.py
pyinstaller --clean --noconfirm --windowed --onefile main.spec

pip install cx_Freeze

## 结构规划

![image-20210830131306464](README.assets/image-20210830131306464.png)

评论和弹幕出现之前：

![image-20210830132434263](README.assets/image-20210830132434263.png)

## 基于vlc

运行时保证vlc库与可执行文件位于同一个目录下

![image-20210830130140110](README.assets/image-20210830130140110.png)

## Qt窗口类型
https://www.cnblogs.com/laizhenghong2012/p/10085089.html

![image-20210830121834596](README.assets/image-20210830121834596.png)

