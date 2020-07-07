# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import sys

class Ui_Kproj(object):
    def __init__(self):
        pass

    def setupUi(self, Kproj):
        Kproj.setObjectName("Kproj")
        Kproj.resize(800, 430)
        self.label_title = QtWidgets.QLabel(Kproj)
        self.label_title.setGeometry(QtCore.QRect(270, 10, 311, 81))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.graphicsView_logo = QtWidgets.QGraphicsView(Kproj)
        self.graphicsView_logo.setGeometry(QtCore.QRect(90, 150, 256, 192))
        self.graphicsView_logo.setObjectName("graphicsView_logo")
        self.line = QtWidgets.QFrame(Kproj)
        self.line.setGeometry(QtCore.QRect(380, 110, 20, 291))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_name = QtWidgets.QLabel(Kproj)
        self.label_name.setGeometry(QtCore.QRect(430, 160, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.label_id = QtWidgets.QLabel(Kproj)
        self.label_id.setGeometry(QtCore.QRect(430, 250, 58, 16))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_id.setFont(font)
        self.label_id.setObjectName("label_id")
        self.lineEdit_name = QtWidgets.QLineEdit(Kproj)
        self.lineEdit_name.setGeometry(QtCore.QRect(520, 160, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_name.setFont(font)
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_id = QtWidgets.QLineEdit(Kproj)
        self.lineEdit_id.setGeometry(QtCore.QRect(520, 250, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_id.setFont(font)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.pushButton_login = QtWidgets.QPushButton(Kproj)
        self.pushButton_login.setGeometry(QtCore.QRect(520, 310, 112, 32))
        self.pushButton_login.setObjectName("pushButton_login")

        self.retranslateUi(Kproj)
        QtCore.QMetaObject.connectSlotsByName(Kproj)

    def retranslateUi(self, Kproj):
        _translate = QtCore.QCoreApplication.translate
        Kproj.setWindowTitle(_translate("Kproj", "Kproj"))
        self.label_title.setText(_translate("Kproj", "Welcome to Kinect ToLf"))
        self.label_name.setText(_translate("Kproj", "Name:"))
        self.label_id.setText(_translate("Kproj", "ID:"))
        self.pushButton_login.setText(_translate("Kproj", "Log On"))


