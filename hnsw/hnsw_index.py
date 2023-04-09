from typing import List, Tuple

from common.base_index import BaseIndex
from common.vector import Vector

import math


class HNSWIndex(BaseIndex):

    def __init__(self, dim: int = 64, m: int = 16):
        """
        Create HNSW index

        :param dim: dimension of the index.
        :param m: parameter used by HNSW
        """
        self.dim = dim

        # line2: ep in the paper
        self.entry_point = None

        # multiplier corresponds to the "multi_" term used in hnswlib
        # it's a multiplier derived from the parameter m and it won't change later on
        self.multiplier = 1 / math.log(m)

    def add_item(self, doc_id: str, v: Vector):
        # get entry point
        ep = self.entry_point

        pass

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        return []
