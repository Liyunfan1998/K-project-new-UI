# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Kproj(object):

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
        self.line.setGeometry(QtCore.QRect(380, 140, 20, 261))
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
        self.label_id.setGeometry(QtCore.QRect(430, 210, 58, 16))
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
        self.lineEdit_id.setGeometry(QtCore.QRect(520, 210, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.lineEdit_id.setFont(font)
        self.lineEdit_id.setObjectName("lineEdit_id")
        self.pushButton_login = QtWidgets.QPushButton(Kproj)
        self.pushButton_login.setGeometry(QtCore.QRect(500, 330, 151, 32))
        self.pushButton_login.setObjectName("pushButton_login")
        self.checkBox_isClinician = QtWidgets.QCheckBox(Kproj)
        self.checkBox_isClinician.setGeometry(QtCore.QRect(260, 100, 261, 20))
        self.checkBox_isClinician.setObjectName("checkBox_isClinician")
        self.label_gender = QtWidgets.QLabel(Kproj)
        self.label_gender.setGeometry(QtCore.QRect(430, 260, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_gender.setFont(font)
        self.label_gender.setObjectName("label_gender")
        self.frame = QtWidgets.QFrame(Kproj)
        self.frame.setGeometry(QtCore.QRect(520, 260, 111, 61))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.radioButton_male = QtWidgets.QRadioButton(self.frame)
        self.radioButton_male.setGeometry(QtCore.QRect(10, 10, 81, 20))
        self.radioButton_male.setObjectName("radioButton_male")
        self.radioButton_female = QtWidgets.QRadioButton(self.frame)
        self.radioButton_female.setGeometry(QtCore.QRect(10, 30, 81, 20))
        self.radioButton_female.setObjectName("radioButton_female")

        self.retranslateUi(Kproj)
        QtCore.QMetaObject.connectSlotsByName(Kproj)

    def retranslateUi(self, Kproj):
        _translate = QtCore.QCoreApplication.translate
        Kproj.setWindowTitle(_translate("Kproj", "Kproj"))
        self.label_title.setText(_translate("Kproj", "Welcome to Kinect ToLf"))
        self.label_name.setText(_translate("Kproj", "Name:"))
        self.label_id.setText(_translate("Kproj", "ID:"))
        self.pushButton_login.setText(_translate("Kproj", "Log in as patient"))
        self.checkBox_isClinician.setText(_translate("Kproj", "Click if you want to log in as a clinician"))
        self.label_gender.setText(_translate("Kproj", "Gender:"))
        self.radioButton_male.setText(_translate("Kproj", "Male"))
        self.radioButton_female.setText(_translate("Kproj", "Female"))
