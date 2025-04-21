import sys

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget
from screeninfo import get_monitors

from config import GAME_MONITOR_INDEX


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        monitores = get_monitors()
        monitor = monitores[GAME_MONITOR_INDEX]
        self.setGeometry(monitor.x, monitor.y, monitor.width, monitor.height)

        self.rois = []
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0, 200))
        painter.setBrush(QColor(255, 0, 0, 80))
        for x, y, w, h in self.rois:
            painter.drawRect(x, y, w, h)


def start_overlay(shared_rois):
    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.show()

    def atualizar_rois():
        overlay.rois = shared_rois()

    timer = QTimer()
    timer.timeout.connect(atualizar_rois)
    timer.start(30)

    sys.exit(app.exec_())
