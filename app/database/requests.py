from app.database.models import User, async_session, AdventDay
from sqlalchemy import select, BigInteger, update, delete, func, case, insert, or_


async def add_user(tg_id: BigInteger, first_name: str, username: str, full_name: str, mark: str = ""):
    """
    Функция добавляет пользователя в БД
    """
    async with async_session() as session:
        session.add(User(
            tg_id=tg_id,
            first_name=first_name,
            username=username,
            full_name=full_name,
            mark=mark))
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
        session.add(advent_day)
        await session.commit()


async def update_stats_advent_day(advent_day: AdventDay):
    async with async_session() as session:
        await session.execute(update(AdventDay).where(AdventDay.day == advent_day.day).
                              values(
            left_wins=advent_day.left_wins,
            count_clicks=advent_day.count_clicks,
            winners=advent_day.winners
        ))
        await session.commit()


async def update_advent_day(advent_day: AdventDay):
    async with async_session() as session:
        await session.execute(update(AdventDay).where(AdventDay.day == advent_day.day).
                              values(
            count_wins=advent_day.count_wins,
            msgs_wins=advent_day.msgs_wins,
            msgs_loses=advent_day.msgs_loses,
        ))

        await session.commit()


async def sync_history_lucky_post():
    pass