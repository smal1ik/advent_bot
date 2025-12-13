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

    count_wins_1: Mapped[int] = mapped_column(nullable=True)
    count_wins_2: Mapped[int] = mapped_column(nullable=True)
    count_wins_3: Mapped[int] = mapped_column(nullable=True)
    left_wins_1: Mapped[int] = mapped_column(nullable=True, default=0)
    left_wins_2: Mapped[int] = mapped_column(nullable=True, default=0)
    left_wins_3: Mapped[int] = mapped_column(nullable=True, default=0)
    msgs_wins: Mapped[List[str]] = mapped_column(JSONB, default=[])
    msgs_loses: Mapped[List[str]] = mapped_column(JSONB, default=[])

    count_clicks: Mapped[int] = mapped_column(default=0)


class Winner(Base):
    __tablename__ = 'winners'
    id: Mapped[int] = mapped_column(primary_key=True)
    day: Mapped[int] = mapped_column(nullable=False)
    tg_id: Mapped[int] = mapped_column(nullable=False)
    type_prize: Mapped[int] = mapped_column(nullable=False)
