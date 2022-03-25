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

import os
os.add_dll_directory(r'C:\Program Files\VideoLAN\VLC')

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QLabel, QMainWindow
from PyQt5.QtCore import QDir, Qt, QUrl, QSize, QPoint, QTimer
from PyQt5.QtGui import QPainter, QColor, QPen,QFont,QIcon, QPixmap
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QGridLayout, QLCDNumber)
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QGridLayout, QLCDNumber
import vlc


class MainProg(QtWidgets.QMainWindow):
    def __init__(self, parent=None):

        super(MainProg, self).__init__(parent)

        self.setObjectName("MainWindow")
        self.setFixedSize(675, 324)
        self.setWindowTitle("DCM HeadEnd 1 / DW LAN1 / (RTP) Stream Tester")

###############################
        ########### VLC parts ##############
        self.instance = vlc.Instance()
        self.mediaplayer = self.instance.media_player_new()
############################      The Video and frame  #################################

        self.videoframe = QtWidgets.QFrame(self)
        self.videoframe.setGeometry(QtCore.QRect(210, 20, 431, 271))

        self.videoframe.setFrameShape(QtWidgets.QFrame.Box)
        self.videoframe.setFrameShadow(QtWidgets.QFrame.Raised)

        self.vboxlayout = QVBoxLayout()
        self.vboxlayout.addWidget(self.videoframe)
        self.mediaplayer.set_hwnd(int(self.videoframe.winId()))


        ###################combobox

        self.comboBox = QtWidgets.QComboBox(self)
        self.comboBox.setGeometry(QtCore.QRect(30, 50, 161, 22))
        self.comboBox.setObjectName("comboBox")

###### the streams
        self.comboBox.addItem("STREAM-B1")
        self.comboBox.setItemData(0,'rtp://239.195.0.3:50000')

        self.comboBox.addItem("Reuters wne SD")
        self.comboBox.setItemData(1,'rtp://239.195.0.5:50000')

        self.comboBox.addItem("RTV 1 SD")
        self.comboBox.setItemData(2,'rtp://239.195.0.6:50000')

        self.comboBox.addItem("EBU 1 SD")
        self.comboBox.setItemData(3,'rtp://239.195.0.7:50000')

        self.comboBox.addItem("AP DIRECT SD")
        self.comboBox.setItemData(4,'rtp://239.195.0.8:50000')

        self.comboBox.addItem("AP Feeds SD")
        self.comboBox.setItemData(5,'rtp://239.195.0.8:50000')

        self.comboBox.addItem("Konferenzraum 102")
        self.comboBox.setItemData(6,'rtp://239.195.0.10:50000')

        self.comboBox.addItem("Hauskanal 1 HD")
        self.comboBox.setItemData(7,'rtp://239.195.0.11:50000')

        self.comboBox.addItem("EBU 2 SD")
        self.comboBox.setItemData(8,'rtp://239.195.0.12:50000')

        self.comboBox.addItem("Eurosport 1 Deutschland")
        self.comboBox.setItemData(9,'rtp://239.225.236.101:50000')

        self.comboBox.addItem("DW Deutsch plus")
        self.comboBox.setItemData(10,'rtp://239.225.236.102:50000')

        self.comboBox.addItem("DW Espanol")
        self.comboBox.setItemData(11,'rtp://239.225.236.103:50000')

        self.comboBox.addItem("DW Deutsch")
        self.comboBox.setItemData(12,'rtp://239.225.236.104:50000')

        self.comboBox.addItem("DW Arabia")
        self.comboBox.setItemData(13,'rtp://239.225.236.105:50000')

        self.comboBox.addItem("DW English")
        self.comboBox.setItemData(14,'rtp://239.225.236.106:50000')

        self.comboBox.addItem("EBU 3 SD")
        self.comboBox.setItemData(15,'rtp://239.225.236.107:50000')

        self.comboBox.addItem("Al Jazeera English HD")
        self.comboBox.setItemData(16,'rtp://239.225.236.108:50000')

        self.comboBox.addItem("CGTN")
        self.comboBox.setItemData(17,'rtp://239.225.236.109:50000')

        self.comboBox.addItem("CNN HD")
        self.comboBox.setItemData(18,'rtp://239.225.236.110:50000')

        self.comboBox.addItem("France 24")
        self.comboBox.setItemData(19,'rtp://239.225.236.111:50000')

        self.comboBox.addItem("BBC World News")
        self.comboBox.setItemData(20,'rtp://239.225.236.112:50000')

        self.comboBox.addItem("TVE International")
        self.comboBox.setItemData(21,'rtp://239.225.236.113:50000')

        self.comboBox.addItem("RT HD")
        self.comboBox.setItemData(22,'rtp://239.225.236.114:50000')

        self.comboBox.addItem("Bloomberg Europe TV")
        self.comboBox.setItemData(23,'rtp://239.225.236.115:50000')

        self.comboBox.addItem("WELT")
        self.comboBox.setItemData(24,'rtp://239.225.236.116:50000')

        self.comboBox.addItem("n-TV")
        self.comboBox.setItemData(25,'rtp://239.225.236.117:50000')

        self.comboBox.addItem("ProSieben")
        self.comboBox.setItemData(26,'rtp://239.225.236.118:50000')

        self.comboBox.addItem("SAT.1")
        self.comboBox.setItemData(27,'rtp://239.225.236.119:50000')

        self.comboBox.addItem("RTL Bayern")
        self.comboBox.setItemData(28,'rtp://239.225.236.120:50000')

        self.comboBox.addItem("Das Erste")
        self.comboBox.setItemData(29,'rtp://239.225.236.121:50000')

        self.comboBox.addItem("ZDF")
        self.comboBox.setItemData(30,'rtp://239.225.236.122:50000')

        self.comboBox.addItem("phoenix")
        self.comboBox.setItemData(31,'rtp://239.225.236.123:50000')

        self.comboBox.addItem("Arte")
        self.comboBox.setItemData(32,'rtp://239.225.236.124:50000')


        self.comboBox.addItem("3sat")
        self.comboBox.setItemData(33,'rtp://239.225.236.125:50000')


        self.comboBox.addItem("Tagesschau24")
        self.comboBox.setItemData(34,'rtp://239.225.236.126:50000')


        self.comboBox.addItem("ZDFinfo")
        self.comboBox.setItemData(35,'rtp://239.225.236.127:50000')


        self.comboBox.addItem("EBSHD")
        self.comboBox.setItemData(36,'rtp://239.225.236.128:50000')


        self.comboBox.addItem("STUDIO 1 SD")
        self.comboBox.setItemData(37,'rtp://239.225.236.129:50000')


        self.comboBox.addItem("STUDIO 2 SD")
        self.comboBox.setItemData(38,'rtp://239.225.236.130:50000')


        self.comboBox.addItem("STUDIO 3 SD")
        self.comboBox.setItemData(39,'rtp://239.225.236.131:50000')


        self.comboBox.addItem("SPORT 1")
        self.comboBox.setItemData(40,'rtp://239.225.236.132:50000')


        self.comboBox.addItem("Al Rasheed")
        self.comboBox.setItemData(41,'rtp://239.225.236.134:50000')


        self.comboBox.addItem("PAW HAV")
        self.comboBox.setItemData(42,'rtp://239.225.236.135:50000')


        self.comboBox.addItem("Echorouk TV News")
        self.comboBox.setItemData(43,'rtp://239.225.236.136:50000')


        self.comboBox.addItem("AFP 1")
        self.comboBox.setItemData(44,'rtp://239.225.236.137:50000')


        self.comboBox.addItem("Crowdtangle")
        self.comboBox.setItemData(45,'rtp://239.225.236.138:50000')


        self.comboBox.addItem("AFP 2")
        self.comboBox.setItemData(46,'rtp://239.225.236.139:50000')


        self.comboBox.addItem("AFP 3")
        self.comboBox.setItemData(47,'rtp://239.225.236.140:50000')


        self.comboBox.addItem("AFP 4")
        self.comboBox.setItemData(48,'rtp://239.225.236.141:50000')


        self.comboBox.addItem("AP 1")
        self.comboBox.setItemData(49,'rtp://239.225.236.142:50000')


        self.comboBox.addItem("AP 2")
        self.comboBox.setItemData(50,'rtp://239.225.236.143:50000')

        self.comboBox.addItem("AP 3")
        self.comboBox.setItemData(51,'rtp://239.225.236.144:50000')


        self.comboBox.addItem("AP 4")
        self.comboBox.setItemData(52,'rtp://239.225.236.145:50000')


        self.comboBox.addItem("MV Agencies HD")
        self.comboBox.setItemData(53,'rtp://239.225.236.151:50000')


        self.comboBox.addItem("MV News")
        self.comboBox.setItemData(54,'rtp://239.225.236.152:50000')

        self.comboBox.addItem("MV Bundestagswahl 2021")
        self.comboBox.setItemData(55, 'rtp://239.195.0.13:50000')

        self.comboBox.addItem("Studio 5 HD")
        self.comboBox.setItemData(56, 'rtp://239.225.236.133:50000')



