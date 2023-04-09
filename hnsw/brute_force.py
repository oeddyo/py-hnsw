from typing import List

from vector import Vector

class BruteForce:
    def __init__(self):
        self.index = {}

    def add(self, doc_id: str, v: Vector) -> None:
        self.index[doc_id] = v

    def knn(self, k: int) -> List[Vector]:

        for v in self.index.values():


        return []
