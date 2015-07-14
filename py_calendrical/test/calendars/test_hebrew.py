import unittest

from py_calendrical.calendars.hebrew import HebrewDate, HebrewMonth

class HebrewSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(HebrewDate.from_fixed(self.testvalue), HebrewDate(5706, HebrewMonth.KISLEV, 7))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, HebrewDate(5706, HebrewMonth.KISLEV, 7).to_fixed())

if __name__ == "__main__":
    unittest.main()