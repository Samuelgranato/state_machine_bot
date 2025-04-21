import time
import tkinter as tk

from screeninfo import get_monitors


def abrir_janelas_em_cada_monitor():
    monitores = get_monitors()
    print("Monitores detectados:")
    for i, monitor in enumerate(monitores):
        print(f"[{i}] x={monitor.x}, y={monitor.y}, w={monitor.width}, h={monitor.height}")
        root = tk.Tk()
        root.title(f"Monitor {i}")
        root.geometry("300x100+{}+{}".format(monitor.x + 100, monitor.y + 100))
        label = tk.Label(root, text=f"Janela no monitor {i}", font=("Arial", 14))
        label.pack(pady=30)
        root.update()  # atualiza a janela antes de seguir
        root.after(1000, root.destroy)  # fecha após 1 segundo
        root.mainloop()


if __name__ == "__main__":
    abrir_janelas_em_cada_monitor()
