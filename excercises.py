# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'excercises.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 800)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_exerciseName = QtWidgets.QLabel(self.centralwidget)
        self.label_exerciseName.setGeometry(QtCore.QRect(10, 10, 471, 101))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_exerciseName.setFont(font)
        self.label_exerciseName.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_exerciseName.setMidLineWidth(0)
        self.label_exerciseName.setWordWrap(True)
        self.label_exerciseName.setObjectName("label_exerciseName")
        self.listWidget_realtimeInstructions = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_realtimeInstructions.setGeometry(QtCore.QRect(10, 170, 471, 441))
        self.listWidget_realtimeInstructions.setObjectName("listWidget_realtimeInstructions")
        self.progressBar_leftToGo = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar_leftToGo.setGeometry(QtCore.QRect(10, 670, 471, 51))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar_leftToGo.sizePolicy().hasHeightForWidth())
        self.progressBar_leftToGo.setSizePolicy(sizePolicy)
        self.progressBar_leftToGo.setMinimumSize(QtCore.QSize(0, 41))
        self.progressBar_leftToGo.setBaseSize(QtCore.QSize(0, 20))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.progressBar_leftToGo.setFont(font)
        self.progressBar_leftToGo.setAutoFillBackground(False)
        self.progressBar_leftToGo.setProperty("value", 50)
        self.progressBar_leftToGo.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.progressBar_leftToGo.setInvertedAppearance(False)
        self.progressBar_leftToGo.setObjectName("progressBar_leftToGo")
        self.label_leftToGo = QtWidgets.QLabel(self.centralwidget)
        self.label_leftToGo.setGeometry(QtCore.QRect(10, 617, 471, 51))
        font = QtGui.QFont()
        font.setPointSize(40)
        self.label_leftToGo.setFont(font)
        self.label_leftToGo.setFrameShape(QtWidgets.QFrame.WinPanel)
        self.label_leftToGo.setMidLineWidth(0)
        self.label_leftToGo.setWordWrap(True)
        self.label_leftToGo.setObjectName("label_leftToGo")
        self.graphicsView_videoCapture = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_videoCapture.setGeometry(QtCore.QRect(500, 410, 480, 360))
        self.graphicsView_videoCapture.setObjectName("graphicsView_videoCapture")
        self.pushButton_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_home.setGeometry(QtCore.QRect(170, 720, 112, 32))
        self.pushButton_home.setObjectName("pushButton_home")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(500, 10, 481, 361))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout_videoPlayer = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout_videoPlayer.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_videoPlayer.setObjectName("verticalLayout_videoPlayer")
        self.pushButton_videoPlay = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_videoPlay.setGeometry(QtCore.QRect(490, 370, 91, 32))
        self.pushButton_videoPlay.setObjectName("pushButton_videoPlay")
        self.horizontalSlider_videoPos = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_videoPos.setGeometry(QtCore.QRect(600, 370, 381, 22))
        self.horizontalSlider_videoPos.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_videoPos.setObjectName("horizontalSlider_videoPos")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_exerciseName.setText(_translate("MainWindow", "Muscle Tightening Deep Breathing"))
        self.progressBar_leftToGo.setFormat(_translate("MainWindow", "nothing"))
        self.label_leftToGo.setText(_translate("MainWindow", "2 to go!"))
        self.pushButton_home.setText(_translate("MainWindow", "Home"))
        self.pushButton_videoPlay.setText(_translate("MainWindow", "Play"))


