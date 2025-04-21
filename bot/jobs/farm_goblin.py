import asyncio

from bot.actors.attack import attack_goblin


async def run_farm_goblin(state):
    substate = await state.get("substate")
    detections = await state.get("detections")
    enemies = detections.get("enemy", [])

    if substate == "searching":
        if enemies:
            print(">> Enemy detected, preparing to attack...")
            await state.set("substate", "attacking")

    elif substate == "attacking":
        await attack_goblin()
        await state.set("substate", "waiting_for_death")

    elif substate == "waiting_for_death":
        print(">> Waiting for mob to die...")
        await asyncio.sleep(1)
        await state.set("substate", "searching")

    await asyncio.sleep(0.2)
