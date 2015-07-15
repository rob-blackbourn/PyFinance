import unittest

from py_calendrical.calendars.iso import IsoDate

class ISOSmokeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347
        self.aDate = IsoDate(1945, 46, 1)

    def testConversionFromFixed(self):
        self.assertEqual(IsoDate.from_fixed(self.testvalue), IsoDate(1945, 46, 1))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, IsoDate(1945, 46, 1).to_fixed())

if __name__ == "__main__":
    unittest.main()