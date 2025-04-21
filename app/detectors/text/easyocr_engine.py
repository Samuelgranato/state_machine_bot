import re

import cv2
import easyocr
import numpy as np

from detectors.text.base import BaseOCREngine


def clean_digits(text):
    return re.sub(r"[^\d]", "", text)


class EasyOCREngine(BaseOCREngine):
    def __init__(self, languages=["en"]):
        self.reader = easyocr.Reader(languages, gpu=False)

    def read(self, image, digits=True) -> str:
        processed = self.preprocess(image)
        result = self.reader.readtext(processed, detail=1)
        if result:
            raw_text = result[0][1]
            return clean_digits(raw_text) if digits else raw_text
        return

    def preprocess(self, roi):
        roi_gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
        _, roi_thresh = cv2.threshold(roi_gray, 140, 255, cv2.THRESH_BINARY)
        roi_resized = cv2.resize(roi_thresh, None, fx=4, fy=4, interpolation=cv2.INTER_CUBIC)
        kernel = np.ones((2, 2), np.uint8)
        processed = cv2.dilate(roi_resized, kernel, iterations=1)
        return processed
