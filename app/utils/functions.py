from datetime import datetime, timedelta
from random import randint


async def check_winner():
    n = randint(0, 100)
    if n < 50:
        return True
    else:
        return False
