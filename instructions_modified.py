# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instructions.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_Instructions:  # (object)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(30, 20, 256, 701))
        self.listWidget.setObjectName("listWidget")
        self.pushButton_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_home.setGeometry(QtCore.QRect(100, 730, 112, 32))
        self.pushButton_home.setObjectName("pushButton_home")
        self.graphicsView_video = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_video.setGeometry(QtCore.QRect(290, 20, 751, 591))
        self.graphicsView_video.setObjectName("graphicsView_video")
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(290, 610, 751, 161))
        self.textBrowser.setObjectName("textBrowser")
        self.pushButton_play = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_play.setGeometry(QtCore.QRect(1060, 20, 112, 32))
        self.pushButton_play.setObjectName("pushButton_play")
        self.pushButton_pause = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_pause.setGeometry(QtCore.QRect(1060, 70, 112, 32))
        self.pushButton_pause.setObjectName("pushButton_pause")
        self.pushButton_stop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_stop.setGeometry(QtCore.QRect(1060, 120, 112, 32))
        self.pushButton_stop.setObjectName("pushButton_stop")
        self.pushButton_print = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_print.setGeometry(QtCore.QRect(1060, 250, 112, 32))
        self.pushButton_print.setObjectName("pushButton_print")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(1060, 190, 111, 22))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        # MainWindow.setCentralWidget(self.centralwidget)
        # self.statusbar = QtWidgets.QStatusBar(MainWindow)
        # self.statusbar.setObjectName("statusbar")
        # MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_home.setText(_translate("MainWindow", "Home"))
        self.pushButton_play.setText(_translate("MainWindow", "Play"))
        self.pushButton_pause.setText(_translate("MainWindow", "Pause"))
        self.pushButton_stop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_print.setText(_translate("MainWindow", "Print"))
