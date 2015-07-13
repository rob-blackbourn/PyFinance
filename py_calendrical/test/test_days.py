import unittest
from py_calendrical.days import DayOfWeek


class Test(unittest.TestCase):


    def testDayOfWeek(self):
        m = DayOfWeek.Monday
        print m


if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()