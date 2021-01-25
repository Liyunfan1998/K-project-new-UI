import os

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import sys
from Tools.Utils import DBUtils
from Layouts.excercises_modified import *

# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class Exercise_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(Exercise_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.dbUtils = DBUtils(rootController=self)
        self.ui = Ui_MainWindow_Exercises()
        self.ui.setupUi(self)
        self.connectUserDefinedSlots()
        self.setUpComboBox()

    def setUpComboBox(self):
        sql = "select exe from instructionnotes"
        rows = self.dbUtils.DBFetchAll(sql)
        comboList = [str(row[0]) for row in rows]
        self.ui.comboBox_actions.addItems(comboList)
        self.ui.comboBox_actions.activated.connect(self.updateAll)

    def updateAll(self):
        exeName = self.ui.comboBox_actions.currentText().split(': ')[1]
        self.labelExerciseNameUpdate(exeName)
        index = self.ui.comboBox_actions.currentText().split(' ')[1]
        self.videoPlayerUpdate(index=index)

    def videoPlayerUpdate(self, index=1):
        # TODO
        # 好像没有exit掉，多个视频在后台同时播放
        sql = 'select videoExercise from instructionnotes where instructionnotes.index="' + str(index) + '"'
        rows = self.dbUtils.DBFetchAll(sql)
        relativePath = '../Assets/' + str(rows[0][0])
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, relativePath)
        self.videoPlayerController.open_file(filename=filename)

    def bindVideoPlayerController(self, videoPlayerController=None):
        self.videoPlayerController = videoPlayerController

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)

    def labelExerciseNameUpdate(self, text):
        self.ui.label_exerciseName.setText(text)

    def videoOps(self):
        pass

    def gotoHomeWindow(self):
        self.videoPlayerController.exit_video()
        self.hide()
        self.videoCaptureController.closeEvent()
        home_controller = self.rootController
        dialog = home_controller
        dialog.show()

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    exercise_controller = Exercise_controller()
    MainWindow = QtWidgets.QMainWindow()
    exercise_controller.ui.setupUi(MainWindow)
    exercise_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
