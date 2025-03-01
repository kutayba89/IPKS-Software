import sys
import json
import shlex
import threading
import subprocess
import webbrowser
from QLed import QLed
from functools import partial
from PyQt5.QtGui import QColor,QFont
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtGui import QPainter, QPen
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QMainWindow
from PyQt5 import QtCore, QtGui, QtWidgets, QtMultimedia, QtMultimediaWidgets
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication,QGridLayout, QLCDNumber)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLCDNumber


class MainProg(QtWidgets.QMainWindow):
    def __init__(self, parent=None):


        super(MainProg, self).__init__(parent)

        self.setObjectName("MainWindow")

        self.setFixedSize(1366, 768)

        self.setStyleSheet("")

        icon = QtGui.QIcon()
        # icon.addPixmap(QtGui.QPixmap("/home/kikomii/Desktop/index.png"),QtGui.QIcon.Normal,QtGui.QIcon.on)
        self.setWindowIcon(icon)

        self.setWindowTitle("Software as IP Based Crossbar ( IP Basierte Kreuzschiene )DVB Playout Stream")
        #################              The LEDs              ########################################################
        self.TPL1 = QLed(self, onColour=QLed.Orange, shape=QLed.Round)
        self.TPL1.setGeometry(QtCore.QRect(120, 548, 35, 25))
        #self.TPL1.value = False

        self.TPL2 = QLed(self, onColour=QLed.Orange, shape=QLed.Round)
        self.TPL2.setGeometry(QtCore.QRect(120, 678, 35, 25))
        #self.TPL2.value = False

        self.TPL3 = QLed(self, onColour=QLed.Orange, shape=QLed.Round)
        self.TPL3.setGeometry(QtCore.QRect(380, 568, 35, 25))
        #self.TPL3.value = False

        self.TPL4 = QLed(self, onColour=QLed.Orange, shape=QLed.Round)
        self.TPL4.setGeometry(QtCore.QRect(380, 688, 35, 25))
        #self.TPL4.value = False


        ############### LCD frame
        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(1090, 410, 241, 291))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        ###################Video LCDS##################

        self.V_lcd7 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd7.setGeometry(QtCore.QRect(100, 250, 81, 31))
        self.V_lcd7.setObjectName("V_Bitrate")
        self.V_lcd5 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd5.setGeometry(QtCore.QRect(100, 170, 81, 31))
        self.V_lcd5.setObjectName("V_Disratio")
        self.V_lcd4 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd4.setGeometry(QtCore.QRect(100, 130, 81, 31))
        self.V_lcd4.setObjectName("V_Width")
        self.V_lcd2 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd2.setGeometry(QtCore.QRect(100, 50, 81, 31))
        self.V_lcd2.setObjectName("V_Codname")
        self.V_lcd3 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd3.setGeometry(QtCore.QRect(100, 90, 81, 31))
        self.V_lcd3.setObjectName("V_High")
        self.V_lcd1 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd1.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.V_lcd1.setObjectName("V_Indx")
        self.V_lcd6 = QtWidgets.QLCDNumber(self.frame)
        self.V_lcd6.setGeometry(QtCore.QRect(100, 210, 81, 31))
        self.V_lcd6.setObjectName("V_Ref")
        ##############################################################

        self.progressbar = QtWidgets.QProgressBar(self)
        self.progressbar.setGeometry(QtCore.QRect(1010, 710, 118, 23))
        # self.progressbar.setProperty("value", 24)
        # self.progressbar.setObjectName("progressbar")
        #################THe Scraaap#################################

        self.SW1L = QtWidgets.QToolButton(self)
        self.SW1L.setEnabled(False)
        self.SW1L.setGeometry(QtCore.QRect(250, 400, 21, 321))
        self.SW1L.setStyleSheet("")
        self.SW1L.setText("")
        self.SW1L.setObjectName("SW1L")
        self.SW1R = QtWidgets.QToolButton(self)
        self.SW1R.setEnabled(False)
        self.SW1R.setGeometry(QtCore.QRect(660, 400, 21, 321))
        self.SW1R.setStyleSheet("")
        self.SW1R.setText("")
        self.SW1R.setObjectName("SW1R")
        self.SW2R = QtWidgets.QToolButton(self)
        self.SW2R.setEnabled(False)
        self.SW2R.setGeometry(QtCore.QRect(610, 440, 21, 281))
        self.SW2R.setStyleSheet("")
        self.SW2R.setText("")
        self.SW2R.setObjectName("SW2R")
        self.SW2L = QtWidgets.QToolButton(self)
        self.SW2L.setEnabled(False)
        self.SW2L.setGeometry(QtCore.QRect(300, 440, 21, 281))
        self.SW2L.setStyleSheet("")
        self.SW2L.setText("")
        self.SW2L.setObjectName("SW2L")
        self.SW2up = QtWidgets.QToolButton(self)
        self.SW2up.setEnabled(True)
        self.SW2up.setGeometry(QtCore.QRect(300, 440, 331, 31))
        self.SW2up.setStyleSheet("")
        self.SW2up.setObjectName("SW2up")

        self.EncMain = QtWidgets.QToolButton(self)
        self.EncMain.setGeometry(QtCore.QRect(100, 460, 71, 111))
        self.EncMain.setObjectName("EncMain")
        self.EncBack = QtWidgets.QToolButton(self)
        self.EncBack.setGeometry(QtCore.QRect(100, 590, 71, 111))
        self.EncBack.setObjectName("EncBack")
        self.Muxmain = QtWidgets.QToolButton(self)
        self.Muxmain.setGeometry(QtCore.QRect(360, 480, 71, 111))
        self.Muxmain.setObjectName("Muxmain")
        self.MuxBack = QtWidgets.QToolButton(self)
        self.MuxBack.setGeometry(QtCore.QRect(360, 600, 71, 111))
        self.MuxBack.setObjectName("MuxBack")


        self.Testpunk1 = QtWidgets.QPushButton(self)
        self.Testpunk1.setGeometry(QtCore.QRect(190, 460, 31, 31))
        self.Testpunk1.setObjectName("TP1")
          ###TP1

        self.Testpunk2 = QtWidgets.QPushButton(self)
        self.Testpunk2.setGeometry(QtCore.QRect(190, 530, 31, 31))
        self.Testpunk2.setObjectName("TP2")
        self.Testpunk3 = QtWidgets.QPushButton(self)
        self.Testpunk3.setGeometry(QtCore.QRect(190, 590, 31, 31))
        self.Testpunk3.setObjectName("TP3")
        self.Testpunk4 = QtWidgets.QPushButton(self)
        self.Testpunk4.setGeometry(QtCore.QRect(190, 670, 31, 31))
        self.Testpunk4.setObjectName("TP4")
        self.Testpunk5 = QtWidgets.QPushButton(self)
        self.Testpunk5.setGeometry(QtCore.QRect(440, 490, 31, 31))
        self.Testpunk5.setObjectName("TP5")
        self.Testpunk6 = QtWidgets.QPushButton(self)
        self.Testpunk6.setGeometry(QtCore.QRect(440, 550, 31, 31))
        self.Testpunk6.setObjectName("TP6")
        self.Testpunk7 = QtWidgets.QPushButton(self)
        self.Testpunk7.setGeometry(QtCore.QRect(440, 610, 31, 31))
        self.Testpunk7.setObjectName("TP7")
        self.Testpunk8 = QtWidgets.QPushButton(self)
        self.Testpunk8.setGeometry(QtCore.QRect(440, 670, 31, 31))
        self.Testpunk8.setObjectName("TP8")


        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(220, 470, 31, 16))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(220, 540, 81, 16))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(220, 600, 31, 16))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setGeometry(QtCore.QRect(220, 680, 81, 16))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.EncFram = QtWidgets.QFrame(self)
        self.EncFram.setGeometry(QtCore.QRect(90, 440, 161, 281))
        self.EncFram.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.EncFram.setFrameShadow(QtWidgets.QFrame.Raised)
        self.EncFram.setObjectName("EncFram")
        self.line_5 = QtWidgets.QFrame(self)
        self.line_5.setGeometry(QtCore.QRect(470, 500, 141, 16))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self)
        self.line_6.setGeometry(QtCore.QRect(470, 560, 191, 16))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self)
        self.line_7.setGeometry(QtCore.QRect(470, 680, 191, 16))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self)
        self.line_8.setGeometry(QtCore.QRect(470, 620, 141, 16))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.SW2up_2 = QtWidgets.QToolButton(self)
        self.SW2up_2.setEnabled(True)
        self.SW2up_2.setGeometry(QtCore.QRect(250, 400, 431, 31))
        self.SW2up_2.setStyleSheet("")
        self.SW2up_2.setObjectName("SW2up_2")





        self.VidLb = QtWidgets.QLabel(self)
        self.VidLb.setGeometry(QtCore.QRect(1200, 390, 67, 17))
        self.VidLb.setObjectName("VidLb")
        self.VidL = QtWidgets.QLabel(self)
        self.VidL.setGeometry(QtCore.QRect(930, 390, 67, 17))
        self.VidL.setObjectName("VidL")
        self.frame_2 = QtWidgets.QFrame(self)
        self.frame_2.setGeometry(QtCore.QRect(810, 410, 241, 291))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        ################# AUDIO  LCDs##############
        self.A_lcd7 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd7.setGeometry(QtCore.QRect(100, 250, 81, 31))
        self.A_lcd7.setObjectName("A_Bitrate")
        self.A_lcd5 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd5.setGeometry(QtCore.QRect(100, 170, 81, 31))
        self.A_lcd5.setObjectName("A_Samrate")
        self.A_lcd4 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd4.setGeometry(QtCore.QRect(100, 130, 81, 31))
        self.A_lcd4.setObjectName("A_CodeTag")
        self.A_lcd2 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd2.setGeometry(QtCore.QRect(100, 50, 81, 31))
        self.A_lcd2.setObjectName("A_CodNm")
        self.A_lcd3 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd3.setGeometry(QtCore.QRect(100, 90, 81, 31))
        self.A_lcd3.setObjectName("A_Ch")
        self.A_lcd1 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd1.setGeometry(QtCore.QRect(100, 10, 81, 31))
        self.A_lcd1.setObjectName("A_Index")
        self.A_lcd6 = QtWidgets.QLCDNumber(self.frame_2)
        self.A_lcd6.setGeometry(QtCore.QRect(100, 210, 81, 31))
        self.A_lcd6.setObjectName("A_CHlaout")


        self.StreamANFr = QtWidgets.QFrame(self)
        self.StreamANFr.setGeometry(QtCore.QRect(790, 390, 561, 351))
        self.StreamANFr.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.StreamANFr.setFrameShadow(QtWidgets.QFrame.Raised)
        self.StreamANFr.setObjectName("StreamANFr")





        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(930, 710, 67, 17))
        self.label.setObjectName("label")
        self.line_9 = QtWidgets.QFrame(self)
        self.line_9.setGeometry(QtCore.QRect(7, 340, 1341, 21))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(980, 360, 181, 20))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(350, 360, 121, 17))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(830, 430, 67, 17))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(830, 470, 91, 17))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self)
        self.label_6.setGeometry(QtCore.QRect(830, 510, 67, 17))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(self)
        self.label_7.setGeometry(QtCore.QRect(830, 550, 71, 17))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(self)
        self.label_8.setGeometry(QtCore.QRect(830, 590, 81, 17))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(self)
        self.label_9.setGeometry(QtCore.QRect(830, 630, 67, 17))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(self)
        self.label_10.setGeometry(QtCore.QRect(830, 670, 67, 17))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self)
        self.label_11.setGeometry(QtCore.QRect(1110, 430, 67, 17))
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self)
        self.label_12.setGeometry(QtCore.QRect(1110, 470, 91, 17))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self)
        self.label_13.setGeometry(QtCore.QRect(1110, 550, 67, 17))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(self)
        self.label_14.setGeometry(QtCore.QRect(1110, 510, 67, 17))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(self)
        self.label_15.setGeometry(QtCore.QRect(1090, 590, 101, 17))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(self)
        self.label_16.setGeometry(QtCore.QRect(1110, 630, 67, 17))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(self)
        self.label_17.setGeometry(QtCore.QRect(1110, 670, 67, 17))
        self.label_17.setObjectName("label_17")
        self.StreamANFr.raise_()
        self.frame_2.raise_()
        self.label_5.raise_()
        self.EncFram.raise_()
        self.SW1L.raise_()
        self.SW1R.raise_()
        self.SW2R.raise_()
        self.SW2L.raise_()
        self.SW2up.raise_()
        self.EncMain.raise_()
        self.EncBack.raise_()
        self.Muxmain.raise_()
        self.MuxBack.raise_()
        self.Testpunk1.raise_()
        self.Testpunk2.raise_()
        self.Testpunk3.raise_()
        self.Testpunk4.raise_()
        self.Testpunk5.raise_()
        self.Testpunk6.raise_()
        self.Testpunk7.raise_()
        self.Testpunk8.raise_()
        self.line.raise_()
        self.line_2.raise_()
        self.line_3.raise_()
        self.line_4.raise_()
        self.line_5.raise_()
        self.line_6.raise_()
        self.line_7.raise_()
        self.line_8.raise_()
        self.SW2up_2.raise_()
        self.frame.raise_()
        self.VidLb.raise_()
        self.VidL.raise_()
        self.progressbar.raise_()
        self.label.raise_()
        self.line_9.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_9.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.label_12.raise_()
        self.label_13.raise_()
        self.label_14.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()

        self.SW2up.setText("Catalyst WS - C 4948 -10 GE   / bcisqr62b")
        self.EncMain.setText("Encoder \n"
                             "Chassis\n"
                             " 1\n"
                             " Main")
        self.EncBack.setText("Encoder \n"
                             "Chassis\n"
                             " 2\n"
                             " Backup")
        self.Muxmain.setText("MUX \n"
                             "DCM\n"
                             " 1\n"
                             " Main")
        self.MuxBack.setText("MUX \n"
                             "DCM\n"
                             " 2\n"
                             "Backup")
        self.Testpunk1.setText(("TP1"))
        self.Testpunk2.setText(("TP2"))
        self.Testpunk3.setText(("TP3"))
        self.Testpunk4.setText(("TP4"))
        self.Testpunk5.setText(("TP5"))
        self.Testpunk6.setText(("TP6"))
        self.Testpunk7.setText(("TP7"))
        self.Testpunk8.setText(("TP8"))
        self.SW2up_2.setText(("Catalyst WS - C 4948 -10 GE   / bcisqr62a"))
        self.VidLb.setText(("Video"))
        self.VidL.setText(("Audio"))
        self.label.setText(("Test State"))
        self.label_2.setText(("Video and Audio Analyze"))
        self.label_3.setText(("Source Room"))
        self.label_4.setText(("Index"))
        self.label_5.setText(("Codec NM"))
        self.label_6.setText(("Channels"))
        self.label_7.setText(("Codec Tag"))
        self.label_8.setText(("Samp Rate"))
        self.label_9.setText(("Ch Layout"))
        self.label_10.setText(("Bit rate"))
        self.label_11.setText(("Index"))
        self.label_12.setText(("Codec NM"))
        self.label_13.setText(("Width"))
        self.label_14.setText(("Hight"))
        self.label_15.setText(("     Dsy Asp Rt"))
        self.label_16.setText("Refrence")
        self.label_17.setText("Bit rate")

        ############################      The Viedeo and frame  ###############################################3

        self.frame = QtWidgets.QFrame(self)
        self.frame.setGeometry(QtCore.QRect(950, 40, 391, 291))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)

        self.mediaPlayer = QtMultimedia.QMediaPlayer(self.frame)
        self.video_widget = QtMultimediaWidgets.QVideoWidget(self.frame)
        self.mediaPlayer.setVideoOutput(self.video_widget)
        layout1 = QtWidgets.QGridLayout(self.frame)
        layout1.addWidget(self.video_widget, 0, 0, 1, 2)

        ########################################################################################################################
        ########################## SD and HD buttons############################################

        #self.AASD = QtWidgets.QToolButton(self)
        self.AASD = QtWidgets.QToolButton(self,text="SD", checkable=True)

        self.AASD.setGeometry(QtCore.QRect(140, 70, 31, 32))

        #self.AASD.setObjectName("AASD")
        #self.AASD.setText("SD")
        #self.AASD.clicked.connect(self.funcchoos)
        QTimer.singleShot(5000, lambda: self.AASD.setDisabled(False))

        #self.AAHD = QtWidgets.QToolButton(self)
        self.AAHD = QtWidgets.QToolButton(self,text="HD",checkable=True )

        self.AAHD.setGeometry(QtCore.QRect(180, 70, 31, 32))
        #self.AAHD.setObjectName("AAHD")
        #self.AAHD.setText("HD")
        #self.AAHD.clicked.connect(self.funcchoos)
        self.AAHD.setEnabled(False)
        #####
        #self.EngHD = QtWidgets.QToolButton(self)
        self.EngHD = QtWidgets.QToolButton(self,text="HD",checkable=True )
        self.EngHD.setGeometry(QtCore.QRect(180, 120, 31, 32))
        #self.EngHD.setObjectName("EngHD")
        #self.EngHD.setText("HD")
        #self.EngHD.clicked.connect(self.funcchoos)

        #self.EngSD = QtWidgets.QToolButton(self)
        self.EngSD = QtWidgets.QToolButton(self,text="SD",checkable=True )

        self.EngSD.setGeometry(QtCore.QRect(140, 120, 31, 32))
        #self.EngSD.clicked.connect(self.funcchoos)
        #self.EngSD.setText("SD")
        #self.EngSD.setObjectName("EngSD")
        ######

        #self.EspHD = QtWidgets.QToolButton(self)
        self.EspHD = QtWidgets.QToolButton(self,text="HD",checkable=True )
        self.EspHD.setGeometry(QtCore.QRect(180, 170, 31, 32))

        #self.EspHD.setObjectName("EspHD")
        #self.EspHD.setText("HD")
        #self.EspHD.clicked.connect(self.funcchoos)
        self.EspHD.setEnabled(False)

        #self.EspSD = QtWidgets.QToolButton(self)
        self.EspSD = QtWidgets.QToolButton(self,text="SD",checkable=True )
        self.EspSD.setGeometry(QtCore.QRect(140, 170, 31, 32))

        #self.EspSD.setObjectName("EspSD")
        #self.EspSD.setText("SD")
        #self.EspSD.clicked.connect(self.funcchoos)
        ######
        #self.DeuHD = QtWidgets.QToolButton(self)
        self.DeuHD = QtWidgets.QToolButton(self,text="HD",checkable=True )
        self.DeuHD.setGeometry(QtCore.QRect(180, 220, 31, 32))

        #self.DeuHD.setObjectName("DeuHD")
        #self.DeuHD.setText("HD")
        #self.DeuHD.clicked.connect(self.funcchoos)
        self.DeuHD.setEnabled(False)

        #self.DeuSD = QtWidgets.QToolButton(self)
        self.DeuSD = QtWidgets.QToolButton(self,text="SD",checkable=True )
        self.DeuSD.setGeometry(QtCore.QRect(140, 220, 31, 32))

        #self.DeuSD.setObjectName("DeuSD")
        #self.DeuSD.setText("SD")
       # self.DeuSD.toggled.connect(self.setValue)     ## the button and led

        #self.DeuSD.clicked.connect(self.setValue)
        #####

        #self.DeupHD = QtWidgets.QToolButton(self)
        self.DeupHD = QtWidgets.QToolButton(self,text="HD",checkable=True )
        self.DeupHD.setGeometry(QtCore.QRect(180, 270, 31, 32))

        #self.DeupHD.setObjectName("DeupHD")
        #self.DeupHD.setText("SD")
        #self.DeupHD.clicked.connect(self.funcchoos)
        self.DeupHD.setEnabled(False)

        #self.DeupSD = QtWidgets.QToolButton(self)
        self.DeupSD = QtWidgets.QToolButton(self,text="SD",checkable=True )
        self.DeupSD.setGeometry(QtCore.QRect(140, 270, 31, 32))

        #self.DeupSD.setObjectName("DeupSD")
        #self.DeupSD.setText("SD")
        #self.DeupSD.clicked.connect(self.funcchoos)

        ################################### The Main Labels #######################################################

        self.infolabel = QtWidgets.QLabel(self)
        self.infolabel.setFont(QFont('Arial', 8))
        self.infolabel.setGeometry(QtCore.QRect(990, 325, 250, 35))
        self.infolabel.setText("Info: ")

        self.Tvlabel = QtWidgets.QLabel(self)
        self.Tvlabel.setFont(QFont('Arial', 18))
        self.Tvlabel.setGeometry(QtCore.QRect(1070, 7, 250, 35))
        self.Tvlabel.setText("TV Display")

        self.Chnlabel = QtWidgets.QLabel(self)
        self.Chnlabel.setFont(QFont('Arial', 14))
        self.Chnlabel.setGeometry(QtCore.QRect(20, 15, 500, 35))
        self.Chnlabel.setText("Choose one of the services for testing")

        #######  the top DW channels color and labels###############################

        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(20, 70, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.53, y2:0.460227, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(20, 120, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.53, y2:0.460227, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setGeometry(QtCore.QRect(20, 170, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_3.setFont(font)
        self.label_3.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.53, y2:0.460227, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(20, 220, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_4.setFont(font)
        self.label_4.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.53, y2:0.460227, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setGeometry(QtCore.QRect(20, 270, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)
        self.label_5.setFont(font)
        self.label_5.setStyleSheet(
            "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:0.53, y2:0.460227, stop:0 rgba(0, 0, 0, 255), stop:1 rgba(255, 255, 255, 255));")
        self.label_5.setObjectName("label_5")

        self.label.setText("DW Arabia")
        self.label_2.setText("DW English")
        self.label_3.setText("DW Español")
        self.label_4.setText("DW Deutsch")
        self.label_5.setText("DW Deutsch+")
        #######################################################################################


        ###########################the lines####################
        self.line_2 = QtWidgets.QFrame(self)
        self.line_2.setGeometry(QtCore.QRect(220, 80, 311, 1))
        self.line_2.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_2.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self)
        self.line_3.setGeometry(QtCore.QRect(220, 130, 291, 1))
        self.line_3.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_3.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self)
        self.line_4.setGeometry(QtCore.QRect(220, 180, 271, 1))
        self.line_4.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_4.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_5 = QtWidgets.QFrame(self)
        self.line_5.setGeometry(QtCore.QRect(220, 230, 251, 1))
        self.line_5.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_5.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.line_6 = QtWidgets.QFrame(self)
        self.line_6.setGeometry(QtCore.QRect(220, 280, 231, 1))
        self.line_6.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_6.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line = QtWidgets.QFrame(self)
        self.line.setGeometry(QtCore.QRect(450, 280, 1, 70))
        self.line.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_7 = QtWidgets.QFrame(self)
        self.line_7.setGeometry(QtCore.QRect(470, 230, 1, 120))
        self.line_7.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_7.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_7.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.line_8 = QtWidgets.QFrame(self)
        self.line_8.setGeometry(QtCore.QRect(490, 180, 1, 170))
        self.line_8.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_8.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_8.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self)
        self.line_9.setGeometry(QtCore.QRect(510, 130, 1, 220))
        self.line_9.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_9.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_9.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.line_10 = QtWidgets.QFrame(self)
        self.line_10.setGeometry(QtCore.QRect(530, 80, 1, 270))
        self.line_10.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_10.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_10.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.line_12 = QtWidgets.QFrame(self)
        self.line_12.setGeometry(QtCore.QRect(680, 80, 1, 270))
        self.line_12.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_12.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_12.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.line_15 = QtWidgets.QFrame(self)
        self.line_15.setGeometry(QtCore.QRect(740, 230, 1, 120))
        self.line_15.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_15.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_15.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_15.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_15.setObjectName("line_15")
        self.line_16 = QtWidgets.QFrame(self)
        self.line_16.setGeometry(QtCore.QRect(700, 130, 1, 220))
        self.line_16.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_16.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_16.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_16.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_16.setObjectName("line_16")
        self.line_17 = QtWidgets.QFrame(self)
        self.line_17.setGeometry(QtCore.QRect(720, 180, 1, 170))
        self.line_17.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_17.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_17.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_17.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_17.setObjectName("line_17")
        self.line_18 = QtWidgets.QFrame(self)
        self.line_18.setGeometry(QtCore.QRect(760, 280, 1, 70))
        self.line_18.setMaximumSize(QtCore.QSize(1, 16777215))
        self.line_18.setStyleSheet("background-color: rgb(91, 91, 91);")
        self.line_18.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_18.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_18.setObjectName("line_18")
        self.line_19 = QtWidgets.QFrame(self)
        self.line_19.setGeometry(QtCore.QRect(700, 130, 251, 1))
        self.line_19.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_19.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_19.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_19.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_19.setObjectName("line_19")
        self.line_20 = QtWidgets.QFrame(self)
        self.line_20.setGeometry(QtCore.QRect(760, 280, 191, 1))
        self.line_20.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_20.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_20.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_20.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_20.setObjectName("line_20")
        self.line_21 = QtWidgets.QFrame(self)
        self.line_21.setGeometry(QtCore.QRect(740, 230, 211, 1))
        self.line_21.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_21.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_21.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_21.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_21.setObjectName("line_21")
        self.line_22 = QtWidgets.QFrame(self)
        self.line_22.setGeometry(QtCore.QRect(680, 80, 271, 1))
        self.line_22.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_22.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_22.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_22.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_22.setObjectName("line_22")
        self.line_23 = QtWidgets.QFrame(self)
        self.line_23.setGeometry(QtCore.QRect(720, 180, 231, 1))
        self.line_23.setMaximumSize(QtCore.QSize(16777215, 1))
        self.line_23.setStyleSheet("background-color: rgb(94, 94, 94);")
        self.line_23.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_23.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_23.setObjectName("line_23")
    ######################################################################################
    ############################ the special functions#######################
        self.AASD.toggled.connect(self.TPL1.setValue)
        self.EngSD.toggled.connect(self.TPL1.setValue)
        self.EngHD.toggled.connect(self.TPL1.setValue)
        self.DeuSD.toggled.connect(self.TPL1.setValue)
        self.DeupSD.toggled.connect(self.TPL1.setValue)


        self.Testpunk1.clicked.connect(self.on_tp_clicked)
        self.Testpunk2.clicked.connect(self.on_tp_clicked)
        self.Testpunk3.clicked.connect(self.on_tp_clicked)
        self.Testpunk4.clicked.connect(self.on_tp_clicked)
        self.Testpunk5.clicked.connect(self.on_tp_clicked)
        self.Testpunk6.clicked.connect(self.on_tp_clicked)
        self.Testpunk7.clicked.connect(self.on_tp_clicked)
        self.Testpunk8.clicked.connect(self.on_tp_clicked)

        self.current_button = None

        self.process = QtCore.QProcess(self)
        self.process.finished.connect(self.on_finish)

    @QtCore.pyqtSlot()
    def on_tp_clicked(self):
        if self.AASD.isChecked():
            urls_map = {
                self.Testpunk1: "http://dwstream6-lh.akamaihd.net/i/dwstream6_live@123962/master.m3u8",
                self.Testpunk2: "239.168.1.7:1116",
                self.Testpunk3:  "239.168.1.6:1132",
                self.Testpunk4:  "239.168.1.6:1136",
                self.Testpunk5:  "239.168.2.6:2113",
                self.Testpunk6:  "239.168.2.7:2122",
                self.Testpunk7:  "239.168.2.8:2132",
                self.Testpunk8:  "239.168.2.9:2142",
            }
            url = urls_map.get(self.sender(), "")
            if url:
                self.play(url)
                self.current_button = self.sender()
                self.current_button.setEnabled(False)

        if self.EngSD.isChecked():
            urls_map = {

                self.Testpunk1: "239.168.1.6:1111",
                self.Testpunk2: "239.168.1.7:1115",
                self.Testpunk3: "239.168.1.6:1131",
                self.Testpunk4: "239.168.1.6:1135",
                self.Testpunk5: "239.168.2.6:2111",
                self.Testpunk6: "239.168.2.7:2121",
                self.Testpunk7: "239.168.2.8:2131",
                self.Testpunk8: "239.168.2.9:2141",
            }
            url = urls_map.get(self.sender(), "")
            if url:
                self.play(url)
                self.current_button = self.sender()
                self.current_button.setEnabled(False)




              ###########add the others















    def play(self, url):

        self.progressbar.setRange(0, 0)
        self.mediaPlayer.setMedia(QtMultimedia.QMediaContent(QtCore.QUrl(url)))
        self.mediaPlayer.play()

        cmd = "ffprobe -v quiet -print_format json -show_streams"
        program, *args = shlex.split(cmd)
        args.append(url)
        self.process.start(program, args)

    @QtCore.pyqtSlot()
    def on_finish(self):
        data = self.process.readAllStandardOutput().data()
        if data:
            ffprobeOutput = json.loads(data)
            #result = ffprobeOutput['streams'][0]


            ##############  Video parameter############33

            index=ffprobeOutput['streams'][0]['index']
            codec_name = ffprobeOutput['streams'][0]['codec_name']
            height = ffprobeOutput['streams'][0]['height']
            width = ffprobeOutput['streams'][0]['width']

            display_aspect_ratio = ffprobeOutput['streams'][0]['display_aspect_ratio']
            codec_tag=ffprobeOutput['streams'][0]['codec_tag']

            sample_aspect_ratio = ffprobeOutput['streams'][0]['sample_aspect_ratio']
            refs = ffprobeOutput['streams'][0]['refs']
            has_b_frames = ffprobeOutput['streams'][0]['has_b_frames']
            start_pts = ffprobeOutput['streams'][0]['start_pts']


            self.V_lcd1.display(index)
            self.V_lcd2.display(codec_name)
            self.V_lcd3.display(height)
            self.V_lcd4.display(width)
            self.V_lcd5.display(display_aspect_ratio)
            self.V_lcd6.display(refs)
            self.V_lcd7.display(sample_aspect_ratio)
            ################### Audio parameters 3###########
            index = ffprobeOutput['streams'][1]['index'] #1
            codec_name = ffprobeOutput['streams'][1]['codec_name']#2
            channels=ffprobeOutput['streams'][1]['channels']#3
            codec_tag=ffprobeOutput['streams'][1]['codec_tag']#4
            sample_rate=ffprobeOutput['streams'][1]['sample_rate']#5
            bits_per_sample=ffprobeOutput['streams'][1]['bits_per_sample']#6
            sample_fmt=ffprobeOutput['streams'][1]['sample_fmt']#7

            self.A_lcd1.display(index)
            self.A_lcd2.display(codec_name)
            self.A_lcd3.display(channels)
            self.A_lcd4.display(codec_tag)
            self.A_lcd5.display(sample_rate)
            self.A_lcd6.display(bits_per_sample)
            self.A_lcd7.display(sample_fmt)







        self.current_button.setEnabled(True)
        self.current_button = None
        self.progressbar.setRange(0, 1)
        self.progressbar.setValue(0)








if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = MainProg()
    w.show()
    sys.exit(app.exec_())