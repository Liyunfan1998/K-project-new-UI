import cv2
from PyQt5.QtGui import QTextCharFormat, QIcon, QPalette, QImage
from PyQt5.QtWidgets import QApplication, QDialog, QPushButton, QMessageBox, QCalendarWidget, QMessageBox, QWidget, \
    QStyle, QLabel, QWidget, QHBoxLayout, QVBoxLayout, QSlider, QStyle, QSizePolicy, QFileDialog
from PyQt5.QtCore import Qt, QDate, QUrl, QThread, pyqtSignal, pyqtSlot
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import MySQLdb as mdb
import sys


# To replace the repetitive code in the controllers
class DBUtils(object):
    def __init__(self, rootController=None):
        self.con = None
        self.rootController = rootController

    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', '', 'rehab')
        except mdb.Error as e:
            QMessageBox.about(self.rootController, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

    """
    def DBFetchJsonOne(self, sql):
        with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            jsonFetchedBySQL = cur.fetchone()
            return jsonFetchedBySQL
    """

    def DBFetchAll(self, sql):
        with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            rows = cur.fetchall()
            return rows

    def DBValidation(self, userInput, type="PatientLogIn"):
        con = self.con
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


class MyCalendar(QCalendarWidget):
    def __init__(self, rootConrtoller=None):
        super().__init__(rootConrtoller.centralwidget)
        self.begin_date = None
        self.end_date = None

        self.highlight_format = QTextCharFormat()
        self.highlight_format.setBackground(self.palette().brush(QPalette.Highlight))
        self.highlight_format.setForeground(self.palette().color(QPalette.HighlightedText))

        self.clicked.connect(self.highLightDate)
        # TODO
        # use DB to fetch the dates
        self.markedDates = ['2020-7-13', '2020-7-15', '2020-7-17']
        for date in self.markedDates:
            ymd = date.split('-')
            yy = int(ymd[0])
            mm = int(ymd[1])
            dd = int(ymd[2])
            date = QDate(yy, mm, dd)
            self.highLightDate(date)
        print(super().dateTextFormat())

    def format_range(self, format):
        if self.begin_date and self.end_date:
            d0 = min(self.begin_date, self.end_date)
            d1 = max(self.begin_date, self.end_date)
            while d0 <= d1:
                self.setDateTextFormat(d0, format)
                d0 = d0.addDays(1)

    def highLightDate(self, date):
        self.begin_date = date
        self.end_date = date
        # reset highlighting of previously selected date range
        self.format_range(QTextCharFormat())
        """
        if QApplication.instance().keyboardModifiers() & Qt.ShiftModifier and self.begin_date:
            self.end_date = date
            # set highilighting of currently selected date range
            self.format_range(self.highlight_format)
        else:
            self.begin_date = date
            self.end_date = None
        """
        self.end_date = date
        # set highilighting of currently selected date range
        self.format_range(self.highlight_format)


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

    def open_file(self, filename='/Users/liyunfan/Desktop/深度学习/NYU_summer_intern/K-project-new-UI/1.mp4'):
        # filename, _ = QFileDialog.getOpenFileName(self.rootUIController, "Open Video")
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
        print("pos changed", position)
        self.rootUIController.mediaPlayer.setPosition(position)

    def screenShot(self):
        pass


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
        self.rootUIController = rootUIController
        # create a label
        rootUIController.label = QLabel(rootUIController)
        self.setFramePoisition(X=500, Y=410, W=480, H=360)
        self.th = th = Thread(rootUIController)
        th.changePixmap.connect(rootUIController.setImage)
        th.start()

    def setFramePoisition(self, X=500, Y=410, W=480, H=360):
        # parse the coords as parameters
        self.rootUIController.label.move(X, Y)
        self.rootUIController.label.resize(W, H)

    def closeEvent(self):
        self.th.stop()

    def screenShot(self):
        pass
