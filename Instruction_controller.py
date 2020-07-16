import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QLabel, QListWidgetItem
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import MySQLdb as mdb
from Utils import DBUtils, VideoPlayerController
import sys
from random import sample
from instructions_modified import *


# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class Instruction_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(Instruction_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.dbUtils = DBUtils(rootController=self)
        self.ui = Ui_MainWindow_Instructions()
        self.ui.setupUi(self)
        self.listWidget_exerciseListUpdate()
        self.textBrowserInstructionsPerExerciseUpdate()
        self.connectUserDefinedSlots()

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)
        self.ui.pushButton_VideoStop.clicked.connect(self.updateAll)

    def updateAll(self):
        self.textBrowserInstructionsPerExerciseUpdate()
        self.listWidget_exerciseListUpdate()
        self.videoPlayerController.exit_video()

    def textBrowserInstructionsPerExerciseUpdate(self):
        sql = ""
        # rows = self.dbUtils.DBFetchAll(sql)
        rows = sample(range(10, 30), 5)
        self.ui.textBrowser.clear()
        self.ui.textBrowser.insertPlainText(str(rows))

    def listWidget_exerciseListUpdate(self):
        sql = ""
        # rows = self.dbUtils.DBFetchAll(sql)
        rows = sample(range(10, 30), 5)
        self.ui.listWidget.clear()
        for row in rows:
            # TODO
            QListWidgetItem(str(row), self.ui.listWidget)
            # print(row)

    def videoOps(self):
        pass

    def gotoHomeWindow(self):
        self.hide()
        home_controller = self.rootController
        dialog = home_controller

        dialog.show()

    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'rehab')
        except mdb.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    instruction_controller = Instruction_controller()
    MainWindow = QtWidgets.QMainWindow()
    instruction_controller.ui.setupUi(MainWindow)
    instruction_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
