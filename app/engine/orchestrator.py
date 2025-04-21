import time
from threading import Thread

import cv2

from app.actor.mouse import clicar, mover_mouse_humanizado
from app.actor.triggers import avaliar_triggers
from app.engine.state import criar_estado
from app.reader.life import update_life
from app.reader.stamina import update_stamina
from app.reader.target_finder import carregar_templates, encontrar_melhor_alvo
from app.window import cv2_debug
from automacoes.goblin_farm.job import executar_job
from capture.screen import capturar_tela
from detection.motion import detectar_movimentos

from .overlay import start_overlay

TEMPLATES_PATH = "assets/mobs/goblin"
templates = carregar_templates(TEMPLATES_PATH)

frame_anterior = None
estado = criar_estado()

rois_compartilhadas = []


def get_rois():
    return rois_compartilhadas


# iniciar overlay em background
# Thread(target=start_overlay, args=(get_rois,), daemon=True).start()


def run_bot_loop():
    global frame_anterior
    while True:
        frame = capturar_tela()
        if frame is None or frame.size == 0:
            time.sleep(0.5)
            continue

        estado["__frame"] = frame

        update_life(estado, frame)
        update_stamina(estado, frame)
        avaliar_triggers(estado)
        executar_job(estado)

        frame_gray, rois = detectar_movimentos(frame_anterior, frame, estado, debug=False)
        frame_anterior = frame_gray

        rois_compartilhadas.clear()
        rois_compartilhadas.extend(rois)

        nome, pos, score, sprite_crop, template_proc = encontrar_melhor_alvo(frame, templates, rois=rois, estado=estado)
        if pos:
            print(f"[MATCH] {nome} | Score: {score:.2f}")
            if sprite_crop is not None:
                cv2_debug("Sprite encontrado", sprite_crop, estado)
            mover_mouse_humanizado(*pos)
            # clicar()

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.03)


if __name__ == "__main__":
    run_bot_loop()
