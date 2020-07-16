from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox
import MySQLdb as mdb
import sys
from history_modified import *
from Utils import DBUtils


# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class History_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(History_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.dbUtils = DBUtils(rootController=self)
        self.ui = Ui_MainWindow_History()
        self.ui.setupUi(self)
        self.connectUserDefinedSlots()

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)

    def gotoHomeWindow(self):
        self.hide()
        home_controller = self.rootController
        dialog = home_controller
        dialog.show()


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    history_controller = History_controller()
    MainWindow = QtWidgets.QMainWindow()
    history_controller.ui.setupUi(MainWindow)
    history_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
