from Layouts.home_modified import *
from Controllers.Instruction_controller import *
from Controllers.Exercise_controller import *
from Controllers.History_controller import *
from Tools.Utils import *


class Home_controller(QDialog):
    def __init__(self, parent=None):
        super(Home_controller, self).__init__(parent)
        self.dbUtils = DBUtils(rootController=self)
        self.ui = Ui_MainWindow_Home()
        self.ui.setupUi(self)
        self.connectUserDefinedSlots()
        self.loadLogo()
        self.controllers = {}

    def loadLogo(self):
        self.image = QPixmap('Assets/logo.jpeg').scaled(150, 150, QtCore.Qt.KeepAspectRatio)
        self.ui.graphicsView_logo.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.ui.graphicsView_logo.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.ui.graphicsView_logo.setScene(self.ui.graphicsView_logo.scene)

    def connectUserDefinedSlots(self):
        self.ui.pushButton_instructions.clicked.connect(self.gotoInstructionsWindow)
        self.ui.pushButton_excercises.clicked.connect(self.gotoExercisesWindow)
        self.ui.pushButton_history.clicked.connect(self.gotoHistoryWindow)

    # should this function be the base model for displaying?
    def fetchAllWithSQL(self, sql, displayWidget=None):
        return self.dbUtils.DBFetchAll(sql)

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
        instruction_controller.videoPlayerController = VideoPlayerController(instruction_controller)
        instruction_controller.bindVideoPlayerController(instruction_controller.videoPlayerController)
        dialog = instruction_controller
        dialog.show()

    def gotoExercisesWindow(self):
        self.hide()
        exercise_controller = Exercise_controller(parent=self, rootController=self)
        exercise_controller.videoCaptureController = VideoCaptureController(exercise_controller)
        exercise_controller.videoPlayerController = VideoPlayerController(exercise_controller)
        exercise_controller.bindVideoPlayerController(exercise_controller.videoPlayerController)
        dialog = exercise_controller
        dialog.show()

    def gotoHistoryWindow(self):
        self.hide()
        history_controller = History_controller(parent=self, rootController=self)
        dialog = history_controller
        dialog.show()


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_controller = Home_controller()
    MainWindow = QtWidgets.QMainWindow()
    home_controller.ui.setupUi(MainWindow)
    home_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
