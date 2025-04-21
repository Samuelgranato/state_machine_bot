import asyncio

import cv2
import mss
import numpy as np
from config import DEBUG_MONITOR_INDEX


def capturar_tela():
    with mss.mss() as sct:
        monitores = sct.monitors
        monitor = monitores[DEBUG_MONITOR_INDEX]

        screenshot = sct.grab(monitor)
        frame = np.array(screenshot)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGRA2BGR)
        return frame


async def watch_frame(state):
    while True:
        frame = capturar_tela()
        await state.set("__frame", frame)
        await asyncio.sleep(0.05)  # pode ajustar a frequência ideal
