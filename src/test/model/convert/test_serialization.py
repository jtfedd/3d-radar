import test.testutils.models as util
import unittest

from lib.model.serialization import serialization


class TestSerialization(unittest.TestCase):
    def testSerializeRecord(self) -> None:
        record = util.newTestRecord()
        recordBytes = serialization.serializeRecord(record)
        self.assertEqual(len(recordBytes), 12)

        output, size = serialization.deserializeRecord(recordBytes)
        util.assertRecordsEqual(self, record, output)
        self.assertEqual(size, len(recordBytes))

    def testSerializeSweepMeta(self) -> None:
        sweepMeta = util.newTestSweepMeta()
        sweepMetaBytes = serialization.serializeSweepMeta(sweepMeta)
        self.assertEqual(len(sweepMetaBytes), 32)

        output, size = serialization.deserializeSweepMeta(sweepMetaBytes)
        util.assertSweepMetasEqual(self, sweepMeta, output)
        self.assertEqual(size, len(sweepMetaBytes))

    def testSerializeScanData(self) -> None:
        scanData = util.newTestScanData()
        scanDataBytes = serialization.serializeScanData(scanData)
        self.assertEqual(len(scanDataBytes), 4328)

        output, size = serialization.deserializeScanData(scanDataBytes)
        util.assertScanDatasEqual(self, scanData, output)
        self.assertEqual(size, len(scanDataBytes))

    def testSerializeScan(self) -> None:
        scan = util.newTestScan()
        scanBytes = serialization.serializeScan(scan)
        self.assertEqual(len(scanBytes), 8668)

        output, size = serialization.deserializeScan(scanBytes)
        util.assertScansEqual(self, scan, output)
        self.assertEqual(size, len(scanBytes))
