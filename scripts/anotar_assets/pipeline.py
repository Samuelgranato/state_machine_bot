import os
import shutil

from app.pipeline import preparar_sistema
from config import ASSET_ANOTACAO_BATCH, ASSET_MOBS_DIR, ASSET_RAW_DIR

TRASH_DIR = "dataset/trash"


def preparar_estado():
    estado = preparar_sistema()
    estado["classe"] = input("Digite a classe para esse lote: ").strip()
    return estado


def carregar_lote(estado):
    arquivos = sorted([f for f in os.listdir(ASSET_RAW_DIR) if f.lower().endswith((".png", ".jpg", ".jpeg"))])
    estado["arquivos"] = arquivos[:ASSET_ANOTACAO_BATCH]
    estado["selecionados"] = set()
    return bool(estado["arquivos"])


def mover_lote(estado):
    arquivos = estado["arquivos"]
    selecionados = estado["selecionados"]
    classe = estado["classe"]

    destino_ok = os.path.join(ASSET_MOBS_DIR, classe)
    destino_trash = TRASH_DIR
    os.makedirs(destino_ok, exist_ok=True)
    os.makedirs(destino_trash, exist_ok=True)

    for idx, nome in enumerate(arquivos):
        origem = os.path.join(ASSET_RAW_DIR, nome)
        destino = os.path.join(destino_ok if idx in selecionados else destino_trash, nome)
        shutil.move(origem, destino)
        print(f"[✓] Movido: {destino}")
