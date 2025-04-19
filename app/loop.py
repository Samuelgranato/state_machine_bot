from app.pipeline import (
    capturar,
    exibir,
    finalizar,
    posicionar_janela_se_necessario,
    preparar_sistema,
    processar,
    verificar_saida,
)


def run():
    estado = preparar_sistema()

    while True:
        capturar(estado)
        processar(estado)
        exibir(estado)
        posicionar_janela_se_necessario(estado)

        acao = verificar_saida()
        if acao == "sair":
            break

    finalizar()
