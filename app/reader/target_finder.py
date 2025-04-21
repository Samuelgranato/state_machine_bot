import os

import cv2
import numpy as np

from app.window import cv2_debug


def preprocess_image(img, scale=1):
    if scale != 1:
        img = cv2.resize(img, (0, 0), fx=scale, fy=scale)
    return img  # mantém em BGR para match com cor


def carregar_templates(pasta_templates, scale=1):
    templates = []
    for arquivo in os.listdir(pasta_templates):
        if not arquivo.lower().endswith((".png", ".jpg", ".jpeg")):
            continue
        caminho = os.path.join(pasta_templates, arquivo)
        img = cv2.imread(caminho)
        if img is not None:
            proc = preprocess_image(img, scale)
            templates.append((arquivo, proc, img.shape[:2]))
    return templates


def encontrar_melhor_alvo(frame, templates, scale=1, threshold=0.6, rois=None, estado=None):
    melhor_score = -1
    melhor_pos = None
    melhor_nome = None
    sprite_crop = None
    template_usado = None

    frame_proc = preprocess_image(frame, scale)
    debug_frame = frame.copy()

    for x, y, w, h in rois:
        cv2.rectangle(debug_frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2_debug("Frame Atual", debug_frame, estado)

    for nome, template_proc, (h_t, w_t) in templates:
        for x, y, w, h in rois:
            if w <= w_t or h <= h_t:
                continue  # ROI muito pequeno

            roi = frame_proc[y : y + h, x : x + w]
            if roi.shape[0] < h_t or roi.shape[1] < w_t:
                continue

            result = cv2.matchTemplate(roi, template_proc, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, max_loc = cv2.minMaxLoc(result)

            if max_val > melhor_score and max_val >= threshold:
                top_left = (x + max_loc[0], y + max_loc[1])
                center_x = top_left[0] + w_t // 2
                center_y = top_left[1] + h_t // 2

                melhor_pos = (center_x, center_y)
                melhor_score = max_val
                melhor_nome = nome
                sprite_crop = frame[top_left[1] : top_left[1] + h_t, top_left[0] : top_left[0] + w_t]
                template_usado = template_proc

    # debug visual do alvo detectado
    if melhor_pos and sprite_crop is not None:
        debug_final = frame.copy()
        cv2.rectangle(
            debug_final,
            (melhor_pos[0] - w_t // 2, melhor_pos[1] - h_t // 2),
            (melhor_pos[0] + w_t // 2, melhor_pos[1] + h_t // 2),
            (0, 255, 0),
            2,
        )
        cv2_debug("Alvo Match", debug_final, estado)
        cv2_debug("Template Usado", template_usado, estado)
        cv2_debug("Recorte Match", sprite_crop, estado)

    return melhor_nome, melhor_pos, melhor_score, sprite_crop, template_usado


from ultralytics import YOLO

model = YOLO("best.pt")


def detectar_alvos_yolo(frame):
    results = model.predict(source=frame, conf=0.5, verbose=False)[0]
    detections = []
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cls_id = int(box.cls[0])
        score = float(box.conf[0])
        detections.append({"classe": model.names[cls_id], "bbox": (x1, y1, x2 - x1, y2 - y1), "score": score})
    return detections
