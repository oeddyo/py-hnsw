from unittest import TestCase
from brute_force.brute_force import BruteForce


class Test(TestCase):

    def test_add_different_dimension(self):

        bf = BruteForce(dim=10)

        with self.assertRaises(AssertionError):
            bf.add_item("doc1", [1.0])

    def test_bf_with_multiple_vectors(self):
        bf = BruteForce(dim=2)

        v1 = [0.0, 0.0]
        v2 = [1.0, 2.0]
        v3 = [100.0, 100.0]

        bf.add_item("doc1", v1)
        bf.add_item("doc2", v2)
        bf.add_item("doc3", v3)

        ans = bf.knn(1, [99, 99])

        self.assertEqual(1, len(ans))

        self.assertEqual("doc3", ans[0][0])

