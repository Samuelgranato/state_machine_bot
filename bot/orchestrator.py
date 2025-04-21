import asyncio

from bot.actors.heal import use_healing_potion
from bot.jobs.farm_goblin import run_farm_goblin
from bot.visual.panel import render_status
from bot.watchers.frame import watch_frame
from bot.watchers.health import watch_health
from bot.watchers.life_text import watch_life_text
from bot.watchers.stamina_text import watch_stamina_text
from bot.watchers.vision import watch_assets


async def main_loop(state):
    while True:
        alert = await state.get("alert")
        mode = await state.get("mode")

        if alert == "heal":
            await use_healing_potion()
            await state.set("alert", None)
        elif mode == "farm_goblin":
            await run_farm_goblin(state)

        await asyncio.sleep(0.05)


async def start_bot(state):
    await asyncio.gather(
        watch_frame(state),
        watch_health(state),
        watch_assets(state),
        watch_life_text(state),
        watch_stamina_text(state),
        main_loop(state),
        render_status(state),  # new generic vision watcher
    )
