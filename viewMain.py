# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'viewMain.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_instructions = QtWidgets.QLabel(self.centralwidget)
        self.label_instructions.setGeometry(QtCore.QRect(350, 90, 111, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_instructions.setFont(font)
        self.label_instructions.setObjectName("label_instructions")
        self.graphicsView_logo = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_logo.setGeometry(QtCore.QRect(80, 90, 150, 150))
        self.graphicsView_logo.setObjectName("graphicsView_logo")
        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(330, 90, 20, 471))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.label_title = QtWidgets.QLabel(self.centralwidget)
        self.label_title.setGeometry(QtCore.QRect(260, -10, 311, 81))
        font = QtGui.QFont()
        font.setPointSize(30)
        self.label_title.setFont(font)
        self.label_title.setObjectName("label_title")
        self.label_exercises = QtWidgets.QLabel(self.centralwidget)
        self.label_exercises.setGeometry(QtCore.QRect(350, 240, 101, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_exercises.setFont(font)
        self.label_exercises.setObjectName("label_exercises")
        self.calendarWidget = QtWidgets.QCalendarWidget(self.centralwidget)
        self.calendarWidget.setGeometry(QtCore.QRect(10, 280, 311, 211))
        self.calendarWidget.setObjectName("calendarWidget")
        self.label_history = QtWidgets.QLabel(self.centralwidget)
        self.label_history.setGeometry(QtCore.QRect(350, 380, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_history.setFont(font)
        self.label_history.setObjectName("label_history")
        self.textBrowser_history = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_history.setGeometry(QtCore.QRect(460, 390, 331, 171))
        self.textBrowser_history.setObjectName("textBrowser_history")
        self.textBrowser_instructions = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_instructions.setGeometry(QtCore.QRect(460, 90, 331, 131))
        self.textBrowser_instructions.setObjectName("textBrowser_instructions")
        self.textBrowser_excercises = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser_excercises.setGeometry(QtCore.QRect(460, 240, 331, 131))
        self.textBrowser_excercises.setObjectName("textBrowser_excercises")
        self.pushButton_instructions = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_instructions.setGeometry(QtCore.QRect(340, 120, 112, 51))
        self.pushButton_instructions.setObjectName("pushButton_instructions")
        self.pushButton_excercises = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_excercises.setGeometry(QtCore.QRect(340, 270, 112, 51))
        self.pushButton_excercises.setObjectName("pushButton_excercises")
        self.pushButton_history = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_history.setGeometry(QtCore.QRect(340, 410, 112, 51))
        self.pushButton_history.setObjectName("pushButton_history")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_instructions.setText(_translate("MainWindow", "Instructions"))
        self.label_title.setText(_translate("MainWindow", "Welcome to Kinect ToLf"))
        self.label_exercises.setText(_translate("MainWindow", "Exercises"))
        self.label_history.setText(_translate("MainWindow", "History"))
        self.pushButton_instructions.setText(_translate("MainWindow", "Instruction\n"
"Details"))
        self.pushButton_excercises.setText(_translate("MainWindow", "Excercise\n"
"Details"))
        self.pushButton_history.setText(_translate("MainWindow", "History\n"
"Details"))


