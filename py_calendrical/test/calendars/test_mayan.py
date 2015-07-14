import unittest

from py_calendrical.calendars.mayan import MayanLongCountDate, MayanHaabDate, MayanTzolkinDate

class MayanSmokeTestCase(unittest.TestCase):
    def setUp(self):
        self.testvalue = 710347

    def testConversionFromFixed(self):
        self.assertEqual(MayanLongCountDate.from_fixed(self.testvalue), MayanLongCountDate(12, 16, 11, 16, 9))
        self.assertEqual(MayanLongCountDate.from_fixed(0), MayanLongCountDate(7, 17, 18, 13, 2))
        self.assertEqual(MayanHaabDate.from_fixed(self.testvalue), MayanHaabDate(11, 7))
        self.assertEqual(MayanTzolkinDate.from_fixed(self.testvalue), MayanTzolkinDate(11, 9))

    def testConversionToFixed(self):
        self.assertEqual(self.testvalue, MayanLongCountDate(12, 16, 11, 16, 9).to_fixed())
        self.assertEqual(0, MayanLongCountDate(7, 17, 18, 13, 2).to_fixed())
        self.assertEqual(MayanHaabDate.on_or_before(MayanHaabDate(11, 7), self.testvalue), self.testvalue)
        self.assertEqual(MayanTzolkinDate.on_or_before(MayanTzolkinDate(11, 9), self.testvalue), self.testvalue)

if __name__ == "__main__":
    unittest.main()