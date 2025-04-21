import asyncio

from orchestrator import start_bot
from state import BotState


async def main():
    state = BotState()
    await start_bot(state)


if __name__ == "__main__":
    asyncio.run(main())
