import re

import cv2
import easyocr
import numpy as np

# Inicializa EasyOCR
easy_reader = easyocr.Reader(["en"], gpu=False)


def clean_digits(text):
    return re.sub(r"[^\d]", "", text)


def get_text(roi):

    # Pré-processamento
    roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    _, roi_thresh = cv2.threshold(roi_gray, 140, 255, cv2.THRESH_BINARY)
    roi_resized = cv2.resize(roi_thresh, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)

    kernel = np.ones((2, 2), np.uint8)
    processed = cv2.dilate(roi_resized, kernel, iterations=1)

    # EasyOCR
    easy_result = easy_reader.readtext(processed)
    if easy_result:
        raw_text = easy_result[0][1]
        clean_text = clean_digits(raw_text)
        return clean_text
    else:
        print("[EasyOCR] nada detectado")
