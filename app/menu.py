import os
import subprocess
import sys

SCRIPTS_DIR = "scripts"
AUTOMACOES_DIR = "automacoes"

PYTHON_EXEC = os.path.join(os.getcwd(), ".venv", "Scripts", "python.exe")
if not os.path.exists(PYTHON_EXEC):
    PYTHON_EXEC = sys.executable  # fallback


def listar_scripts():
    scripts = []
    for nome in os.listdir(SCRIPTS_DIR):
        caminho = os.path.join(SCRIPTS_DIR, nome, "loop.py")
        if os.path.isfile(caminho):
            scripts.append((nome, f"{SCRIPTS_DIR}.{nome}.loop"))
    return scripts


def listar_automacoes():
    automacoes = []
    if not os.path.exists(AUTOMACOES_DIR):
        return automacoes
    for nome in os.listdir(AUTOMACOES_DIR):
        caminho = os.path.join(AUTOMACOES_DIR, nome, "loop.py")
        if os.path.isfile(caminho):
            automacoes.append((nome, f"{AUTOMACOES_DIR}.{nome}.loop"))
    return automacoes


def menu():
    print("\n====== MENU DO BOT ======")
    print("[0] Executar com estado reativo (orchestrator)")
    print("-- Scripts auxiliares --")
    scripts = listar_scripts()
    for i, (nome, _) in enumerate(scripts, start=1):
        print(f"[{i}] Rodar script: {nome}")
    offset = len(scripts) + 1

    print("-- Automações com máquina de estados --")
    automacoes = listar_automacoes()
    for i, (nome, _) in enumerate(automacoes, start=offset):
        print(f"[{i}] Executar automação: {nome}")

    print("\n[q] Sair")
    return scripts + automacoes


def executar_menu():
    opcoes = menu()
    escolha = input("\nEscolha uma opção: ").strip()

    if escolha == "0":
        subprocess.call([PYTHON_EXEC, "-m", "app.engine.orchestrator"])
    elif escolha.lower() == "q":
        return
    elif escolha.isdigit():
        idx = int(escolha)
        if 1 <= idx <= len(opcoes):
            _, modulo = opcoes[idx - 1]
            subprocess.call([PYTHON_EXEC, "-m", modulo])
        else:
            print("Opção inválida.")
    else:
        print("Entrada inválida.")

    input("\nPressione Enter para voltar ao menu...")
    executar_menu()


if __name__ == "__main__":
    executar_menu()
