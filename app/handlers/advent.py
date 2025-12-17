import datetime
import random

from aiogram import types, F, Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from decouple import config as env_config

from app.database.requests import get_user, add_user, update_user_check_days, get_winner, add_winner
from app.texts import main as cp
from app.keyboards import main as kb
from app.utils.cache import CacheAdvent
from app.utils.functions import check_winner

advent_handler = Router()


@advent_handler.callback_query(F.data == "miss_advent")
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(text=cp.miss_advent, reply_markup=kb.advent_btn)


@advent_handler.callback_query(F.data == "lock_advent")
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    await callback.message.answer(text=cp.lock_advent, reply_markup=kb.advent_btn)


@advent_handler.callback_query(F.data.contains("unlock_advent:"))
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot, cache_advent: CacheAdvent):
    day = int(callback.data.split(":")[1])
    user = await get_user(callback.from_user.id)

    if day not in user.check_days:
        return

    advent_day = await cache_advent.add(day)
    already_winner = await get_winner(callback.from_user.id)
    if already_winner and already_winner.day == day:
        type_prize = already_winner.type_prize - 1
        await callback.message.answer_photo(caption=advent_day.msgs_wins[type_prize], photo=FSInputFile(f"app/static/win_{type_prize + 1}.png"), reply_markup=kb.advent_btn, parse_mode="HTML")
    else:
        await callback.message.answer_photo(caption=cp.creative_already, photo=FSInputFile(f"app/static/creative_already.png"), reply_markup=kb.advent_btn, parse_mode="HTML")


@advent_handler.callback_query(F.data.contains("new_advent:"))
async def answer_message(callback: types.CallbackQuery, state: FSMContext, bot: Bot, cache_advent: CacheAdvent):
    day = int(callback.data.split(":")[1])
    today = datetime.datetime.now().day
    if day != today:
        return

    user = await get_user(callback.from_user.id)
    if day in user.check_days:
        return

    if day not in user.check_days:
        user.check_days.append(day)
        await update_user_check_days(callback.from_user.id, user.check_days)

    advent_day = await cache_advent.add(day)
    advent_day.count_clicks += 1
    total_prizes = advent_day.count_wins_1 + advent_day.count_wins_2 + advent_day.count_wins_3
    prizes_given = total_prizes - advent_day.left_wins_1 + advent_day.left_wins_2 + advent_day.left_wins_3
    check_win = check_winner(total_prizes, prizes_given)

    if check_win:
        already_winner = await get_winner(callback.from_user.id)
        if already_winner:
            check_win = False

    if check_win and (advent_day.left_wins_1 >= 1 or advent_day.left_wins_2 >= 1 or advent_day.left_wins_3 >= 1):
        if not callback.from_user.username:
            text = f"Пользователь [{callback.from_user.full_name}](tg://user?id={callback.from_user.id})\nВыйграл"
        else:
            text = f"Пользователь @{callback.from_user.username}\nВыйграл"

        if advent_day.left_wins_1 >= 1:
            text += f" {cp.prizes[0]}\nВремя: {datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')}"
            advent_day.left_wins_1 -= 1
            await callback.message.answer_photo(caption=advent_day.msgs_wins[0],
                                                photo=FSInputFile("app/static/win_1.png"),
                                                reply_markup=kb.advent_btn, parse_mode="HTML")
            await add_winner(callback.from_user.id, advent_day.day, 1)

        elif advent_day.left_wins_2 >= 1:
            text += f" {cp.prizes[1]}\nВремя: {datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')}"
            advent_day.left_wins_2 -= 1
            await callback.message.answer_photo(caption=advent_day.msgs_wins[1],
                                                photo=FSInputFile("app/static/win_2.png"),
                                                reply_markup=kb.advent_btn, parse_mode="HTML")
            await add_winner(callback.from_user.id, advent_day.day, 2)

        elif advent_day.left_wins_3 >= 1:
            text += f" {cp.prizes[2]}\nВремя: {datetime.datetime.now().strftime('%d.%m.%y %H:%M:%S')}"
            advent_day.left_wins_3 -= 1
            await callback.message.answer_photo(caption=advent_day.msgs_wins[3],
                                                photo=FSInputFile("app/static/win_3.png"),
                                                reply_markup=kb.advent_btn)
            await add_winner(callback.from_user.id, advent_day.day, 3)

        else:
            await callback.message.answer_photo(caption=random.choice(advent_day.msgs_loses),
                                                photo=FSInputFile(f"app/static/creative_{advent_day.day}.png"),
                                                reply_markup=kb.advent_btn, parse_mode="HTML")
            return
        await bot.send_message(text=text.replace('.', '\.'), chat_id=env_config("CHAT_ID"), parse_mode="MarkdownV2")

    else:
        if advent_day.day == 30:
            await callback.message.answer_photo(caption=random.choice(advent_day.msgs_loses),
                                                photo=FSInputFile(f"app/static/creative_{advent_day.day}.png"),
                                                reply_markup=kb.advent_30_btn, parse_mode="HTML")
            return
        await callback.message.answer_photo(caption=random.choice(advent_day.msgs_loses),
                                            photo=FSInputFile(f"app/static/creative_{advent_day.day}.png"),
                                            reply_markup=kb.advent_btn, parse_mode="HTML")



