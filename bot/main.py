import asyncio

from bot.orchestrator import start_bot
from bot.state import BotState


async def main():
    state = BotState()
    await start_bot(state)


if __name__ == "__main__":
    asyncio.run(main())
