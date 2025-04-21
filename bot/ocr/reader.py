from bot.ocr.easyocr_engine import EasyOCREngine

ocr_engine = EasyOCREngine()


def read_text_from_region(frame, region):
    x, y, w, h = region
    cropped = frame[y : y + h, x : x + w]
    return ocr_engine.read(cropped)
