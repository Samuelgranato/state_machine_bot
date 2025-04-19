import time

from app.actor.triggers import avaliar_triggers
from app.reader.life import update_life
from app.reader.stamina import update_stamina
from automacoes.goblin_farm.job import executar_job
from capture.screen import capturar_tela


def run_bot_loop(estado):
    while True:
        frame = capturar_tela()
        update_life(estado, frame)
        update_stamina(estado, frame)
        avaliar_triggers(estado)
        executar_job(estado)
        time.sleep(1)
