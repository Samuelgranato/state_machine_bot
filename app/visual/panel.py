import asyncio

from rich.console import Console
from rich.live import Live

from visual.table import generate_table

console = Console()


async def render_status(state):
    with Live(generate_table(await state.dump()), refresh_per_second=2, console=console) as live:
        while True:
            data = await state.dump()
            live.update(generate_table(data))
            await asyncio.sleep(0.5)
