import asyncio

from config import STAMINA_REGION
from detectors.text.reader import read_text_from_region

# Exemplo de coordenadas — ajustar conforme sua HUD


async def watch_stamina_text(state):
    while True:
        frame = await state.get("__frame")
        if frame is None:
            continue
        stamina_text = read_text_from_region(frame, STAMINA_REGION)
        await state.set("stamina_text", stamina_text)
        await asyncio.sleep(0.5)
