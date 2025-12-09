import datetime

from aiogram import types, F, Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from decouple import config as env_config

from app.database.requests import get_user, add_user, update_user_check_days
from app.texts import main as cp
from app.keyboards import main as kb
from app.utils.cache import CacheUser, CacheAdvent

advent_handler = Router()


@advent_handler.callback_query(F.data == "miss_advent")
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer(text=cp.miss_advent, show_alert=True)


@advent_handler.callback_query(F.data == "lock_advent")
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.answer(text=cp.lock_advent, show_alert=True)


@advent_handler.callback_query(F.data.contains("unlock_advent:"))
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot, cache_user: CacheUser, cache_advent: CacheAdvent):
    day = int(callback.data.split(":")[1])
    user = await cache_user.add(callback.from_user.id)

    if day not in user.check_days:
        return

    advent_day = await cache_advent.add(day)

#   Логика для отправки сообщения


@advent_handler.callback_query(F.data.contains("new_advent:"))
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot, cache_user: CacheUser, cache_advent: CacheAdvent):
    day = int(callback.data.split(":")[1])
    today = datetime.datetime.now().day
    if day != today:
        return

    user = await cache_user.add(callback.from_user.id)

    if day not in user.check_days:
        user.check_days.append(day)
        await update_user_check_days(callback.from_user.id, user.check_days)

    advent_day = await cache_advent.add(day)

#   Логика для отправки сообщения



