import unittest

from py_calendrical.calendars.coptic import CopticDate

class CopticSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(CopticDate.from_fixed(self.testvalue), CopticDate(1662, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, CopticDate(1662, 3, 3).to_fixed())

if __name__ == "__main__":
    unittest.main()