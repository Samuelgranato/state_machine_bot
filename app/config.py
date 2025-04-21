# Configurações do projeto
# Configurações globais do projeto

DEBUG = True
DEBUG_MONITOR_INDEX = 2  # 1 é o principal, 2 é o secundário etc.
GAME_MONITOR_INDEX = 1  # 1 é o principal, 2 é o secundário etc.
MOTION_MIN_AREA = 300
MOTION_MAX_AREA = 10000
ROI_LIMIT = 100

# Escala da janela exibida no monitor (1.0 = tamanho original)
DISPLAY_SCALE = 0.6

# Tamanho mínimo e máximo do ROI para salvar em gerar_assets
ASSET_MIN_SIZE = 20  # pixels (largura ou altura mínima)
ASSET_MAX_SIZE = 10000  # pixels (largura ou altura máxima)

ASSET_SALVAR_INTERVALO = 1.5  # segundos entre salvamentos consecutivos

ASSET_ANOTACAO_BATCH = 30
ASSET_RAW_DIR = "dataset/raw"
ASSET_MOBS_DIR = "assets/mobs"


VIDA_REGION = (1680, 75, 30, 25)  # x, y, w, h — região da vida na tela
STAMINA_REGION = (1690, 150, 30, 22)  # x, y, w, h — região da vida na tela

OCR_CONFIG = "--psm 7 --oem 3 -c tessedit_char_whitelist=0123456789"