####################labels


        self.label = QtWidgets.QLabel(self)
        self.label.setGeometry(QtCore.QRect(30, 20, 180, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setGeometry(QtCore.QRect(40, 190, 150, 16))
        self.label_2.setObjectName("label_2")
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setGeometry(QtCore.QRect(40, 210, 150, 25))
        self.label_4.setObjectName("stream variable")
        self.label.setText(("Wählen Sie den Stream für Test"))
        self.label_2.setText(("Aktueller Stream und Port"))

        self.labelco = QtWidgets.QLabel(self)
        self.labelco.setGeometry(QtCore.QRect(450, 300, 200, 16))
        self.labelco.setObjectName("Copyrights")

        self.labelco.setText(("Copyright: © 2021 etc. Kutayba Nazhah"))
        font = QtGui.QFont()
        font.setFamily("Calibri")
        font.setPointSize(8)
        font.setItalic(True)
        self.labelco.setFont(font)

############ the combo box texts####
        self.comboBox.setItemText(0, ("STREAM-B1"))
        self.comboBox.setItemText(1, ( "Reuters wne SD"))
        self.comboBox.setItemText(2, ( "RTV 1 SD"))
        self.comboBox.setItemText(3, ( "EBU 1 SD"))
        self.comboBox.setItemText(4, ("AP DIRECT SD"))
        self.comboBox.setItemText(5, ("ap feeds SD"))








#############################
        self.comboBox.currentIndexChanged.connect(self.updateGraph)

    def updateGraph(self):

        self.mediaplayer.stop()


        url= str(self.comboBox.currentData())

        currentstram=((self.comboBox.currentData()))

        self.label_4.setText(str(currentstram))



        print(url)
        self.play(url)



    def play(self, url):


        self.media = self.instance.media_new(url)
        self.media.get_mrl()
        self.mediaplayer.set_media(self.media)
        self.mediaplayer.play()
















if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)

    w = MainProg()
    w.show()
    sys.exit(app.exec_())

##############################   End of the Code  ##########################################
