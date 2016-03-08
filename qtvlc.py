#! /usr/bin/python

import sys
import os.path
import vlc
import time
import serial
import getopt
import os
import glob
import datetime
import socket
from time import sleep
from PyQt4 import QtGui, QtCore

class NetworkManager():
    
    def __init__(self):
        self.HOST, self.PORT = "127.0.0.1", 45454
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def sendStart(self):
        self.sock.sendto("start\n", (self.HOST,self.PORT))

    def sendStop(self):
        self.sock.sendto("stop\n", (self.HOST,self.PORT))

    def sendExit(self):
        self.sock.sendto("exit\n", (self.HOST,self.PORT))

class Player(QtGui.QMainWindow):
    """A simple Media Player using VLC and Qt
    """
    def __init__(self, master=None):
        QtGui.QMainWindow.__init__(self, master)
        self.setWindowTitle("Media Player")

        # creating a basic vlc instance
        self.instance = vlc.Instance()
        # creating an empty vlc media player
        self.mediaplayer = self.instance.media_player_new()

        self.createUI()


    def createUI(self):
        """Set up the user interface, signals & slots
        """
        self.widget = QtGui.QWidget(self)
        self.setCentralWidget(self.widget)

        # In this widget, the video will be drawn
        if sys.platform == "darwin": # for MacOS
            self.videoframe = QtGui.QMacCocoaViewContainer(0)
        else:
            self.videoframe = QtGui.QFrame()
        self.palette = self.videoframe.palette()
        self.palette.setColor (QtGui.QPalette.Window,
                               QtGui.QColor(0,0,0))
        self.videoframe.setPalette(self.palette)
        self.videoframe.setAutoFillBackground(True)

        #self.positionslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        #self.positionslider.setToolTip("Position")
        #self.positionslider.setMaximum(1000)
        #self.connect(self.positionslider,
        #             QtCore.SIGNAL("sliderMoved(int)"), self.setPosition)

        #self.hbuttonbox = QtGui.QHBoxLayout()
        #self.playbutton = QtGui.QPushButton("Play")
        #self.hbuttonbox.addWidget(self.playbutton)
        #self.connect(self.playbutton, QtCore.SIGNAL("clicked()"),
        #             self.PlayPause)

        #self.stopbutton = QtGui.QPushButton("Stop")
        #self.hbuttonbox.addWidget(self.stopbutton)
        #self.connect(self.stopbutton, QtCore.SIGNAL("clicked()"),
        #             self.Stop)

        #self.hbuttonbox.addStretch(1)
        #self.volumeslider = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        #self.volumeslider.setMaximum(100)
        #self.volumeslider.setValue(self.mediaplayer.audio_get_volume())
        #self.volumeslider.setToolTip("Volume")
        #self.hbuttonbox.addWidget(self.volumeslider)
        #self.connect(self.volumeslider,
        #             QtCore.SIGNAL("valueChanged(int)"),
        #             self.setVolume)

        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        #self.vboxlayout.addWidget(self.positionslider)
        #self.vboxlayout.addLayout(self.hbuttonbox)

        self.widget.setLayout(self.vboxlayout)

        #open = QtGui.QAction("&Open", self)
        #self.connect(open, QtCore.SIGNAL("triggered()"), self.OpenFile)
        #exit = QtGui.QAction("&Exit", self)
        #self.connect(exit, QtCore.SIGNAL("triggered()"), sys.exit)
        #menubar = self.menuBar()
        #filemenu = menubar.addMenu("&File")
        #filemenu.addAction(open)
        #filemenu.addSeparator()
        #filemenu.addAction(exit)

        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(200)
        self.connect(self.timer, QtCore.SIGNAL("timeout()"),
                     self.updateUI)

    def PlayPause(self):
        """Toggle play/pause status
        """
        self.mediaplayer.play()
        self.timer.start()

    def OpenFile(self, filename=None):
        """Open a media file in a MediaPlayer
        """
        if filename is None:
            filename = QtGui.QFileDialog.getOpenFileName(self, "Open File", os.path.expanduser('~'))
        if not filename:
            return

        # create the media
        if sys.version < '3':
            filename = unicode(filename)
        self.media = self.instance.media_new(filename)
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
        NM.sendStart()

    def updateUI(self):
        """updates the user interface"""
        # setting the slider to the desired position
        #self.positionslider.setValue(self.mediaplayer.get_position() * 1000)

        if not self.mediaplayer.is_playing():
            # no need to call this function if nothing is played
            #self.timer.stop()
            self.timer.stop()
            NM.sendStop()
            NM.sendExit()
            time.sleep(0)
            self.close()
            QtGui.QAction("&Exit", self)
            QtCore.QCoreApplication.instance().quit()
            sys.exit(0)



if __name__ == "__main__":

    videoFile = sys.argv[1] 
    NM = NetworkManager()

    app = QtGui.QApplication(sys.argv)
    player = Player()

    player.show()
    player.resize(640, 480)
    player.OpenFile(videoFile)
    player.timer.start()
    #player.OpenFile('./Ext.mp4')

    
    sys.exit(app.exec_())
