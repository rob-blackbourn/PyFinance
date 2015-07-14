import unittest

from py_calendrical.calendars.egyptian import EgyptianDate

class EgyptianSmokeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347
        self.aDate = EgyptianDate(2694, 7, 10)

    def testConversionFromFixed(self):
        self.assertEqual(EgyptianDate.from_fixed(self.testvalue), EgyptianDate(2694, 7, 10))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, EgyptianDate(2694, 7, 10).to_fixed())

if __name__ == "__main__":
    unittest.main()