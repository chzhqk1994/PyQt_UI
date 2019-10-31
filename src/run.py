import sys
import cv2
import time

from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import QTimer
from PyQt5 import uic

form_class1 = uic.loadUiType("main.ui")[0]


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Find video file'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.openFileNameDialog()

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        self.fileName, _ = QFileDialog.getOpenFileName(self, "Find video file", "",
                                                       "All Files (*);;Python Files (*.py)", options=options)


class MainWindow(QWidget, form_class1):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.setupUi(self)

        self.cap = None
        self.fileName = ''

        self.find_video_bt.clicked.connect(self.findVideoFile)

        self.timer = QTimer()
        self.timer.timeout.connect(self.viewCam)
        self.start_bt.clicked.connect(self.controlTimer)

    # video 를 선택하기 위한 창을 보여줌
    def findVideoFile(self):
        self.app = App()
        self.app.show()
        self.video_file_path_label.setText(self.app.fileName)
        self.fileName = self.app.fileName
        self.app.close()
        if self.app.fileName == '':
            return

        self.cap = cv2.VideoCapture(self.app.fileName)
        # video file load 후 첫 번재 프레임을 화면에 출력
        ret, frame = self.cap.read()
        try:
            self.viewer_drawer(frame)
        except TypeError:
            pass

    def viewCam(self):
        # prev_time = time.time()
        # cur_time = time.time()
        # sec = cur_time - prev_time
        #
        # self.cap.set(cv2.CAP_PROP_POS_FRAMES, sec * 30)
        ret, frame = self.cap.read()

        if ret:

            # get image infos
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            # create QImage from image
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)

            width = self.image_label.geometry().getRect()[2]
            height = self.image_label.geometry().getRect()[3]

            self.image_label.setPixmap(QPixmap.fromImage(qImg).scaled(width, height))

        else:
            self.timer.stop()
            self.cap.release()
            self.start_bt.setText("Start")

    def viewer_drawer(self, frame):
        try:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            height, width, channel = frame.shape
            step = channel * width
            qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)

            # for resize
            width = self.image_label.geometry().getRect()[2]
            height = self.image_label.geometry().getRect()[3]
            self.image_label.setPixmap(QPixmap.fromImage(qImg).scaled(width, height))

        except:
            pass

    # start/stop timer
    def controlTimer(self):
        if not self.timer.isActive():
            self.cap = cv2.VideoCapture(self.fileName)
            self.timer.start(20)
            self.start_bt.setText("Stop")

        else:
            self.timer.stop()
            self.cap.release()
            self.start_bt.setText("Start")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
