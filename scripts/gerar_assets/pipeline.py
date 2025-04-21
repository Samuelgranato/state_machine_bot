import os
import time
from datetime import datetime

import cv2

from config import ASSET_MAX_SIZE, ASSET_MIN_SIZE, ASSET_SALVAR_INTERVALO
from detection.motion import detectar_movimentos

SAVE_DIR = "dataset/raw"


def salvar_roi(imagem, x, y, w, h):
    roi = imagem[y : y + h, x : x + w]
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join(SAVE_DIR, f"asset_{timestamp}.png")
    cv2.imwrite(filename, roi)
    print(f"[+] Asset salvo: {filename} ({w}x{h})")


def coletar_e_salvar_rois(estado):
    frame_atual = estado["frame_atual"]
    frame_anterior = estado["frame_anterior"]

    frame_anterior, regioes = detectar_movimentos(frame_anterior, frame_atual, debug=False)
    estado["frame_anterior"] = frame_anterior
    estado["regioes"] = regioes

    agora = time.time()
    if agora - estado["ultimo_salvamento"] < ASSET_SALVAR_INTERVALO:
        return

    # frame_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)
    frame_gray = frame_atual

    for x, y, w, h in regioes:
        if w < ASSET_MIN_SIZE or h < ASSET_MIN_SIZE:
            continue
        if w > ASSET_MAX_SIZE or h > ASSET_MAX_SIZE:
            continue

        salvar_roi(frame_gray, x, y, w, h)
        cv2.rectangle(frame_atual, (x, y), (x + w, y + h), (255, 0, 0), 1)

    estado["ultimo_salvamento"] = agora
