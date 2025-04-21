import asyncio


async def watch_health(state):
    while True:
        health = await state.get("health")
        new_health = max(health - 3, 0)
        await state.set("health", new_health)
        if new_health < 30:
            await state.set("alert", "heal")
        await asyncio.sleep(0.3)
