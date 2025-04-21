import cv2
from screeninfo import get_monitors

from config import DEBUG_MONITOR_INDEX


def posicionar_janela(janela_nome, monitor_index):
    monitores = get_monitors()
    if monitor_index < len(monitores):
        monitor = monitores[monitor_index]
        cv2.moveWindow(janela_nome, monitor.x, monitor.y)


def cv2_debug(janela_nome, frame, estado):
    frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
    cv2.imshow(janela_nome, frame)
    if estado.get(f"janela_posicionada_{janela_nome}") is None:
        posicionar_janela(janela_nome, DEBUG_MONITOR_INDEX - 2)
        estado[f"janela_posicionada_{janela_nome}"] = True
    cv2.waitKey(1)
