from typing import List

from app.database.models import User, async_session, AdventDay, Winner
from sqlalchemy import select, BigInteger, update, delete, func, case, insert, or_


async def add_user(tg_id: BigInteger, first_name: str, username: str, full_name: str, mark: str = "", member_status: str = ""):
    """
    Функция добавляет пользователя в БД
    """
    async with async_session() as session:
        session.add(User(
            tg_id=tg_id,
            first_name=first_name,
            username=username,
            full_name=full_name,
            mark=mark,
            member_status=member_status))
        await session.commit()


async def update_user_subscription(tg_id: BigInteger, subscription: bool = True):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(new_subscriber=subscription))
        await session.commit()


async def update_user_check_days(tg_id: BigInteger, check_days: list[int]):
    async with async_session() as session:
        await session.execute(update(User).where(User.tg_id == tg_id).values(check_days=check_days))
        await session.commit()


async def get_user(tg_id: BigInteger) -> User:
    """
    Получаем пользователя по tg_id
    """
    async with async_session() as session:
        result = await session.scalar(select(User).where(User.tg_id == tg_id))
        return result


async def get_advent_day(day: int) -> AdventDay:
    async with async_session() as session:
        result = await session.scalar(select(AdventDay).where(AdventDay.day == day))
        return result


async def add_advent_day(advent_day: AdventDay):
    async with async_session() as session:
        if advent_day.left_wins_1 is None:
            advent_day.left_wins_1 = advent_day.count_wins_1
        if advent_day.left_wins_2 is None:
            advent_day.left_wins_2 = advent_day.count_wins_2
        if advent_day.left_wins_3 is None:
            advent_day.left_wins_3 = advent_day.count_wins_3
        session.add(advent_day)
        await session.commit()


async def update_stats_advent_day(advent_day: AdventDay):
    async with async_session() as session:
        await session.execute(update(AdventDay).where(AdventDay.day == advent_day.day).
                              values(
            left_wins_1=advent_day.left_wins_1,
            left_wins_2=advent_day.left_wins_2,
            left_wins_3=advent_day.left_wins_3,
            count_clicks=advent_day.count_clicks
        ))
        await session.commit()


async def update_advent_day(advent_day: AdventDay):
    async with async_session() as session:
        await session.execute(update(AdventDay).where(AdventDay.day == advent_day.day).
                              values(
            count_wins_1=advent_day.count_wins_1,
            count_wins_2=advent_day.count_wins_2,
            count_wins_3=advent_day.count_wins_3,
            msgs_wins=advent_day.msgs_wins,
            msgs_loses=advent_day.msgs_loses,
        ))

        await session.commit()


async def sync_history_lucky_post():
    pass


async def add_winner(tg_id: BigInteger, day: int, type_prize: int):
    async with async_session() as session:
        session.add(Winner(tg_id=tg_id, day=day, type_prize=type_prize))
        await session.commit()


async def get_winner(tg_id: BigInteger) -> Winner | None:
    async with async_session() as session:
        result = await session.scalar(select(Winner).where(Winner.tg_id == tg_id))
        if result:
            return result
        return None


async def get_analytics() -> List[int]:
    async with async_session() as session:
        count_users = await session.scalar(select(func.count(User.tg_id)))
        count_new_subscribers = await session.scalar(select(func.count(User.tg_id)).where(User.new_subscriber == True))
        count_new_members = await session.scalar(select(func.count(User.tg_id)).where(User.new_subscriber == True, User.member == "new"))
        summary_clicks = await session.scalar(select(func.sum(AdventDay.count_clicks)))
        count_users_with_mark = await session.scalar(select(func.count(User.tg_id)).where(User.mark != ""))

    return [count_users, count_new_subscribers, count_new_members, summary_clicks, count_users_with_mark]