import datetime
import unittest

from lib.model.record import Record


class TestRecord(unittest.TestCase):
    def testAWSSmallNumbers(self) -> None:
        time = datetime.datetime(2019, 2, 4, hour=5, minute=2, second=9)
        record = Record("KDMX", time)

        self.assertEqual("2019/02/04/KDMX/KDMX20190204_050209_V06", record.awsKey())

    def testAWSLargeNumbers(self) -> None:
        time = datetime.datetime(2022, 11, 16, hour=21, minute=59, second=59)
        record = Record("KAMX", time)

        self.assertEqual("2022/11/16/KAMX/KAMX20221116_215959_V06", record.awsKey())

    def testCacheSmallNumbers(self) -> None:
        time = datetime.datetime(2019, 2, 4, hour=5, minute=2, second=9)
        record = Record("KDMX", time)

        self.assertEqual("KDMX20190204_050209", record.cacheKey())

    def testCacheLargeNumbers(self) -> None:
        time = datetime.datetime(2022, 11, 16, hour=21, minute=59, second=59)
        record = Record("KAMX", time)

        self.assertEqual("KAMX20221116_215959", record.cacheKey())
