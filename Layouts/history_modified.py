# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'history.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow_History:  # (object)
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.listWidget_history = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_history.setGeometry(QtCore.QRect(20, 249, 256, 471))
        self.listWidget_history.setObjectName("listWidget_history")
        self.graphicsView_angleDatePlot = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_angleDatePlot.setGeometry(QtCore.QRect(290, 10, 901, 751))
        self.graphicsView_angleDatePlot.setObjectName("graphicsView_angleDatePlot")
        self.pushButton_home = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_home.setGeometry(QtCore.QRect(80, 730, 112, 32))
        self.pushButton_home.setObjectName("pushButton_home")
        self.label_patientInfo = QtWidgets.QLabel(self.centralwidget)
        self.label_patientInfo.setGeometry(QtCore.QRect(20, 10, 251, 191))
        self.label_patientInfo.setAutoFillBackground(False)
        self.label_patientInfo.setFrameShape(QtWidgets.QFrame.Box)
        self.label_patientInfo.setObjectName("label_patientInfo")
        self.comboBox_actions = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_actions.setGeometry(QtCore.QRect(10, 210, 271, 32))
        self.comboBox_actions.setObjectName("comboBox_actions")
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
        self.label_patientInfo.setText(_translate("MainWindow", "Patient Info"))
