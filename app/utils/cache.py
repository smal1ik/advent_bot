import asyncio
from aiogram import Bot
from aiocache import Cache
from decouple import config

from app.database.models import User, AdventDay
from app.database.requests import sync_history_lucky_post, get_user, get_advent_day, update_advent_day, \
    update_stats_advent_day


class CacheAdvent:
    def __init__(self, reset_interval=60):
        self.cache_advent_day = Cache(Cache.MEMORY)
        self.reset_interval = reset_interval

        self._flush_lock = asyncio.Lock()
        self._key_locks: dict[str, asyncio.Lock] = {}
        asyncio.create_task(self._periodic_flush())


    def _get_lock(self, key: str) -> asyncio.Lock:
        if key not in self._key_locks:
            self._key_locks[key] = asyncio.Lock()
        return self._key_locks[key]


    async def add(self, day: int) -> AdventDay:
        key = f"day:{day}"

        async with self._get_lock(key):
            advent_day = await self.cache_advent_day.get(key)
            if not advent_day:
                advent_day = await get_advent_day(day)
                await self.cache_advent_day.set(key, advent_day)

            return advent_day


    async def flush(self):
        async with self._flush_lock:
            items = list(self.cache_advent_day._cache.items())

            if not items:
                return

            for key, value in items:
                await update_stats_advent_day(value)
                await self.cache_advent_day.delete(key)


    async def _periodic_flush(self):
        while True:
            await asyncio.sleep(self.reset_interval)
            await self.flush()
