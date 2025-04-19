from config import STAMINA_REGION
from detection.text_recognition import get_text


def update_stamina(estado, frame):
    x, y, w, h = STAMINA_REGION
    roi = frame[y : y + h, x : x + w]

    digits = get_text(roi)

    try:
        value = int(digits)
        value = min(value, 100)
        estado["stamina"] = value
    except ValueError:
        pass

    print(f"[watcher][easyOCR] stamina: {estado.get('stamina', '?')}%")
