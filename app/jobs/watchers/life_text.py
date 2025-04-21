import asyncio

from config import VIDA_REGION
from detectors.text.reader import read_text_from_region

# Exemplo de coordenadas — ajustar conforme sua HUD


async def watch_life_text(state):
    while True:
        frame = await state.get("__frame")
        if frame is None:
            continue
        life_text = read_text_from_region(frame, VIDA_REGION)
        await state.set("vida_texto", life_text)
        await asyncio.sleep(0.5)
