import os

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
        self.textBrowserInstructionsPerExerciseUpdate()
        self.listWidget_exerciseListUpdate()
        self.connectUserDefinedSlots()

    def bindVideoPlayerController(self, videoPlayerController=None):
        self.videoPlayerController = videoPlayerController

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)
        self.ui.pushButton_VideoStop.clicked.connect(self.refresh)

    def refresh(self):
        self.updateAll(index=1)
        defaultItem = self.ui.listWidget.item(0)
        self.ui.listWidget.setCurrentItem(defaultItem)

    def updateAll(self, index=1):
        if index == False: index = 1
        self.textBrowserInstructionsPerExerciseUpdate(index)
        # self.listWidget_exerciseListUpdate()
        self.videoPlayerUpdate(index)

    def videoPlayerUpdate(self, index=1):
        self.videoPlayerController.exit_video()
        # TODO
        # 好像没有exit掉，多个视频在后台同时播放
        sql = 'select videoInstruction from instructionnotes where instructionnotes.index="' + str(index) + '"'
        rows = self.dbUtils.DBFetchAll(sql)
        relativePath = 'NoLongerInUse/' + str(rows[0][0])
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, relativePath)
        self.videoPlayerController.open_file(filename=filename)
        self.videoPlayerController.exit_video()

    def textBrowserInstructionsPerExerciseUpdate(self, index=1):
        sql = 'select ins from instructionnotes where instructionnotes.index="' + str(index) + '"'
        rows = self.dbUtils.DBFetchAll(sql)
        # rows = sample(range(10, 30), 5)
        txt = str(rows[0][0]).replace('\\n', '\n')
        self.ui.textBrowser.clear()
        self.ui.textBrowser.insertPlainText(txt)

    def listWidget_exerciseListUpdate(self):
        sql = "select exe from instructionnotes"
        rows = self.dbUtils.DBFetchAll(sql)
        # rows = sample(range(10, 30), 5)
        self.ui.listWidget.clear()
        for row in rows:
            # TODO
            qlw = QListWidgetItem(str(row[0]), self.ui.listWidget)
            self.ui.listWidget.itemClicked.connect(self.listwidgetItemClicked)
            # qlw.isSelected.connect(self.textBrowserInstructionsPerExerciseUpdate(index=int(row[0][0])))
            # print(row)

    def listwidgetItemClicked(self, item):
        index = item.text().split(' ')[1]
        self.updateAll(index)

    def videoOps(self):
        pass

    def gotoHomeWindow(self):
        self.videoPlayerController.exit_video()
        self.hide()
        home_controller = self.rootController
        dialog = home_controller
        dialog.show()


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    instruction_controller = Instruction_controller()
    MainWindow = QtWidgets.QMainWindow()
    instruction_controller.ui.setupUi(MainWindow)
    instruction_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
