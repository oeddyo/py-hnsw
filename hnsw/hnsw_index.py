import typing
from queue import PriorityQueue
from typing import List, Tuple

from common.base_index import BaseIndex
from common.distance import euclidean
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
        self.vector_dict = {}

        # key is level, value is the adjacent list on that level
        self.level_graphs = {}

    def _get_neighbourhood(self, cur: int, level: int) -> List[str]:
        return self.level_graphs[level][cur]

    def _search_layer(self, q: Vector, enter_point: str, ef: int, level: int) -> List[str]:
        """
        Search on a specific level and return closest ef candidates. The search starts from enter_point

        :param q: the query vector to search for on the level
        :param enter_point: enter point
        :param ef: how many to return
        :param level: level on the hierarchy graph
        """
        visited = set()
        visited.add(enter_point)

        cur_point_vector = self.vector_dict[enter_point]
        q_to_enter_point = euclidean(q, cur_point_vector)

        candidates = PriorityQueue()
        candidates.put((q_to_enter_point, enter_point))

        results = []

        while candidates.qsize() > 0:
            closest_dis, closest_point = candidates.get()

            for neighbour in self._get_neighbourhood(closest_point, level):
                if neighbour not in visited:
                    visited.add(neighbour)

                    distance = euclidean(self.vector_dict[neighbour], q)

                    if len(results) < ef:
                        results.append((distance, neighbour))

        return [doc_id for (dis, doc_id) in sorted(results)[:ef]]

    def add_item(self, doc_id: str, v: Vector):
        # get entry point
        ep = self.entry_point_id
        current_level = get_random_level(self.multiplier)

        # if it's adding the first point in index, do nothing
        if self.entry_point_id is not None:

            # get the entry point in the vector space
            # we call it cur_point. It means the current position of our exploration on the graph
            cur_point = self.vector_dict[self.entry_point_id]

            # get the distance of the inserted vector v to the "cur_point"
            distance_to_v = euclidean(v, cur_point)
            for level in range(self.max_level, current_level, -1):
                changed = True
                while changed:
                    changed = False

                    # from the cur_point, we find all the

            pass

        # update max level and enter point when the current level is larger than max level
        if current_level > self.max_level:
            self.max_level = current_level
            self.entry_point_id = doc_id

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        return []
