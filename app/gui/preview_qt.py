import sys
import threading

import cv2
import numpy as np
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget

from app.engine.orchestrator import run_bot_loop
from app.engine.state import criar_estado


class TelaPreview(QWidget):
    def __init__(self, estado):
        super().__init__()
        self.estado = estado
        self.setWindowTitle("Bot Preview - PyQt")
        self.setGeometry(100, 100, 800, 600)

        self.label_imagem = QLabel(self)
        self.label_imagem.setFixedSize(800, 600)

        layout = QVBoxLayout()
        layout.addWidget(self.label_imagem)
        self.setLayout(layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.atualizar_frame)
        self.timer.start(30)  # ~33 FPS

    def atualizar_frame(self):
        frame = self.estado.get("__frame")
        if frame is None:
            return

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


if __name__ == "__main__":
    estado = criar_estado()
    threading.Thread(target=run_bot_loop, args=(estado,), daemon=True).start()
    # run_pyqt_preview(estado)
