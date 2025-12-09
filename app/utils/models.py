from enum import EnumType, Enum
from typing import Optional

from aiogram.types import InlineKeyboardMarkup
from pydantic import BaseModel


class TypeAdventDay(str, Enum):
    LINK = "link"
    LUCKY_CLICK = "lucky_click"
    TEXT = "text"


class AdventDay(BaseModel):
    day: int
    type: TypeAdventDay = None
    link: Optional[str] = None
    text: Optional[str] = None
    buttons: Optional[list[InlineKeyboardMarkup]] = None

    count_wins: Optional[int] = None
    left_wins: Optional[int] = None
    msgs_wins: Optional[list[str]] = None
    msgs_loses: Optional[list[str]] = None

