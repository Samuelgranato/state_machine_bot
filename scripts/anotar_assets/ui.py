import cv2
import numpy as np

from app.window import posicionar_janela
from config import DEBUG_MONITOR_INDEX, DISPLAY_SCALE

GRID_COLS = 6
IMG_SIZE = 100
_click_info = {}


def construir_grade(estado):
    arquivos = estado["arquivos"]
    selecionados = estado["selecionados"]

    total = len(arquivos)
    linhas = (total + GRID_COLS - 1) // GRID_COLS
    grade = np.ones((linhas * IMG_SIZE, GRID_COLS * IMG_SIZE, 3), dtype=np.uint8) * 30

    for idx, nome in enumerate(arquivos):
        img = cv2.imread(f"dataset/raw/{nome}")
        if img is None:
            continue
        thumb = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        x = (idx % GRID_COLS) * IMG_SIZE
        y = (idx // GRID_COLS) * IMG_SIZE

        cor = (0, 255, 0) if idx in selecionados else (100, 100, 100)
        cv2.rectangle(thumb, (0, 0), (IMG_SIZE - 1, IMG_SIZE - 1), cor, 2)
        grade[y : y + IMG_SIZE, x : x + IMG_SIZE] = thumb
        cv2.putText(
            grade,
            str(idx + 1),
            (x + 3, y + 15),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (255, 255, 255),
            1,
        )

    return grade


def configurar_mouse(estado):
    _click_info["estado"] = estado
    cv2.namedWindow(estado["janela"])  # 💥 criar janela ANTES do setMouseCallback
    cv2.setMouseCallback(estado["janela"], on_mouse)
    posicionar_janela(estado["janela"], DEBUG_MONITOR_INDEX)


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        estado = _click_info["estado"]

        # Corrige coordenadas com base na escala de exibição
        x_real = int(x / DISPLAY_SCALE)
        y_real = int(y / DISPLAY_SCALE)

        col = x_real // IMG_SIZE
        row = y_real // IMG_SIZE
        idx = row * GRID_COLS + col

        if idx < len(estado["arquivos"]):
            if idx in estado["selecionados"]:
                estado["selecionados"].remove(idx)
            else:
                estado["selecionados"].add(idx)
