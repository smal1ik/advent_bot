from datetime import datetime

from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
from decouple import config

sub_btn = InlineKeyboardBuilder()
sub_btn.row(
    types.InlineKeyboardButton(
        text="Проверить подписку",
        callback_data="check_sub"
    )
)
sub_btn.row(
    types.InlineKeyboardButton(
        text="Подписаться",
        url=f"https://t.me/{config('CHANNEL_NAME')}"
    )
)
sub_btn = sub_btn.as_markup()


def get_advent_btn(start_day=1,
                   end_day: int = 30,
                   interval_1: int = 4,
                   interval_2: int = 3,
                   check_days: list = []) -> InlineKeyboardMarkup:
    btns = InlineKeyboardBuilder()
    stop = False
    interval = interval_1
    today = datetime.today().day

    while True:
        row = []
        if interval == interval_1:
            interval = interval_2
        else:
            interval = interval_1

        for j in range(interval):
            text = f"{start_day + j}"

            # if start_day + j in check_days:
            #     text += " ✅"
            #     callback_data = f'unlock_advent:{start_day + j}'
            # else:
            #     text += " 🎁"
            #     callback_data = f'new_advent:{start_day + j}'

            if start_day + j in check_days:
                text += " ✅"
                callback_data = f'unlock_advent:{start_day + j}'
            elif start_day + j < today:
                text += " ❌"
                callback_data = "miss_advent"
            elif start_day + j == today:
                text += " 🎁"
                callback_data = f'new_advent:{start_day + j}'
            else:
                text += " 🔒"
                callback_data = "lock_advent"

            row.append(
                types.InlineKeyboardButton(
                    text=text,
                    callback_data=callback_data)
            )
            if start_day + j == end_day:
                stop = True
                break

        start_day += interval
        btns.row(*row)

        if stop:
            break

    return btns.as_markup()


advent_16_btn = InlineKeyboardBuilder()
advent_16_btn.row(
    types.InlineKeyboardButton(
        text="Ссылка на плейлист",
        url="https://music.yandex.ru/users/valerarokidemchenko/playlists/1003?ref_id=778D9512-DD2B-463B-97C3-150B2BD4C95E&utm_medium=copy_link)"
    )
)
advent_16_btn.row(
    types.InlineKeyboardButton(
        text="Вернуться к календарю",
        callback_data="advent"
    )
)
advent_16_btn = advent_16_btn.as_markup()


advent_btn = InlineKeyboardBuilder()
advent_btn.row(
    types.InlineKeyboardButton(
        text="Вернуться к календарю",
        callback_data="advent"
    )
)
advent_btn = advent_btn.as_markup()
