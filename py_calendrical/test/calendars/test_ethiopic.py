import unittest

from py_calendrical.calendars.ethiopic import EthiopicDate

class EthiopicSmokeTestCase(unittest.TestCase):

    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(EthiopicDate.from_fixed(self.testvalue), EthiopicDate(1938, 3, 3))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, EthiopicDate(1938, 3, 3).to_fixed())

if __name__ == "__main__":
    unittest.main()