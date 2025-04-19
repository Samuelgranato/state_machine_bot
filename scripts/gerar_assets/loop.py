import os

import cv2

from app.pipeline import (
    capturar,
    exibir,
    posicionar_janela_se_necessario,
    preparar_sistema,
    verificar_saida,
)
from scripts.gerar_assets.pipeline import coletar_e_salvar_rois

SAVE_DIR = "dataset/raw"


def run():
    os.makedirs(SAVE_DIR, exist_ok=True)
    estado = preparar_sistema()
    estado["ultimo_salvamento"] = 0
    estado["janela"] = "Modo coleta de assets"
    estado["janela_posicionada"] = False

    while True:
        capturar(estado)
        coletar_e_salvar_rois(estado)
        exibir(estado)
        posicionar_janela_se_necessario(estado)

        acao = verificar_saida()
        if acao == "sair":
            break

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
