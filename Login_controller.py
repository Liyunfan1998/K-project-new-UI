from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox
import MySQLdb as mdb
import sys
from login import *
from Home_controller import *


class Login_controller(QMainWindow):
    def __init__(self, parent=None):
        super(Login_controller, self).__init__(parent)
        self.ui = Ui_Kproj()
        self.ui.setupUi(self)
        self.parsePrams = {}

    def connectUserDefinedSlots(self):
        self.ui.checkBox_isClinician.stateChanged.connect(self.userTypeFlip)
        self.ui.pushButton_login.clicked.connect(self.submit_form)

    def submit_form(self):
        ui = self.ui
        # if 单选 type
        self.parsePrams['name'] = ui.label_name.text()
        self.parsePrams['gender'] = ui.label_gender.text()

        # TODO
        # create a gender text edit component!

        self.parsePrams['id'] = ui.label_id.text()
        type = "PatientLogIn"
        userInput = {'First Name': self.parsePrams['name'], 'Gender': self.parsePrams['gender']}
        self.gotoHomeWindow()

        """
        # check with database
        con = self.DBConnection()

        if self.DBValidation(con=con, userInput=userInput, type=type):
            self.gotoHomeWindow()
        else:
            QMessageBox.about(self, 'Validation', 'Information Mismatch! Please check again!')
        """

    def userTypeFlip(self, state):
        if state == QtCore.Qt.Checked:
            self.parsePrams['userType'] = "ClinicianLogIn"
            self.ui.pushButton_login.setText("Log in as clinician")
        else:
            self.parsePrams['userType'] = "PatientLogIn"
            self.ui.pushButton_login.setText("Log in as patient")

    def gotoHomeWindow(self):
        self.hide()
        home_controller = Home_controller(parent=self)
        dialog = home_controller
        # if dialog.exec():
        #     pass  # do stuff on success
        # self.show()
        dialog.show()

    def DBConnection(self):
        try:
            con = mdb.connect('localhost', 'root', '', 'rehab')
            return con

        except mdb.Error as e:
            QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

    def DBValidation(self, con, userInput, type="PatientLogIn"):
        if type == "PatientLogIn":
            with con:
                cur = con.cursor()
                sql = "SELECT"
                cur.execute(sql)
                jsonDataFoundByID = cur.fetchone()
                name = jsonDataFoundByID['Name']
                gender = jsonDataFoundByID['Gender']

                userInputName = userInput['Name']
                userInputGender = userInput['Gender']
                valid = name == userInputName and gender == userInputGender
                return valid
        elif type == "ClinicianLogIn":
            with con:
                cur = con.cursor()
                sql = "SELECT"
                cur.execute(sql)
                jsonDataFoundByID = cur.fetchone()
                name = jsonDataFoundByID['Name']

                userInputName = userInput['Name']
                valid = name == userInputName
                return valid


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_controller = Login_controller()
    # MainWindow = QtWidgets.QMainWindow()
    # login_controller.ui.setupUi(MainWindow)
    login_controller.connectUserDefinedSlots()
    # MainWindow.show
    login_controller.show()
    app.exec_()
