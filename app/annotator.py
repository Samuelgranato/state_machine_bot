import os
import shutil

import cv2
import numpy as np

from app.window import posicionar_janela
from config import ASSET_ANOTACAO_BATCH, ASSET_MOBS_DIR, ASSET_RAW_DIR, DEBUG_MONITOR_INDEX

GRID_COLS = 6
IMG_SIZE = 100
TRASH_DIR = "dataset/trash"

_click_info = {"arquivos": [], "selecionados": set()}


def carregar_imagens_raw():
    arquivos = sorted([f for f in os.listdir(ASSET_RAW_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
    return arquivos[:ASSET_ANOTACAO_BATCH]


def construir_grade(arquivos, selecionados):
    total = len(arquivos)
    linhas = (total + GRID_COLS - 1) // GRID_COLS
    grade = np.ones((linhas * IMG_SIZE, GRID_COLS * IMG_SIZE, 3), dtype=np.uint8) * 30

    for idx, nome in enumerate(arquivos):
        img_path = os.path.join(ASSET_RAW_DIR, nome)
        img = cv2.imread(img_path)
        if img is None:
            continue
        thumb = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
        x = (idx % GRID_COLS) * IMG_SIZE
        y = (idx // GRID_COLS) * IMG_SIZE

        border_color = (0, 255, 0) if idx in selecionados else (100, 100, 100)
        cv2.rectangle(thumb, (0, 0), (IMG_SIZE - 1, IMG_SIZE - 1), border_color, 2)
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


def mover_imagens(arquivos, selecionados, classe):
    destino_ok = os.path.join(ASSET_MOBS_DIR, classe)
    destino_trash = TRASH_DIR
    os.makedirs(destino_ok, exist_ok=True)
    os.makedirs(destino_trash, exist_ok=True)

    for idx, nome in enumerate(arquivos):
        origem_path = os.path.join(ASSET_RAW_DIR, nome)
        if idx in selecionados:
            destino_path = os.path.join(destino_ok, nome)
        else:
            destino_path = os.path.join(destino_trash, nome)
        shutil.move(origem_path, destino_path)
        print(f"[✓] Movido para: {destino_path}")


def on_mouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        col = x // IMG_SIZE
        row = y // IMG_SIZE
        idx = row * GRID_COLS + col
        if idx < len(_click_info["arquivos"]):
            if idx in _click_info["selecionados"]:
                _click_info["selecionados"].remove(idx)
            else:
                _click_info["selecionados"].add(idx)


def run_anotador():
    arquivos = carregar_imagens_raw()
    if not arquivos:
        print("Nenhuma imagem para anotar.")
        return

    print("\nClasse para anotar os assets:")
    classe = input("Digite o nome da classe (ou Enter para sair): ").strip()
    if not classe:
        return

    janela = "Anotação de Assets"
    cv2.namedWindow(janela)
    posicionar_janela(janela, DEBUG_MONITOR_INDEX)
    cv2.setMouseCallback(janela, on_mouse)

    while True:
        arquivos = carregar_imagens_raw()
        if not arquivos:
            print("Fim das imagens.")
            break

        _click_info["arquivos"] = arquivos
        _click_info["selecionados"] = set()

        while True:
            grade = construir_grade(arquivos, _click_info["selecionados"])
            cv2.imshow(janela, grade)

            tecla = cv2.waitKey(50) & 0xFF
            if tecla == 13:  # Enter
                mover_imagens(arquivos, _click_info["selecionados"], classe)
                break
            elif tecla == 27:  # Esc
                print("Anotação encerrada.")
                cv2.destroyWindow(janela)
                return
