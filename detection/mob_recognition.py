# reconhecimento de mobs
import os

import cv2

MOB_TEMPLATES_PATH = "assets/mobs"
MATCH_THRESHOLD = 0.6  # Pode ajustar depois


def carregar_templates():
    templates = []
    for nome_arquivo in os.listdir(MOB_TEMPLATES_PATH):
        caminho = os.path.join(MOB_TEMPLATES_PATH, nome_arquivo)
        imagem = cv2.imread(caminho, cv2.IMREAD_GRAYSCALE)
        if imagem is not None:
            templates.append((nome_arquivo, imagem))
    return templates


def verificar_mob(cropped_gray, templates):
    for nome, template in templates:
        if cropped_gray.shape[0] < template.shape[0] or cropped_gray.shape[1] < template.shape[1]:
            continue  # Pula se a área for menor que o template
        resultado = cv2.matchTemplate(cropped_gray, template, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(resultado)
        if max_val >= MATCH_THRESHOLD:
            return nome, max_val
    return None, None
