import time

import cv2
from PyQt5.QtGui import QTextCharFormat, QIcon, QPalette, QImage
from PyQt5.QtWidgets import QCalendarWidget, QMessageBox, QLabel, QWidget, QStyle
from PyQt5.QtCore import Qt, QDate, QUrl, QThread, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
import MySQLdb as mdb
from torchvision import transforms
import torch
from PIL import Image, ImageDraw
from sys import exit
from numpy import asarray, zeros
import os.path
from Tools.embedded_inference import embedded_inference
from Tools.stacked_hourglass import hg1, HumanPosePredictor


# To replace the repetitive code in the controllers
class DBUtils(object):
    def __init__(self, rootController=None):
        self.con = None
        self.rootController = rootController
        self.DBConnection()

    def DBConnection(self):
        try:
            self.con = mdb.connect('localhost', 'root', 'yun2' + 'fan1', 'NYU')
        except mdb.Error as e:
            QMessageBox.about(self.rootController, 'Connection', 'Failed To Connect Database')
            sys.exit(1)

    def DBFetchAll(self, sql):
        cur = self.con.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        return rows

    def DBValidation(self, userInput):
        # Used when debugging, comment off!
        return True

        if 'Name' not in userInput or 'Type' not in userInput or 'ID' not in userInput:
            return False
        if userInput['Name'] == '' or userInput['Type'] == '' or userInput['ID'] == '':
            return False
        cur = self.con.cursor()
        sql = "SELECT * from userpassvalidation where username='" + userInput['Name'] + "' and password='" + \
              userInput['ID'] + "' and type='" + userInput['Type'] + "'"
        print(sql)
        cur.execute(sql + ';')
        jsonDataFoundByID = cur.fetchone()
        valid = jsonDataFoundByID is not None
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
        self.end_date = date
        # set highilighting of currently selected date range
        self.format_range(self.highlight_format)


class VideoPlayerController(QWidget):
    def __init__(self, rootUIController, fileRelativePath):
        super().__init__()
        self.rootUIController = rootUIController
        # create videowidget object
        self.rootUIController.videowidget = QVideoWidget()
        self.rootUIController.ui.verticalLayout_videoPlayer.addWidget(self.rootUIController.videowidget)

        # self.rootUIController.ui.pushButton_videoPlay.setEnabled(False)
        self.rootUIController.ui.pushButton_videoPlay.setIcon(
            self.rootUIController.style().standardIcon(QStyle.SP_MediaPlay))
        self.rootUIController.ui.pushButton_videoPlay.clicked.connect(self.play_video)
        # create slider
        self.rootUIController.ui.horizontalSlider_videoPos.sliderMoved.connect(self.set_position)

        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, fileRelativePath)
        self.open_file(filename=filename)

    def createAndSetupMediaPlayer(self):
        # create media player object
        self.rootUIController.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)
        self.rootUIController.mediaPlayer.setVideoOutput(self.rootUIController.videowidget)
        # media player signals
        self.rootUIController.mediaPlayer.stateChanged.connect(self.mediastate_changed)
        self.rootUIController.mediaPlayer.positionChanged.connect(self.position_changed)
        self.rootUIController.mediaPlayer.durationChanged.connect(self.duration_changed)
        self.rootUIController.ui.pushButton_videoPlay.setIcon(
            self.rootUIController.style().standardIcon(QStyle.SP_MediaPlay))

    def open_file(self, filename):
        self.createAndSetupMediaPlayer()
        print("open")
        self.rootUIController.ui.pushButton_videoPlay.setEnabled(True)
        # filename, _ = QFileDialog.getOpenFileName(self.rootUIController, "Open Video")
        if filename != '':
            self.rootUIController.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(filename)))
            self.set_position(0)
            # TODO
            # Don't play on open!
            self.rootUIController.mediaPlayer.stop()

    def play_video(self):
        print("play/pause")
        if self.rootUIController.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.rootUIController.mediaPlayer.pause()
        else:
            self.rootUIController.mediaPlayer.play()

    def exit_video(self):
        print("exit")
        # self.rootUIController.ui.horizontalSlider_videoPos.setValue(0)
        # self.rootUIController.mediaPlayer.pause()
        self.rootUIController.mediaPlayer.stop()

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
        self.video_inf = embedded_inference()
        self.loader = transforms.Compose([transforms.ToTensor()])
        self.model = hg1(pretrained=True)
        self.predictor = HumanPosePredictor(self.model, device='cpu')
        self.device = torch.device('cpu')

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 256)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 256)
        cap.set(cv2.CAP_PROP_FPS, 10)
        # capture from web cam
        while self._run_flag:
            ret, frame = cap.read()
            if ret:
                rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # https://stackoverflow.com/a/55468544/6622587
                image_tensor = self.loader(rgbImage).unsqueeze(0).to(self.device, torch.float)
                """
                frame: 
                rgbImage: 'numpy.ndarray'
                image_tensor: torch tensor
                """
                joints = self.video_inf.tensor_inference(self.predictor, image_tensor)
                h, w, ch = rgbImage.shape
                bytesPerLine = ch * w
                self.draw_joints(joints, rgbImage)
                convertToQtFormat = QImage(rgbImage.data, w, h, bytesPerLine, QImage.Format_RGB888)
                p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
                self.changePixmap.emit(p)
        # shut down capture system
        cap.release()

    def draw_joints(self, joints, cv2image=None):
        # cv2image = zeros((300, 300, 3)) if cv2image is None
        r = int(cv2image.shape[0] / 100)
        red = (255, 0, 0)
        for joint in joints:
            x = joint[0]
            y = joint[1]
            cv2.circle(cv2image, (x, y), r, red, -1)

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

    def restart(self):
        self.th = th = Thread(self.rootUIController)
        th.changePixmap.connect(self.rootUIController.setImage)
        th.start()

    def setFramePoisition(self, X=500, Y=410, W=480, H=360):
        # parse the coords as parameters
        self.rootUIController.label.move(X, Y)
        self.rootUIController.label.resize(W, H)

    def closeEvent(self):
        self.th.stop()

    def screenShot(self):
        pass
