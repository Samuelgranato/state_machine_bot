import cv2

from app.pipeline import exibir, posicionar_janela_se_necessario, verificar_saida
from scripts.anotar_assets.pipeline import carregar_lote, mover_lote, preparar_estado
from scripts.anotar_assets.ui import configurar_mouse, construir_grade


def run():
    estado = preparar_estado()
    configurar_mouse(estado)

    while True:
        if not carregar_lote(estado):
            print("Sem mais imagens.")
            break

        while True:
            estado["frame_atual"] = construir_grade(estado)
            exibir(estado)
            posicionar_janela_se_necessario(estado)

            acao = verificar_saida()
            if acao == "confirmar":
                mover_lote(estado)
                break
            elif acao == "sair":
                return

    cv2.destroyAllWindows()


if __name__ == "__main__":
    run()
