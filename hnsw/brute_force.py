from typing import List, Tuple

from common.vector import Vector
from common.distance import euclidean


class BruteForce:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = {}

    def add(self, doc_id: str, v: Vector) -> None:
        assert len(v) == self.dim, "Added doc has different dimension than the dim of index"
        self.index[doc_id] = v

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        distances = []
        for doc_id, doc_vector in self.index.items():
            distance = euclidean(doc_vector, query_vector)
            distances.append((distance, doc_id))

        # now sort and take k-smallest distance vectors
        sorted_docs = sorted(distances)[:k]

        results = []
        for dis, doc_id in sorted_docs:
            results.append((doc_id, dis))

        return results
