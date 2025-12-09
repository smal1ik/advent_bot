import enum
from datetime import timedelta

from aiogram.types import InlineKeyboardMarkup
from sqlalchemy import Enum, UniqueConstraint
from typing import List, Any, Optional, Set

from pydantic import BaseModel
from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Interval
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from decouple import config

from app.utils.models import TypeAdventDay

engine = create_async_engine(config('POSTGRESQL'), echo=False)
async_session = async_sessionmaker(engine)


class Base(AsyncAttrs, DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)
    first_name: Mapped[str] = mapped_column(nullable=True)
    full_name: Mapped[str] = mapped_column(nullable=True)
    username: Mapped[str] = mapped_column(nullable=True)
    mark: Mapped[str] = mapped_column(nullable=True, default='')
    check_days: Mapped[List[int]] = mapped_column(JSONB, default=[])
    new_subscriber: Mapped[bool] = mapped_column(default=False)


class AdventDay(Base):
    __tablename__ = 'advent_days'
    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[int] = mapped_column(nullable=False)
    type: Mapped[enum.Enum] = mapped_column(Enum(TypeAdventDay), nullable=False)

    link: Mapped[str] = mapped_column(nullable=True)

    text: Mapped[str] = mapped_column(nullable=True)
    buttons: Mapped[List[InlineKeyboardMarkup]] = mapped_column(JSONB, nullable=True)

    count_wins: Mapped[int] = mapped_column(nullable=True)
    left_wins: Mapped[int] = mapped_column(nullable=True)
    msgs_wins: Mapped[List[str]] = mapped_column(JSONB, default=[])
    msgs_loses: Mapped[List[str]] = mapped_column(JSONB, default=[])

    count_clicks: Mapped[int] = mapped_column(default=0)
    winners: Mapped[List[BigInteger]] = mapped_column(JSONB, default=[])
