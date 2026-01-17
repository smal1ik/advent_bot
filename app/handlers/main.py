from datetime import datetime

from aiogram import types, F, Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from decouple import config as env_config

from app.database.requests import get_user, add_user, update_user_subscription, get_analytics, active_user
from app.texts import main as cp
from app.keyboards import main as kb

main_handler = Router()


@main_handler.message(Command('analytics'))
async def cmd_message(message: types.Message, bot: Bot):
    analytics = await get_analytics()
    msg = f"""Всего пользователей: {analytics[0]}
Всего участников: {analytics[1]}
Новых подписчиков: {analytics[2]}
Общее число кликов: {analytics[3]}
"""
    for name_mark, count in analytics[4]:
        msg += f"{name_mark} | {count}\n"
    for day in analytics[5]:
        msg += f"\n{day.day} день | число кликов: {day.count_clicks}"
    await message.answer(msg)


@main_handler.message(Command('start'))
async def cmd_message(message: types.Message, bot: Bot, command: Command):
    user = await get_user(message.from_user.id)
    if user:
        await message.answer("""Начните год с подарков! Для этого вам нужно:
1. Подписаться на канал MAAG
2. Нажать на кнопку «Принять участие»
3. Дождаться результатов уже в это воскресенье в 18:00

Ваша удача ждёт своего часа!""", reply_markup=kb.active_btn)


@main_handler.callback_query(F.data == 'check_sub')
async def check_sub(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    member = await bot.get_chat_member(chat_id=env_config('CHANNEL_ID'), user_id=callback.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        user = await get_user(callback.from_user.id)
        await update_user_subscription(callback.from_user.id)
        now = datetime.now()
        day = now.day
        await callback.message.answer_photo(photo=FSInputFile(f"app/static/advent_{day}.png"),
                                            caption=cp.start_msg,
                                            reply_markup=kb.get_advent_btn(check_days=user.check_days,
                                                                           start_day=17,
                                                                           end_day=31))
    else:
        await callback.message.answer(cp.unsub_msg, reply_markup=kb.sub_btn)


@main_handler.callback_query(F.data == 'advent')
async def advent(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    member = await bot.get_chat_member(chat_id=env_config('CHANNEL_ID'), user_id=callback.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        user = await get_user(callback.from_user.id)
        now = datetime.now()
        day = now.day
        await callback.message.answer_photo(photo=FSInputFile(f"app/static/advent_{day}.png"),
                                            caption=cp.start_msg,
                                            reply_markup=kb.get_advent_btn(check_days=user.check_days,
                                                                           start_day=17,
                                                                           end_day=31))
    else:
        await callback.message.answer(cp.sub_msg, reply_markup=kb.sub_btn)


@main_handler.callback_query(F.data == 'active')
async def advent(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    user = await get_user(callback.from_user.id)
    if user:
        await active_user(callback.from_user.id)
        await callback.message.answer("Теперь вы участвуете, результаты 18го Января в 18:00!")

