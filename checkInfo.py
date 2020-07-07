# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'checkInfo.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_CheckInfo(object):
    def setupUi(self, CheckInfo):
        CheckInfo.setObjectName("CheckInfo")
        CheckInfo.resize(440, 340)
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        CheckInfo.setFont(font)
        self.label_title = QtWidgets.QLabel(CheckInfo)
        self.label_title.setGeometry(QtCore.QRect(30, 10, 391, 81))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.label_name = QtWidgets.QLabel(CheckInfo)
        self.label_name.setGeometry(QtCore.QRect(90, 116, 58, 31))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        self.label_name.setFont(font)
        self.label_name.setObjectName("label_name")
        self.pushButton_login = QtWidgets.QPushButton(CheckInfo)
        self.pushButton_login.setGeometry(QtCore.QRect(50, 290, 112, 32))
        self.pushButton_login.setObjectName("pushButton_login")
        self.label_id = QtWidgets.QLabel(CheckInfo)
        self.label_id.setGeometry(QtCore.QRect(90, 206, 58, 31))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        self.label_id.setFont(font)
        self.label_id.setObjectName("label_id")
        self.label_name_2 = QtWidgets.QLabel(CheckInfo)
        self.label_name_2.setGeometry(QtCore.QRect(240, 110, 151, 41))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        font.setUnderline(True)
        self.label_name_2.setFont(font)
        self.label_name_2.setObjectName("label_name_2")
        self.label_id_2 = QtWidgets.QLabel(CheckInfo)
        self.label_id_2.setGeometry(QtCore.QRect(240, 200, 151, 41))
        font = QtGui.QFont()
        font.setFamily(".AppleSystemUIFont")
        font.setPointSize(20)
        font.setUnderline(True)
        self.label_id_2.setFont(font)
        self.label_id_2.setObjectName("label_id_2")
        self.pushButton_login_2 = QtWidgets.QPushButton(CheckInfo)
        self.pushButton_login_2.setGeometry(QtCore.QRect(290, 290, 112, 32))
        self.pushButton_login_2.setObjectName("pushButton_login_2")

        self.retranslateUi(CheckInfo)
        QtCore.QMetaObject.connectSlotsByName(CheckInfo)

    def retranslateUi(self, CheckInfo):
        _translate = QtCore.QCoreApplication.translate
        CheckInfo.setWindowTitle(_translate("CheckInfo", "CheckInfo"))
        self.label_title.setText(_translate("CheckInfo", "Please check the following Info"))
        self.label_name.setText(_translate("CheckInfo", "Name:"))
        self.pushButton_login.setText(_translate("CheckInfo", "Yes"))
        self.label_id.setText(_translate("CheckInfo", "ID:"))
        self.label_name_2.setText(_translate("CheckInfo", "MyName"))
        self.label_id_2.setText(_translate("CheckInfo", "MyID"))
        self.pushButton_login_2.setText(_translate("CheckInfo", "No"))


