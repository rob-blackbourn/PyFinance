import unittest

from py_calendrical.calendars.islamic import IslamicDate

class IslamicSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(IslamicDate.from_fixed(self.testvalue), IslamicDate(1364, 12, 6))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, IslamicDate(1364, 12, 6).to_fixed())

if __name__ == "__main__":
    unittest.main()