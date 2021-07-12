from app.utils.humanify import pretty_time, pretty_time_small
import unittest


class MyTestCase(unittest.TestCase):

    def test_pretty_time(self):
        self.assertEqual(pretty_time(1),  '1s')
        self.assertEqual(pretty_time(10), '10s')

        self.assertEqual(pretty_time(60), '1m')
        self.assertEqual(pretty_time(3600), '1h')
        self.assertEqual(pretty_time(86400), '1d')
        self.assertEqual(pretty_time(31536000), '1y')

        self.assertEqual(pretty_time(99999999), '3y, 62d, 9h, 46m & 39s')
        self.assertEqual(pretty_time(31536001), '1y & 1s')

    def test_pretty_time_small(self):
        self.assertEqual(pretty_time_small(0.1), '100.00ms')
        self.assertEqual(pretty_time_small(0.005), '5.00ms')
        self.assertEqual(pretty_time_small(0.0005), '500.00µs')
        self.assertEqual(pretty_time_small(0.0000005), '500.00ns')


if __name__ == '__main__':
    unittest.main()
