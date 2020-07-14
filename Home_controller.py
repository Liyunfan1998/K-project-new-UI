from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import MySQLdb as mdb
import sys
from home import *


class Home_controller(object):
    def __init__(self):
        super().__init__()
        self.con = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

    def connectUserDefinedSlots(self):
        pass
    # self.ui.checkBox_isClinician.stateChanged.connect(self.userTypeFlip)

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
        pass

    def gotoExercisesWindow(self):
        pass

    def gotoHistoryWindow(self):
        pass

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
