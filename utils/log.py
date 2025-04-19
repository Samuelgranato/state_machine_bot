import csv
import os
from datetime import datetime

LOG_FILE = "mob_matches.csv"


def iniciar_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "mob", "x", "y", "w", "h", "score"])


def logar_match(mob, x, y, w, h, score):
    timestamp = datetime.now().isoformat(timespec="seconds")
    with open(LOG_FILE, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, mob, x, y, w, h, round(score, 4)])
