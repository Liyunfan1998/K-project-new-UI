import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QLabel
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot
from PyQt5.QtGui import QImage, QPixmap
import MySQLdb as mdb
import sys
from excercises import *


# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class Exercise_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(Exercise_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.ui = Ui_MainWindow_Exercises()
        self.ui.setupUi(self)
        # self.videoCaptureController = VideoCaptureController(self)
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
        self.videoCaptureController.closeEvent()
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

    @pyqtSlot(QImage)
    def setImage(self, image):
        self.label.setPixmap(QPixmap.fromImage(image))


class Thread(QThread):
    changePixmap = pyqtSignal(QImage)

    def __init__(self, rootUIController):
        super().__init__(rootUIController)
        self._run_flag = True

    def run(self):
        cap = cv2.VideoCapture(0)
        self.cap = cap
        # capture from web cam
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                # https://stackoverflow.com/a/55468544/6622587
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        # shut down capture system
        cap.release()

    def stop(self):
        """Sets run flag to False and waits for thread to finish"""
        self._run_flag = False
        self.wait()


class VideoCaptureController:
    def __init__(self, rootUIController):
        # create a label
        rootUIController.label = QLabel(rootUIController)
        rootUIController.label.move(280, 120)
        rootUIController.label.resize(640, 480)
        self.th = th = Thread(rootUIController)
        th.changePixmap.connect(rootUIController.setImage)
        th.start()

    def closeEvent(self, event=None):
        self.th.stop()
        # event.accept()

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
    exercise_controller = Exercise_controller()
    MainWindow = QtWidgets.QMainWindow()
    exercise_controller.ui.setupUi(MainWindow)
    exercise_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
