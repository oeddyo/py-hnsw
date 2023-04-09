import random
from unittest import TestCase

from common.util import get_random_level


class UtilTest(TestCase):
    def test_random_level(self):
        random.seed(42)
        self.assertEqual(0, get_random_level(0.38))

        self.assertEqual(1, get_random_level(0.38))

        self.assertEqual(2, get_random_level(2))
