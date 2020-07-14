from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import MySQLdb as mdb
import sys
from instructions_modified import *


class Instruction_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(Instruction_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.ui = Ui_MainWindow_Instructions()
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

    def textBrowserInstructionsPerExerciseUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    def listWidget_exerciseListUpdate(self):
        sql = ""
        rows = self.fetchAllWithSQL(sql)
        for row in rows:
            # TODO
            print(row)

    def videoOps(self):
        pass

    def gotoHomeWindow(self):
        self.hide()
        home_controller = self.rootController
        dialog = home_controller
        # if dialog.exec():
        #     pass  # do stuff on success
        # self.show()

        dialog.show()

    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'rehab')
        except mdb.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)


class VideoController:
    def __init__(self):
        pass

    def pause(self):
        pass

    def play(self):
        pass

    def toggleProcessBar(self):
        pass

    def screenShot(self):
        pass


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    instruction_controller = Instruction_controller()
    MainWindow = QtWidgets.QMainWindow()
    instruction_controller.ui.setupUi(MainWindow)
    instruction_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
