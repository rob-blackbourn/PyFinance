import unittest

from py_calendrical.calendars.armenian import ArmenianDate

class ArmenianSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(ArmenianDate.from_fixed(self.testvalue), ArmenianDate(1395, 4, 5))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, ArmenianDate(1395, 4, 5).to_fixed())
        
if __name__ == "__main__":
    unittest.main()