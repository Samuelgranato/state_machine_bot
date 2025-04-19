import tkinter as tk

import cv2
from PIL import Image, ImageTk

from capture.screen import capturar_tela
from config import VIDA_REGION


def cv2_to_tk(img):
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)
    return ImageTk.PhotoImage(img_pil)


def debug_life_region():
    x, y, w, h = VIDA_REGION
    frame = capturar_tela()
    roi = frame[y : y + h, x : x + w]

    root = tk.Tk()
    root.title("Life Region Debug")

    # Layout com duas imagens lado a lado
    # frame_img = cv2_to_tk(frame)
    roi_img = cv2_to_tk(roi)

    # label1 = tk.Label(root, image=frame_img)
    # label1.pack(side="left", padx=10, pady=10)

    label2 = tk.Label(root, image=roi_img)
    label2.pack(side="right", padx=10, pady=10)

    root.mainloop()


if __name__ == "__main__":
    debug_life_region()
