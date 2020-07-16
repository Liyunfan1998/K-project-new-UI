# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'instructions.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget_exerciseList = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_exerciseList.setGeometry(QtCore.QRect(30, 20, 256, 701))
        self.listWidget_exerciseList.setObjectName("listWidget_exerciseList")
        self.pushButton_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_home.setGeometry(QtCore.QRect(100, 730, 112, 32))
        self.pushButton_home.setObjectName("pushButton_home")
        self.textBrowser_instructionsPerExercise = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_instructionsPerExercise.setGeometry(QtCore.QRect(290, 610, 751, 161))
        self.textBrowser_instructionsPerExercise.setObjectName("textBrowser_instructionsPerExercise")
        self.pushButton_videoPlay = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_videoPlay.setGeometry(QtCore.QRect(1060, 20, 112, 32))
        self.pushButton_videoPlay.setObjectName("pushButton_videoPlay")
        self.pushButton_VideoStop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_VideoStop.setGeometry(QtCore.QRect(1060, 70, 112, 32))
        self.pushButton_VideoStop.setObjectName("pushButton_VideoStop")
        self.pushButton_print = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_print.setGeometry(QtCore.QRect(1060, 120, 112, 32))
        self.pushButton_print.setObjectName("pushButton_print")
        self.horizontalSlider_videoPos = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_videoPos.setGeometry(QtCore.QRect(290, 570, 751, 22))
        self.horizontalSlider_videoPos.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_videoPos.setObjectName("horizontalSlider_videoPos")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(290, 20, 751, 531))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_videoPlayer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_videoPlayer.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_videoPlayer.setObjectName("verticalLayout_videoPlayer")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton_home.setText(_translate("MainWindow", "Home"))
        self.pushButton_videoPlay.setText(_translate("MainWindow", "Play"))
        self.pushButton_VideoStop.setText(_translate("MainWindow", "Stop"))
        self.pushButton_print.setText(_translate("MainWindow", "Print"))


