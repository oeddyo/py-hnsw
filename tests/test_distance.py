from unittest import TestCase
from common.distance import euclidean


class DistanceTest(TestCase):
    def test_when_dim_diff(self):
        with self.assertRaises(AssertionError):
            dis = euclidean([1.0], [1.0, 2.0])

    def test_euclidean_distance_zero(self):
        dis = euclidean([1.0], [1.0])

        self.assertAlmostEqual(0.0, dis)

    def test_euclidean_distance_large(self):
        dis = euclidean([1.0, 2.0, 3.0], [0.0, -1.0, -2.0])

        self.assertAlmostEqual(5.916079783099616, dis)
