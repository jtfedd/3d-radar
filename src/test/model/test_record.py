from lib.model.record import Record
import datetime

import unittest


class TestRecord(unittest.TestCase):
    def test_AWS_small_numbers(self):
        time = datetime.datetime(2019, 2, 4, hour=5, minute=2, second=9)
        record = Record("KDMX", time)

        self.assertEqual("2019/02/04/KDMX/KDMX20190204_050209", record.awsKey())

    def test_AWS_large_numbers(self):
        time = datetime.datetime(2022, 11, 16, hour=21, minute=59, second=59)
        record = Record("KAMX", time)

        self.assertEqual("2022/11/16/KAMX/KAMX20221116_215959", record.awsKey())

    def test_cache_small_numbers(self):
        time = datetime.datetime(2019, 2, 4, hour=5, minute=2, second=9)
        record = Record("KDMX", time)

        self.assertEqual("KDMX20190204_050209", record.cacheKey())

    def test_cache_large_numbers(self):
        time = datetime.datetime(2022, 11, 16, hour=21, minute=59, second=59)
        record = Record("KAMX", time)

        self.assertEqual("KAMX20221116_215959", record.cacheKey())
