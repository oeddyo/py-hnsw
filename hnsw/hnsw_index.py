from typing import List, Tuple

from common.base_index import BaseIndex
from common.vector import Vector


class HNSWIndex(BaseIndex):
    def __init__(self, dim=64):
        self.dim = dim

    def add_item(self, doc_id: str, v: Vector):
        pass

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        return []

