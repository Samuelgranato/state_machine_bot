from config import VIDA_REGION
from detection.text_recognition import get_text


def update_life(estado, frame):
    x, y, w, h = VIDA_REGION
    roi = frame[y : y + h, x : x + w]
    if roi is None or roi.size == 0:
        return

    digits = get_text(roi)

    if not digits:
        return

    try:
        value = int(digits)
        value = min(value, 100)
        estado["vida"] = value
    except ValueError:
        pass

    print(f"[watcher][easyOCR] vida: {estado.get('vida', '?')}%")
