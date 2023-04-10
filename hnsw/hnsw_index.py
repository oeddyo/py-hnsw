import typing
from collections import defaultdict
from queue import PriorityQueue
from typing import List, Tuple

from common.base_index import BaseIndex
from common.distance import euclidean
from common.util import get_random_level
from common.vector import Vector

import math

StringOpt = typing.Union[str, None]


class HNSWIndex(BaseIndex):

    def __init__(self, dim: int = 64, m: int = 16, ef_construction: int = 100):
        """
        Create HNSW index

        :param dim: dimension of the index.
        :param m: parameter used by HNSW. A reasonable range of M is from 5 to 48 according to the paper
        """
        self.dim = dim
        self.m = m
        self.ef_construction = ef_construction

        # the maximum number of connections an element can have in the zero layer
        self.max_m_0 = self.m * 2

        # line2: ep in the paper
        self.entry_point_id: StringOpt = None

        # multiplier corresponds to the "multi_" term used in hnswlib
        # it's a multiplier derived from the parameter m, and once initialized it won't change later on
        self.multiplier = 1 / math.log(m)
        self.max_level = -1
        self.vector_dict = {}

        # key is level, value is the adjacent list on that level
        # format is {[from_node]:
        self.level_graphs = []

    def _get_neighbourhood(self, cur: str, level: int) -> List[str]:
        return self.level_graphs[level][cur]

    def _search_layer(self, q: Vector, enter_point: str, ef: int, level: int) -> List[str]:
        """
        Search on a specific level and return closest ef candidates. The search starts from enter_point

        :param q: the query vector to search for on the level
        :param enter_point: enter point
        :param ef: how many to return
        :param level: level on the hierarchy graph
        """
        # pq is a min heap
        pq = PriorityQueue()
        pq.put((euclidean(q, self.vector_dict[enter_point]), enter_point))
        visited = set()

        # results is a max heap
        results = PriorityQueue()

        while pq.qsize() > 0:
            cur_dis, cur = pq.get()
            if cur in visited:
                continue
            visited.add(cur)

            largest = -results.queue[0][0] if results.qsize() > 0 else 0
            if cur_dis > largest and results.qsize() >= ef:
                break

            for adj_node in self._get_neighbourhood(cur, level):
                if adj_node not in visited:
                    distance = euclidean(self.vector_dict[adj_node], q)
                    if results.qsize() < ef:
                        results.put((-distance, adj_node))
                        pq.put((distance, adj_node))
                    else:
                        results.get()
                        pq.put((distance, adj_node))

        to_return = []
        for i in range(min(ef, results.qsize())):
            _, cur = results.get()
            to_return.append(cur)

        return to_return

    def add_item(self, doc_id: str, v: Vector):

        # add the vector to dic immediately so following code can access the item in dic
        self.vector_dict[doc_id] = v

        # get entry point
        ep = self.entry_point_id
        assigned_initial_level = get_random_level(self.multiplier)

        # if it's adding the first point in index, do nothing
        if self.entry_point_id is not None:
            for level in range(self.max_level, assigned_initial_level, -1):
                # move enter point from top level to the next
                _, ep = self._search_layer(v, ep, 1, level)[0]

            for level in range(min(assigned_initial_level, self.max_level), -1, -1):
                neighbour_with_distances = \
                    sorted(self._search_layer(v, ep, self.ef_construction, level))[:self.m]

                # get the first m neighbour and create edges on level
                for dis, node in neighbour_with_distances:
                    # create bi-directional edge on level
                    self.level_graphs[level][node].append((doc_id, dis))
                    self.level_graphs[level][doc_id].append((node, dis))

                for _, e in neighbour_with_distances:
                    e_conn = self._get_neighbourhood(e, level)
                    m_max = self.max_m_0 if level == 0 else self.m

                    if len(e_conn) > m_max:
                        # from e_conn pick m closest nodes



                        pass

                # potentially shrink connections

                ep = neighbour_with_distances[0][1]

        # update max level and enter point when the current level is larger than max level
        if assigned_initial_level > self.max_level:
            self.max_level = assigned_initial_level
            self.entry_point_id = doc_id
            if len(self.level_graphs) < self.max_level + 1:
                for i in range(self.max_level + 1 - len(self.level_graphs)):
                    self.level_graphs.append(defaultdict(list))

    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        return []
