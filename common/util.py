import math
import random


def get_random_level(multiplier: float) -> int:
    rnd = random.random()
    r = -math.log(rnd) * multiplier
    return math.floor(r)
