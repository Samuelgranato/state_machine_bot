import os
import uuid

import cv2
import mss
import numpy as np
from pynput import keyboard

OUTPUT_FOLDER = "captures/screenshots"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


def capturar_tela():
    with mss.mss() as sct:
        monitor = sct.monitors[2]  # Altere se for outro monitor
        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame


def salvar_frame():
    frame = capturar_tela()
    filename = f"{uuid.uuid4().hex}.jpg"
    caminho = os.path.join(OUTPUT_FOLDER, filename)
    cv2.imwrite(caminho, frame)
    print(f"✅ Screenshot salva: {caminho}")


def on_press(key):
    try:
        if key.char == "s":
            salvar_frame()
    except AttributeError:
        if key == keyboard.Key.esc:
            print("Encerrando captura...")
            return False


print("🟢 Pressione 's' para salvar screenshot. Pressione ESC para sair.")

with keyboard.Listener(on_press=on_press) as listener:
    listener.join()
