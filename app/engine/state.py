def criar_estado():
    return {
        "vida": 100,
        "stamina": 100,
        "player_status": "idle",
        "inventory_full": False,
        "localizacao": (0, 0),
        "target_area": "zona_goblin",
        "current_job": "goblin_farm",
    }
