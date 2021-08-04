from time import sleep
from typing import List

from app.utils.timer import time
import unittest

FIXED_SIZE: int = 1_000_000
MAX_GAP: float = 0.01


class MyTestCase(unittest.TestCase):

    def test_duplicates(self):
        chronos: List[int] = [time() for _ in range(FIXED_SIZE)]
        self.assertEqual(len(set(chronos)), FIXED_SIZE)

    def test_performance(self):
        t: float = time()
        sleep(1)
        elapsed: int = time(t)

        self.assertAlmostEqual(elapsed, 1, delta=MAX_GAP)

    def test_big(self):
        """Checking Timer Performance and Validating."""
        chronos: List[int] = [time() for _ in range(1_000_000)]

        sleep(1)

        times: List[float] = [time(key) for key in chronos]
        self.assertLessEqual(times[-1] - times[0], MAX_GAP)


if __name__ == '__main__':
    unittest.main()
