import cv2
import numpy as np

from app.window import cv2_debug
from config import MOTION_MAX_AREA, MOTION_MIN_AREA, ROI_LIMIT


def detectar_movimentos(frame_anterior, frame_atual, estado=None, debug=False):
    frame_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(frame_gray, (5, 5), 0)

    regioes = []

    if frame_anterior is not None:
        delta = cv2.absdiff(frame_anterior, blur)
        delta = cv2.GaussianBlur(delta, (3, 3), 0)

        # Threshold fixo
        _, thresh = cv2.threshold(delta, 0, 255, cv2.THRESH_BINARY)

        # Dilata para unir regiões próximas (evita fragmentação)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
        dilated = cv2.dilate(thresh, kernel, iterations=3)

        contornos, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            area = cv2.contourArea(contorno)
            if area < MOTION_MIN_AREA or area > MOTION_MAX_AREA:
                continue
            x, y, w, h = cv2.boundingRect(contorno)
            if w / h > 5 or h / w > 5:
                continue
            regioes.append((x, y, w, h))

        if debug:
            print(f"[DEBUG] {len(regioes)} ROIs detectadas via dilated-contours")
            debug_frame = frame_atual.copy()
            for x, y, w, h in regioes:
                cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)

            cv2_debug("Frame Atual", frame_atual, estado)
            cv2_debug("Delta", delta, estado)
            cv2_debug("Threshold", thresh, estado)
            cv2_debug("Dilated", dilated, estado)
            cv2_debug("ROIs", debug_frame, estado)

    if len(regioes) > ROI_LIMIT:
        print("movimento suspeito detectado (muito ruído) — ignorando tudo")
        regioes = []

    return blur, regioes
