import threading
import tkinter as tk
from tkinter import ttk

import cv2
from PIL import Image, ImageTk
from screeninfo import get_monitors

from app.engine.orchestrator import run_bot_loop
from app.engine.state import criar_estado
from capture.screen import capturar_tela
from config import DEBUG_MONITOR_INDEX, GAME_MONITOR_INDEX


def posicionar_janela_tkinter(root):
    monitores = get_monitors()
    if 0 <= DEBUG_MONITOR_INDEX < len(monitores):
        m = monitores[DEBUG_MONITOR_INDEX]
        root.geometry(f"+{m.x+100}+{m.y+100}")


def recortar_monitor(frame):
    monitores = get_monitors()
    if 0 <= GAME_MONITOR_INDEX < len(monitores):
        m = monitores[GAME_MONITOR_INDEX]
        return frame[m.y : m.y + m.height, m.x : m.x + m.width]
    return frame


class BotDashboard:
    def __init__(self, estado):
        self.estado = estado
        self.root = tk.Tk()
        self.root.title("Bot Dashboard")
        self.root.geometry("1100x700")
        self.root.resizable(False, False)

        posicionar_janela_tkinter(self.root)

        self.labels = {}
        self.video_label = None
        self.image_tk = None

        self._build_ui()
        self._start_bot_thread()
        self._refresh_ui()
        self._start_video_loop()
        self.root.mainloop()

    def _build_ui(self):
        # Info
        info_frame = tk.Frame(self.root)
        info_frame.pack(side="left", fill="y", padx=10, pady=10)

        for key in self.estado:
            frame = ttk.Frame(info_frame)
            frame.pack(fill="x", pady=2)
            label = ttk.Label(frame, text=f"{key}:", width=14, anchor="w")
            label.pack(side="left")
            value = ttk.Label(frame, text="", anchor="w")
            value.pack(side="left", fill="x", expand=True)
            self.labels[key] = value

        # Preview da tela
        preview_frame = tk.Frame(self.root)
        preview_frame.pack(side="right", padx=10, pady=10)
        self.video_label = tk.Label(preview_frame)
        self.video_label.pack()

    def _refresh_ui(self):
        for key, value in self.estado.items():
            self.labels.get(key, ttk.Label()).config(text=str(value))
        self.root.after(200, self._refresh_ui)

    def _start_bot_thread(self):
        def bot_loop():
            run_bot_loop(self.estado)

        threading.Thread(target=bot_loop, daemon=True).start()

    def _start_video_loop(self):
        def atualizar_video():
            frame = capturar_tela()
            frame = recortar_monitor(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            imagem = Image.fromarray(frame)

            if (
                self.image_tk is None
                or self.image_tk.width() != imagem.width
                or self.image_tk.height() != imagem.height
            ):
                self.image_tk = ImageTk.PhotoImage(imagem)
            else:
                self.image_tk.paste(imagem)

            self.video_label.configure(image=self.image_tk)
            self.video_label.image = self.image_tk
            self.root.after(60, atualizar_video)  # reduzido para 16 FPS aprox.

        atualizar_video()


def start_dashboard():
    estado = criar_estado()
    BotDashboard(estado)
