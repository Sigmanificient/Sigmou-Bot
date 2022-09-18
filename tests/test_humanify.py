import unittest

from sigmou.utils.humanify import pretty_time, pretty_time_small


class MyTestCase(unittest.TestCase):
    def test_pretty_time(self):
        self.assertEqual(pretty_time(1), "`1`s")
        self.assertEqual(pretty_time(10), "`10`s")

        self.assertEqual(pretty_time(60), "`1`m")
        self.assertEqual(pretty_time(3600), "`1`h")
        self.assertEqual(pretty_time(86400), "`1`d")
        self.assertEqual(pretty_time(31536000), "`1`y")

        self.assertEqual(pretty_time(99999999), "`3`y, `62`d, `9`h, `46`m and `39`s")

        self.assertEqual(pretty_time(31536001), "`1`y and `1`s")

    def test_pretty_time_small(self):
        self.assertEqual(pretty_time_small(0.1), "100.00ms")
        self.assertEqual(pretty_time_small(0.005), "5.00ms")
        self.assertEqual(pretty_time_small(0.0005), "500.00µs")
        self.assertEqual(pretty_time_small(0.0000005), "500.00ns")


if __name__ == "__main__":
    unittest.main()
