from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QColor, QPainter
from PyQt5.QtWidgets import QApplication, QWidget


class Overlay(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.Tool)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Full HD por exemplo — você pode calcular via pygetwindow
        self.setGeometry(0, 0, 1920, 1080)

        # Timer para redesenhar a cada 30ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(30)

        self.rois = []  # lista de (x, y, w, h)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setPen(QColor(255, 0, 0, 200))
        painter.setBrush(QColor(255, 0, 0, 80))

        for x, y, w, h in self.rois:
            painter.drawRect(x, y, w, h)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    overlay = Overlay()
    overlay.rois = [(800, 400, 100, 100)]  # exemplo de ROI estática
    overlay.show()
    sys.exit(app.exec_())
