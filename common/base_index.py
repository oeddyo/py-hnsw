from abc import abstractmethod, ABC
from typing import Tuple, List

from common.vector import Vector


class BaseIndex(ABC):

    @abstractmethod
    def add_item(self, doc_id: str, v: Vector):
        pass

    @abstractmethod
    def knn(self, k: int, query_vector: Vector) -> List[Tuple[str, float]]:
        pass
