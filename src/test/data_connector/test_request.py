from data_connector.request import Request
import datetime

import unittest


class TestRequest(unittest.TestCase):
    def test_AWS_small_numbers(self):
        date = datetime.date(year=2019, month=2, day=4)
        time = datetime.time(hour=5, minute=2, second=9)
        request = Request("KDMX", date, time)

        self.assertEqual(request.awsKey(), "2019/02/04/KDMX/KDMX20190204_050209")

    def test_AWS_large_numbers(self):
        date = datetime.date(year=2022, month=11, day=16)
        time = datetime.time(hour=21, minute=59, second=59)
        request = Request("KAMX", date, time)

        self.assertEqual(request.awsKey(), "2022/11/16/KAMX/KAMX20221116_215959")

    def test_cache_small_numbers(self):
        date = datetime.date(year=2019, month=2, day=4)
        time = datetime.time(hour=5, minute=2, second=9)
        request = Request("KDMX", date, time)

        self.assertEqual(request.cacheKey(), "KDMX_20190204_050209")

    def test_cache_large_numbers(self):
        date = datetime.date(year=2022, month=11, day=16)
        time = datetime.time(hour=21, minute=59, second=59)
        request = Request("KAMX", date, time)

        self.assertEqual(request.cacheKey(), "KAMX_20221116_215959")
