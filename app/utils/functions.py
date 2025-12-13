from datetime import datetime, timedelta


def frac_of_day(now=None, day_start_hour=0, day_end_hour=24):
    now = now or datetime.now() + timedelta(hours=3)
    start = now.replace(hour=day_start_hour, minute=0, second=0, microsecond=0)
    end = now.replace(hour=day_end_hour % 24, minute=0, second=0, microsecond=0)
    total = (end - start).total_seconds()
    elapsed = (now - start).total_seconds()
    if total <= 0:
        return 1.0
    return max(0.0, min(1.0, elapsed / total))


def win_probability(R, t, base=0.10, s=2.0, k=2.0, h=5.0, p_max=0.5):
    if R <= 0:
        return 0.0
    W = 1.0 + s * (t ** k)            # временной множитель
    I = R / (R + h)                  # инвентарный множитель
    p = base * W * I
    return max(0.0, min(p_max, p))

now_t = frac_of_day()
print(now_t)
p = win_probability(R=3,
                    t=now_t)
print(p*100)