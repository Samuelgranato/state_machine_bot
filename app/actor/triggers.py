def avaliar_triggers(estado):
    if estado.get("vida", 100) < 20:
        print("⚠️ Vida baixa! (trigger)")
