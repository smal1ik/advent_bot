from app.database.models import AdventDay
from app.database.requests import get_advent_day, add_advent_day, update_advent_day

msg_wins_1 = """Поздравляем, удача выбрала именно тебя! 

Используй подарочную карту и исполни своё новогоднее fashion-желание.

С тобой свяжется менеджер и обсудит детали получения подарка.

*рассылка подарков будет осуществляться до конца января"""

msg_wins_2 = """Ура, ты стал победителем — новогодняя магия явно на твоей стороне! 

Лови стильный аксессуар и добавь своему образу яркости в праздничный сезон.

С тобой свяжется менеджер и обсудит детали получения подарка.

*рассылка подарков будет осуществляться до конца января"""

msg_wins_3 = """Вау! Ты стал обладателем нашего эксклюзивного супер-бокса! 

С тобой свяжется менеджер и обсудит детали получения подарка.

*рассылка подарков будет осуществляться до конца января"""


advent_calendar = [
    AdventDay(day=8, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=9, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=15, msgs_wins=["", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=3),
    AdventDay(day=16, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=17, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=18, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=3),
    AdventDay(day=19, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=1),
    AdventDay(day=20, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=21, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=22, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=3),
    AdventDay(day=23, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=24, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=4),
    AdventDay(day=25, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=26, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=27, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2),
    AdventDay(day=28, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=5),
    AdventDay(day=29, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=3),
    AdventDay(day=30, msgs_wins=["1", "2", "3"], msgs_loses=["11", "22", "33"], count_wins=2)
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