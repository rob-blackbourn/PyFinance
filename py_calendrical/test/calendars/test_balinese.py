import unittest

from py_calendrical.calendars.balinese import BalinesePawukonDate

class BalineseSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(BalinesePawukonDate.from_fixed(self.testvalue), BalinesePawukonDate(True, 2, 1, 1, 3, 1, 2, 5, 7, 2))

    def testConversionToFixed(self):
        self.assertEqual(BalinesePawukonDate.on_or_before(BalinesePawukonDate(True, 2, 1, 1, 3, 1, 2, 5, 7, 2), self.testvalue), self.testvalue)

if __name__ == "__main__":
    unittest.main()