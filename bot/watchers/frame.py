import asyncio

from capture.screen import capturar_tela


async def watch_frame(state):
    while True:
        frame = capturar_tela()
        await state.set("__frame", frame)
        await asyncio.sleep(0.05)  # pode ajustar a frequência ideal
