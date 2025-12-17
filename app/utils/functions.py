from datetime import datetime, timedelta, date, time
from random import randint, random


def check_winner(
        total_prizes: int,
        prizes_given: int,
        min_chance: float = 0.005,
        max_chance: float = 1.0,
) -> bool:
    return random() < 0.5
    # if total_prizes == prizes_given:
    #     return False
    #
    # now = datetime.now() + timedelta()
    #
    # # сколько прошло секунд с начала дня
    # seconds_passed = (
    #         now - datetime.combine(now.date(), time.min)
    # ).total_seconds()
    #
    # # всего секунд в дне
    # seconds_in_day = 24 * 60 * 60
    #
    # # Часть дня, которая прошла
    # day_progress = seconds_passed / seconds_in_day
    #
    # # сколько призов должно быть выдано к этому моменту
    # expected_given = total_prizes * day_progress
    #
    # # отклонение от плана
    # delta = expected_given - prizes_given
    #
    # # вероятность выигрыша
    # chance = delta / total_prizes
    #
    # if chance < 0.5:
    #     chance /= 5
    #
    # chance = max(min_chance, min(chance, max_chance))
    #
    # return random() < chance