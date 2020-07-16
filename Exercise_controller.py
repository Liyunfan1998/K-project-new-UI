import cv2
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QLabel, QWidget, QHBoxLayout, QVBoxLayout, \
    QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtCore import QThread, Qt, pyqtSignal, pyqtSlot, QUrl
from PyQt5.QtGui import QImage, QPixmap
import MySQLdb as mdb
import sys
from excercises_modified import *
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtGui import QIcon, QPalette


# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class Exercise_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(Exercise_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
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


class VideoCaptureController:  # instantiation in Home_controller
    def __init__(self, rootUIController):
        # create a label
        rootUIController.label = QLabel(rootUIController)
        # or can parse the coords as parameters
        rootUIController.label.move(500, 410)
        rootUIController.label.resize(480, 360)
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


class VideoPlayerController(QWidget):
    def __init__(self, rootUIController):
        super().__init__()
        self.rootUIController = rootUIController
        # create media player object
        self.rootUIController.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        # create videowidget object
        self.rootUIController.videowidget = QVideoWidget()
        self.rootUIController.ui.verticalLayout_videoPlayer.addWidget(self.rootUIController.videowidget)

        self.rootUIController.ui.pushButton_videoPlay.setEnabled(True)
        self.rootUIController.ui.pushButton_videoPlay.setIcon(
            self.rootUIController.style().standardIcon(QStyle.SP_MediaPlay))
        self.rootUIController.ui.pushButton_videoPlay.clicked.connect(self.play_video)
        # create slider
        self.rootUIController.ui.horizontalSlider_videoPos.sliderMoved.connect(self.set_position)

        self.rootUIController.mediaPlayer.setVideoOutput(self.rootUIController.videowidget)
        # media player signals
        self.rootUIController.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.rootUIController.mediaPlayer.positionChanged.connect(self.position_changed)
        self.rootUIController.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.open_file()

    def open_file(self):
        print("open file")
        # filename, _ = QFileDialog.getOpenFileName(self.rootUIController, "Open Video")
        filename = '/Users/liyunfan/Desktop/深度学习/NYU_summer_intern/K-project-new-UI/1.mp4'
        if filename != '':
            self.rootUIController.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.rootUIController.ui.pushButton_videoPlay.setEnabled(True)

    def play_video(self):
        if self.rootUIController.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.rootUIController.mediaPlayer.pause()
        else:
            self.rootUIController.mediaPlayer.play()

    def mediastate_changed(self, state):
        if self.rootUIController.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.rootUIController.ui.pushButton_videoPlay.setIcon(
                self.rootUIController.style().standardIcon(QStyle.SP_MediaPause))

        else:
            self.rootUIController.ui.pushButton_videoPlay.setIcon(
                self.rootUIController.style().standardIcon(QStyle.SP_MediaPlay))

    def position_changed(self, position):
        self.rootUIController.ui.horizontalSlider_videoPos.setValue(position)

    def duration_changed(self, duration):
        self.rootUIController.ui.horizontalSlider_videoPos.setRange(0, duration)

    def set_position(self, position):
        self.rootUIController.mediaPlayer.setPosition(position)

    def handle_errors(self):
        self.rootUIController.ui.pushButton_videoPlay.setEnabled(False)

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
