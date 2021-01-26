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
        self.user_id = "defaultUser"
        self.loadLogo()
        self.controllers = {"history_controller": None, "exercise_controller": None, "instruction_controller": None}
        self.assets_base = '../Assets/'

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
        if self.controllers['instruction_controller'] is None:
            print("create instruction_controller")
            instruction_controller = Instruction_controller(parent=self, rootController=self)
            instruction_controller.videoPlayerController = VideoPlayerController(instruction_controller,
                                                                                 fileRelativePath=self.assets_base + 'video/tr1.mp4')
            instruction_controller.bindVideoPlayerController(instruction_controller.videoPlayerController, )
            self.controllers['instruction_controller'] = instruction_controller
        dialog = self.controllers['instruction_controller']
        dialog.show()

    def gotoExercisesWindow(self):
        self.hide()
        if self.controllers['exercise_controller'] is None:
            print("create exercise_controller")
            exercise_controller = Exercise_controller(parent=self, rootController=self)
            exercise_controller.videoCaptureController = VideoCaptureController(exercise_controller)
            exercise_controller.videoPlayerController = VideoPlayerController(exercise_controller,
                                                                              fileRelativePath=self.assets_base + 'video/ex1.mpg')
            exercise_controller.bindVideoPlayerController(exercise_controller.videoPlayerController)
            self.controllers['exercise_controller'] = exercise_controller
        else:
            self.controllers['exercise_controller'].videoCaptureController.restart()
        dialog = self.controllers['exercise_controller']
        dialog.show()

    def gotoHistoryWindow(self):
        self.hide()
        if self.controllers['history_controller'] is None:
            print("create history_controller")
            history_controller = History_controller(parent=self, rootController=self)
            self.controllers['history_controller'] = history_controller
        dialog = self.controllers['history_controller']
        dialog.show()

    def setUserID(self, user_id):
        self.user_id = user_id


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    home_controller = Home_controller()
    MainWindow = QtWidgets.QMainWindow()
    home_controller.ui.setupUi(MainWindow)
    home_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
