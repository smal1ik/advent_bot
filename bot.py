import asyncio
import logging
import sys

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties

from decouple import config

from app.handlers.main import main_handler
from app.utils.advent_calendar import migration_advent_calendar
from app.utils.cache import CacheUser, CacheAdvent


async def main():
    bot = Bot(token=config('BOT_TOKEN'),
              default=DefaultBotProperties(
              parse_mode="HTML"))

    await bot.delete_webhook()
    dp = Dispatcher()

    dp.include_router(main_handler)

    await migration_advent_calendar()
    cache_user = CacheUser(ttl=60*5, reset_interval=60*5, max_size_cache=5000)
    cache_advent = CacheAdvent(reset_interval=60*5)

    try:
        await dp.start_polling(bot,
                               polling_timeout=100,
                               cache_user=cache_user,
                               cache_advent=cache_advent)
    finally:
        print("close cache")
        await cache_user.flush()
        await cache_advent.flush()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
        print("Bot start")
    except KeyboardInterrupt:
        print('Bot stop')
    except Exception as e:
        print(e)
