from PyQt5.QtWidgets import QApplication

from login import *


class Login_controller(object):
    def __init__(self):
        self.ui = Ui_Kproj()
        self.parsePrams = {}

    def submit_form(self):
        ui = self.ui
        self.parsePrams['name'] = ui.label_name.text()
        self.parsePrams['id'] = ui.label_id.text()
        # check with database
        # TODO
        if True:
            self.gotoHomeWindow()

    def gotoHomeWindow(self):
        pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_controller = Login_controller()
    MainWindow = QtWidgets.QMainWindow()
    login_controller.ui.setupUi(MainWindow)
    MainWindow.show()
    app.exec_()
