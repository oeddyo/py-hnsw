import random
from unittest import TestCase
from hnsw.hnsw_index import HNSWIndex


class Test(TestCase):
    def setUp(self) -> None:
        random.seed(42)

    def test_add_one_item(self):
        hnsw = HNSWIndex(2, 16, 100)

        hnsw.add_item("doc1", [1.0, 2.0])

        self.assertEqual(hnsw.entry_point[0], "doc1")

    def test_add_multiple_item(self):
        hnsw = HNSWIndex(2, 2, 100)

        hnsw.add_item("doc1", [1.0, 2.0])
        hnsw.add_item("doc2", [2.0, 2.0])

        self.assertEqual("doc2", hnsw.entry_point[0])
