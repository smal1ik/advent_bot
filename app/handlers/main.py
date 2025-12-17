from aiogram import types, F, Router, Bot
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from decouple import config as env_config

from app.database.requests import get_user, add_user, update_user_subscription
from app.texts import main as cp
from app.keyboards import main as kb

main_handler = Router()


@main_handler.message(Command('start'))
async def cmd_message(message: types.Message, bot: Bot, command: Command):
    user = await get_user(message.from_user.id)
    secret_key = command.args
    if not user:
        await add_user(message.from_user.id,
                       message.from_user.first_name,
                       message.from_user.username,
                       message.from_user.full_name,
                       secret_key)
        await message.answer(cp.sub_msg, reply_markup=kb.sub_btn)
        return
    member = await bot.get_chat_member(chat_id=env_config('CHANNEL_ID'), user_id=message.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        await message.answer(cp.start_msg,
                            reply_markup=kb.get_advent_btn(check_days=user.check_days,
                                                           start_day=17,
                                                           end_day=31))
    else:
        await message.answer(cp.sub_msg, reply_markup=kb.sub_btn)


@main_handler.callback_query(F.data == 'check_sub')
async def check_sub(callback: types.CallbackQuery, state: FSMContext, bot: Bot):
    member = await bot.get_chat_member(chat_id=env_config('CHANNEL_ID'), user_id=callback.from_user.id)
    if member.status in ("member", "administrator", "creator"):
        user = await get_user(callback.from_user.id)
        await update_user_subscription(callback.from_user.id)
        await callback.message.answer(cp.start_msg,
                                      reply_markup=kb.get_advent_btn(check_days=user.check_days,
                                                                     start_day=17,
                                                                     end_day=31))
    else:
        await callback.message.answer(cp.unsub_msg, reply_markup=kb.sub_btn)


@main_handler.callback_query(F.data == 'advent')
async def advent(callback: types.CallbackQuery, state: FSMContext):
    user = await get_user(callback.from_user.id)
    await callback.message.answer(cp.start_msg,
                                  reply_markup=kb.get_advent_btn(check_days=user.check_days,
                                                                 start_day=17,
                                                                 end_day=31))
