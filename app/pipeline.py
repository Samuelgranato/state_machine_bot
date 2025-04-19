import cv2

from app.window import posicionar_janela
from capture.screen import capturar_tela
from config import DEBUG, DISPLAY_SCALE
from detection.mob_recognition import carregar_templates, verificar_mob
from detection.motion import detectar_movimentos
from utils.log import iniciar_log, logar_match


def preparar_sistema():
    iniciar_log()
    return {
        "frame_anterior": None,
        "templates": carregar_templates(),
        "monitor_index": 0,
        "janela": "Movimentos detectados",
        "frame_atual": None,
        "regioes": [],
        "matches": [],
    }


def capturar_frame():
    return capturar_tela()


def detectar_e_reconhecer(estado):
    frame_anterior = estado["frame_anterior"]
    frame_atual = estado["frame_atual"]
    templates = estado["templates"]

    frame_anterior, regioes = detectar_movimentos(frame_anterior, frame_atual, debug=DEBUG)
    estado["frame_anterior"] = frame_anterior
    estado["regioes"] = regioes

    frame_gray = cv2.cvtColor(frame_atual, cv2.COLOR_BGR2GRAY)
    matches = []

    for x, y, w, h in regioes:
        roi = frame_gray[y : y + h, x : x + w]
        nome_mob, score = verificar_mob(roi, templates)
        if nome_mob:
            logar_match(nome_mob, x, y, w, h, score)
            matches.append((nome_mob, x, y, w, h, score))

    estado["matches"] = matches


def desenhar_resultado(estado):
    frame = estado["frame_atual"]
    for x, y, w, h in estado["regioes"]:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    for nome_mob, x, y, w, h, _ in estado["matches"]:
        cv2.putText(
            frame,
            f"{nome_mob}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.5,
            (0, 255, 255),
            1,
        )
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 255), 2)


def capturar(estado):
    estado["frame_atual"] = capturar_frame()


def processar(estado):
    detectar_e_reconhecer(estado)
    desenhar_resultado(estado)


def exibir(estado):
    frame = estado["frame_atual"]
    largura = int(frame.shape[1] * DISPLAY_SCALE)
    altura = int(frame.shape[0] * DISPLAY_SCALE)
    frame_redimensionado = cv2.resize(frame, (largura, altura))
    cv2.imshow(estado["janela"], frame_redimensionado)


def posicionar_janela_se_necessario(estado):
    if not estado.get("janela_posicionada"):
        posicionar_janela(estado["janela"], estado["monitor_index"])
        estado["janela_posicionada"] = True


def verificar_saida():
    tecla = cv2.waitKey(50) & 0xFF
    if tecla == 27:
        return "sair"
    elif tecla == 13:
        return "confirmar"
    return None


def finalizar():
    cv2.destroyAllWindows()
