from app.database.requests import get_advent_day, add_advent_day, update_advent_day
from app.utils.models import AdventDay, TypeAdventDay

advent_calendar = [
    AdventDay(day=1, type=TypeAdventDay.LINK, link="tg.com"),
    AdventDay(day=2, type=TypeAdventDay.TEXT, text="text"),
    AdventDay(day=3, type=TypeAdventDay.LUCKY_CLICK, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2, left_wins=10),
]


async def migration_advent_calendar():
    for day in advent_calendar:
        db_day = await get_advent_day(day.day)
        if not db_day:
            print(f"День {day.day} добавлен")
            await add_advent_day(day)
        else:
            print(f"День {day.day} обновлен")
            await update_advent_day(day)