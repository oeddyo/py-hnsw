import math
from common.vector import Vector


def euclidean(a: Vector, b: Vector) -> float:
    assert len(a) == len(b), "Vectors have different dim"
    dis = 0
    for i in range(len(a)):
        dis += (a[i] - b[i]) ** 2
    return math.sqrt(dis)

