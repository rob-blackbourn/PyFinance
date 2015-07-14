import unittest
from py_calendrical.calendars.aztec import AztecXihuitlDate


class AztecSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(AztecXihuitlDate.from_fixed(self.testvalue), AztecXihuitlDate(2, 1))

    def testConversionToFixed(self):
        self.assertEqual(AztecXihuitlDate.on_or_before(AztecXihuitlDate(2, 1), self.testvalue), self.testvalue)

if __name__ == "__main__":
    unittest.main()