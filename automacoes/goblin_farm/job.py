def executar_job(estado):
    if estado["player_status"] == "idle":
        print("[goblin_farm] Jogador está parado. Procurando goblins...")
    # Você pode usar estado["vida"], estado["localizacao"], etc.
