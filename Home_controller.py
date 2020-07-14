from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import MySQLdb as mdb
import sys
from home_modified import *
from Instruction_controller import *
from Exercise_controller import *
from History_controller import *


class Home_controller(QDialog):
    def __init__(self, parent=None):
        super(Home_controller, self).__init__(parent)
        self.con = None
        self.ui = Ui_MainWindow_Home()
        self.ui.setupUi(self)
        self.connectUserDefinedSlots()
        self.controllers = {}

    def connectUserDefinedSlots(self):
        self.ui.pushButton_instructions.clicked.connect(self.gotoInstructionsWindow)
        self.ui.pushButton_excercises.clicked.connect(self.gotoExercisesWindow)
        self.ui.pushButton_history.clicked.connect(self.gotoHistoryWindow)

    def fetchAllWithSQL(self, sql):
        with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

    def textBrowserExcercisesUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    def textBrowserInstructionsUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    def textBrowserHistoryUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    def gotoInstructionsWindow(self):
        self.hide()
        instruction_controller = Instruction_controller(parent=self, rootController=self)
        dialog = instruction_controller
        # if dialog.exec():
        #     pass  # do stuff on success
        # self.show()
        dialog.show()

    def gotoExercisesWindow(self):
        self.hide()
        exercise_controller = Exercise_controller(parent=self, rootController=self)
        exercise_controller.videoCaptureController = VideoCaptureController(exercise_controller)
        dialog = exercise_controller
        dialog.show()

    def gotoHistoryWindow(self):
        self.hide()
        history_controller = History_controller(parent=self, rootController=self)
        dialog = history_controller
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
    home_controller = Home_controller()
    MainWindow = QtWidgets.QMainWindow()
    home_controller.ui.setupUi(MainWindow)
    home_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
