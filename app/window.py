import cv2
from screeninfo import get_monitors


def posicionar_janela(janela_nome, monitor_index):
    monitores = get_monitors()
    if monitor_index < len(monitores):
        monitor = monitores[monitor_index]
        cv2.moveWindow(janela_nome, monitor.x, monitor.y)
