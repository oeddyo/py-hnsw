import typing
from typing import List, Tuple

from common.base_index import BaseIndex
from common.util import get_random_level
from common.vector import Vector

import math

StringOpt = typing.Union[str, None]


class HNSWIndex(BaseIndex):

    def __init__(self, dim: int = 64, m: int = 16):
        """
        Create HNSW index

        :param dim: dimension of the index.
        :param m: parameter used by HNSW. A reasonable range of M is from 5 to 48 according to the paper
        """
        self.dim = dim

        # line2: ep in the paper
        self.entry_point_id: StringOpt = None

        # multiplier corresponds to the "multi_" term used in hnswlib
        # it's a multiplier derived from the parameter m, and once initialized it won't change later on
        self.multiplier = 1 / math.log(m)
        self.max_level = -1

    def add_item(self, doc_id: str, v: Vector):
        # get entry point
        ep = self.entry_point_id
        current_level = get_random_level(self.multiplier)

        if self.entry_point_id is None:
            # adding first point, do nothing but
            self.max_level = current_level
            self.entry_point_id = doc_id
        else:
            self.entry_point_id = "sdf"
            pass

        # update max level and enter point when the current level is larger than max level
        if current_level > self.max_level:
            self.max_level = current_level
            self.entry_point_id = doc_id

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        return []
