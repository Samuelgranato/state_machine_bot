import sys

import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from screeninfo import get_monitors

from capture.screen import capturar_tela
from config import MONITOR_INDEX


class TelaPreview(QWidget):
    def __init__(self, estado):
        super().__init__()
        self.estado = estado
        self.setWindowTitle("Bot Preview - PyQt")
        self.setGeometry(100, 100, 800, 600)

        # layout
        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.label_imagem)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_frame)
        self.timer.start(30)  # ~33 FPS

    def recortar_monitor(self, frame):
        monitores = get_monitors()
        if 0 <= MONITOR_INDEX < len(monitores):
            m = monitores[MONITOR_INDEX]
            return frame[m.y : m.y + m.height, m.x : m.x + m.width]
        return frame

    def atualizar_frame(self):
        frame = capturar_tela()
        frame = self.recortar_monitor(frame)

        # Aqui você pode desenhar, reconhecer, etc (diretamente no frame do orchestrator)
        self.estado["__frame"] = frame.copy()

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame_rgb.shape
        bytes_per_line = ch * w
        q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
        self.label_imagem.setPixmap(QPixmap.fromImage(q_img))


def run_pyqt_preview(estado):
    app = QApplication(sys.argv)
    preview = TelaPreview(estado)
    preview.show()
    sys.exit(app.exec_())
