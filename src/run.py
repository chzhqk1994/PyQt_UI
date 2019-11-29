import sys
import cv2
import time

from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget
from PyQt5.QtGui import QImage, QPixmap, QPainter, QBrush, QColor, QPainterPath
from PyQt5.QtCore import QTimer, QRect, QPoint, pyqtSignal, QSize
from PyQt5 import uic

roi_coord = []

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


class Drawer(QWidget):
    global roi_coord
    newPoint = pyqtSignal(QPoint)

    def __init__(self, roi_label, parent=None):
        QWidget.__init__(self, parent)
        self.begin = QPoint()
        self.end = QPoint()
        self.path = QPainterPath()
        self.roi_label = roi_label

    def paintEvent(self, event):
        qp = QPainter(self)
        br = QBrush(QColor(100, 10, 10, 40))
        qp.setBrush(br)
        qp.drawRect(QRect(self.begin, self.end))

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = event.pos()
        self.update()
        roi_coord.clear()

        # beginning coord of Rect
        roi_coord.append([event.pos().x(), event.pos().y()])

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.newPoint.emit(event.pos())
        self.update()

    def mouseReleaseEvent(self, event):
        # End coord of Rect
        roi_coord.append([event.pos().x(), event.pos().y()])

    def sizeHint(self):
        return QSize(self.roi_label.geometry().getRect()[2], self.roi_label.geometry().getRect()[3])


class MainWindow(QWidget, form_class1):
    def __init__(self):
        # call QWidget constructor
        super().__init__()
        self.setupUi(self)

        self.cap = None
        self.fileName = ''

        self.find_video_bt.clicked.connect(self.findVideoFile)

        drawer = Drawer(self, self.roi_label)
        drawer.newPoint.connect(lambda p: self.posi_label.setText('Coordinates: ( %d : %d )' % (p.x(), p.y())))

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

            # ROI 사각형이 그려졌다면 if 문 실행
            if len(roi_coord) == 2:
                # ROI 값을 추출
                YMAX = roi_coord[1][1]
                YMIN = roi_coord[0][1]
                XMAX = roi_coord[1][0]
                XMIN = roi_coord[0][0]

                # frame 을 자르기 전에 label widget 의 크기에 맞춰 resize 한다
                lb_width = self.image_label.geometry().getRect()[2]
                lb_height = self.image_label.geometry().getRect()[3]
                frame = cv2.resize(frame, dsize=(lb_width, lb_height), interpolation=cv2.INTER_AREA)

                # resize 된 프레임을 crop
                frame = frame[YMIN:YMAX, XMIN:XMAX]

                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                height, width, channel = frame.shape
                step = channel * width
                qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)

                # label 에 ROI 영역의 이미지 출력
                lb_width = self.image_label_2.geometry().getRect()[2]
                lb_height = self.image_label_2.geometry().getRect()[3]
                self.image_label_2.setPixmap(QPixmap.fromImage(qImg).scaled(lb_width, lb_height))

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
