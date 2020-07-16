from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import MySQLdb as mdb
import sys
from Utils import DBUtils
from excercises_modified import *


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

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)

    def fetchAllWithSQL(self, sql):
        with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

    def labelInstructionsRealTimeUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    # TODO
    # Other update functions to be added

    def videoOps(self):
        pass

    def gotoHomeWindow(self):
        self.hide()
        self.videoCaptureController.closeEvent()
        home_controller = self.rootController
        dialog = home_controller
        dialog.show()

    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'rehab')
        except mdb.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

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
