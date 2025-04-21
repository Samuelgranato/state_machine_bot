from asyncio import Lock


class BotState:
    def __init__(self):
        self._data = {
            "health": 100,
            "inventory": ["potion", "sword"],
            "alert": None,
            "mode": "farm_goblin",
            "substate": "searching",
            "detections": {},  # key: type (e.g., "enemy", "resource"), value: list of dicts
            "_frame": None,  # Placeholder for the current frame
        }
        self._lock = Lock()

    async def get(self, key):
        async with self._lock:
            return self._data.get(key)

    async def set(self, key, value):
        async with self._lock:
            self._data[key] = value

    async def update(self, updates: dict):
        async with self._lock:
            self._data.update(updates)

    async def dump(self):
        async with self._lock:
            return self._data.copy()
