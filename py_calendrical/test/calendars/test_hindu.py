import unittest

from py_calendrical.calendars.hindu import OldHinduSolarDate, OldHinduLunarDate, OldHindu

class OldHinduSmokeTestCase(unittest.TestCase):
    
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(OldHinduSolarDate.from_fixed(self.testvalue), OldHinduSolarDate(5046, 7, 29))
        self.assertEqual(OldHinduLunarDate.from_fixed(self.testvalue), OldHinduLunarDate(5046, 8, False, 8))
        # FIXME (not sure the check is correct)
        self.assertEqual(OldHindu.jovian_year(self.testvalue), 32)

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, OldHinduSolarDate(5046, 7, 29).to_fixed())
        self.assertEqual(self.testvalue, OldHinduLunarDate(5046, 8, False, 8).to_fixed())

if __name__ == "__main__":
    unittest.main()