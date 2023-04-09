from typing import List, Tuple

from hnsw.myvector import Vector
from hnsw.distance import euclidean


class BruteForce:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = {}

    def add(self, doc_id: str, v: Vector) -> None:
        assert len(v) == self.dim, "Added doc has different dimension than the dim of index"
        self.index[doc_id] = v

    def knn(self, k: int, q: Vector) -> List[Tuple[str, float]]:
        distances = []
        for k, v in self.index.items():
            d = euclidean(v, q)
            distances.append((d, k))

        # now sort and take top-k
        sorted_docs = sorted(distances)[:k]

        results = []
        for dis, doc_id in sorted_docs:
            results.append((doc_id, dis))

        return results
