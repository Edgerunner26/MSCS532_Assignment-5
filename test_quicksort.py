"""Correctness tests for both sorting implementations."""

import random
import unittest
from quicksort import quicksort, randomized_quicksort


class QuicksortTests(unittest.TestCase):
    def check_case(self, data):
        expected = sorted(data)
        for algorithm in (quicksort, randomized_quicksort):
            with self.subTest(algorithm=algorithm.__name__, size=len(data)):
                actual = data.copy()
                result = algorithm(actual)
                self.assertEqual(actual, expected)
                self.assertIsNone(result)

    def test_edge_cases(self):
        for data in ([], [1], [2, 1], [1, 1], [0, -3, 7, -3]):
            self.check_case(data)

    def test_ordered_inputs(self):
        self.check_case(list(range(1200)))
        self.check_case(list(range(1200, 0, -1)))

    def test_equal_values(self):
        self.check_case([5] * 1200)

    def test_random_inputs(self):
        rng = random.Random(2026)
        for size in (10, 100, 500):
            self.check_case([rng.randrange(-100, 101) for _ in range(size)])


if __name__ == "__main__":
    unittest.main()
