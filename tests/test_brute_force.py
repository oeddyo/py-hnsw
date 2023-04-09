from unittest import TestCase
from hnsw.brute_force import BruteForce


class Test(TestCase):

    def test_add_different_dimension(self):

        bf = BruteForce(dim=10)

        with self.assertRaises(AssertionError):
            bf.add("doc1", [1.0])


