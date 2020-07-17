from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QDialog, QMessageBox, QGraphicsScene, QGraphicsPixmapItem, QListWidgetItem
import sys
from history_modified import *
from Utils import DBUtils
from random import sample


# Note That we have to grant access to the camera if we are using a Mac!
# Either Update your pycharm to 2020.1.3 or use terminal with access settings!

class History_controller(QDialog):
    def __init__(self, parent=None, rootController=None):
        super(History_controller, self).__init__(parent)
        self.rootController = rootController
        self.con = None
        self.dbUtils = DBUtils(rootController=self)
        self.ui = Ui_MainWindow_History()
        self.ui.setupUi(self)
        self.plotAngleHistory()
        self.patientInfoUpdate()
        self.setUpComboBox()
        self.connectUserDefinedSlots()
        self.listWidget_historyUpdate()

    def connectUserDefinedSlots(self):
        self.ui.pushButton_home.clicked.connect(self.gotoHomeWindow)

    def setUpComboBox(self):
        sql = "select exe from instructionnotes"
        rows = self.dbUtils.DBFetchAll(sql)
        comboList = [str(row[0]) for row in rows]
        self.ui.comboBox_actions.addItems(comboList)
        self.ui.comboBox_actions.activated.connect(self.updateAll)

    def updateAll(self):
        exeName = self.ui.comboBox_actions.currentText().replace('Exercise', '').replace(':', '').replace(' ',
                                                                                                          '').lower()
        print(exeName)
        self.listWidget_historyUpdate(exeName=exeName)
        # self.plotAngleHistory()

    def listWidget_historyUpdate(self, exeName='1muscletightingdeepbreath'):
        # TODO
        # Some database table names are inconsistent with the names in the actions table!
        sql = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`='NYU' AND `TABLE_NAME`='" + exeName + "';"
        rows = self.dbUtils.DBFetchAll(sql)
        # rows = sample(range(10, 30), 5)
        self.ui.listWidget_history.clear()
        for row in rows:
            # TODO
            qlw = QListWidgetItem(str(row[0]), self.ui.listWidget_history)
            # self.ui.listWidget.itemClicked.connect(self.plotAngleHistory())
            # print(row)

    def patientInfoUpdate(self):
        sql = ""
        # rows = self.dbUtils.DBFetchAll(sql)
        rows = "Patient:\n\nName: Li Yunfan\nGender: Male\nID=163020"
        self.ui.label_patientInfo.setText(str(rows))

    def plotAngleHistory(self):
        # TODO
        # Dynamic Plot
        self.image = QPixmap('hist.jpg').scaled(901, 750, QtCore.Qt.KeepAspectRatio)
        self.ui.graphicsView_angleDatePlot.scene = QGraphicsScene()  # 创建一个图片元素的对象
        item = QGraphicsPixmapItem(self.image)  # 创建一个变量用于承载加载后的图片
        self.ui.graphicsView_angleDatePlot.scene.addItem(item)  # 将加载后的图片传递给scene对象
        self.ui.graphicsView_angleDatePlot.setScene(self.ui.graphicsView_angleDatePlot.scene)

    def gotoHomeWindow(self):
        self.hide()
        home_controller = self.rootController
        dialog = home_controller
        dialog.show()


# This file should not be ran as main entry!
if __name__ == '__main__':
    app = QApplication(sys.argv)
    history_controller = History_controller()
    MainWindow = QtWidgets.QMainWindow()
    history_controller.ui.setupUi(MainWindow)
    history_controller.connectUserDefinedSlots()
    MainWindow.show()
    app.exec_()
